import logging
from http import HTTPStatus

from django.http import Http404
from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView

from core.auth.views import LoginRequiredMixin
from core.decorators import expect_status

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.applications.services import put_application, post_additional_document
from exporter.core.helpers import get_document_data
from exporter.applications.views.goods.common.mixins import ApplicationMixin

from .forms import SecurityClassifiedDetailsForm, F680ReferenceNumberForm, SecurityOtherDetailsForm, F1686DetailsForm

from .constants import ExportDetailsSteps
from .conditionals import is_f680_approval, is_f1686_approval, is_other_approval
from .payloads import ExportDetailsStepsPayloadBuilder
from .mixins import NonF680SecurityClassifiedFlagMixin

logger = logging.getLogger(__name__)


class ExportDetails(
    LoginRequiredMixin,
    ApplicationMixin,
    BaseSessionWizardView,
    NonF680SecurityClassifiedFlagMixin,
):
    form_list = [
        (ExportDetailsSteps.SECURITY_CLASSIFIED, SecurityClassifiedDetailsForm),
        (ExportDetailsSteps.F680_REFERENCE_NUMBER, F680ReferenceNumberForm),
        (ExportDetailsSteps.F1686_DETAILS, F1686DetailsForm),
        (ExportDetailsSteps.SECURITY_OTHER_DETAILS, SecurityOtherDetailsForm),
    ]

    condition_dict = {
        ExportDetailsSteps.F680_REFERENCE_NUMBER: is_f680_approval,
        ExportDetailsSteps.F1686_DETAILS: is_f1686_approval,
        ExportDetailsSteps.SECURITY_OTHER_DETAILS: is_other_approval,
    }

    def dispatch(self, request, **kwargs):
        if not settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED:
            raise Http404
        return super().dispatch(request, **kwargs)

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:new_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_payload(self, form_dict):
        export_details_payload = ExportDetailsStepsPayloadBuilder().build(form_dict)
        return export_details_payload

    def get_success_url(self):
        return reverse(
            "applications:application_export_details_summary",
            kwargs={"pk": self.application["id"]},
        )

    @expect_status(
        HTTPStatus.OK,
        "Error updating export details",
        "Unexpected error updating export details",
    )
    def update_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return put_application(
            self.request,
            self.application["id"],
            payload,
        )

    def done(self, form_list, form_dict, **kwargs):
        self.update_application(form_dict)
        return redirect(self.get_success_url())


class ApplicationExportDetailsSummaryView(LoginRequiredMixin, ApplicationMixin, TemplateView):
    template_name = "applications/export-details/application-export-details-summary.html"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["application"] = self.application
        context["back_link_url"] = reverse("applications:export_details", kwargs={"pk": self.kwargs["pk"]})
        return context
