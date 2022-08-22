import logging

from http import HTTPStatus

from django.conf import settings
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin

from lite_forms.generators import error_page

from exporter.core.wizard.views import BaseSessionWizardView
from exporter.core.common.decorators import expect_status
from exporter.core.common.exceptions import ServiceError
from exporter.core.helpers import get_document_data
from exporter.goods.forms.common import (
    ProductDocumentAvailabilityForm,
    ProductDocumentSensitivityForm,
    ProductDocumentUploadForm,
    ProductNameForm,
    ProductControlListEntryForm,
    ProductPVGradingForm,
    ProductPVGradingDetailsForm,
    ProductPartNumberForm,
)
from exporter.goods.forms.firearms import (
    FirearmOnwardExportedForm,
    FirearmOnwardAlteredProcessedForm,
    FirearmOnwardIncorporatedForm,
    FirearmQuantityAndValueForm,
)
from exporter.goods.forms.goods import ProductUsesInformationSecurityForm, ProductMilitaryUseForm

from exporter.goods.services import post_component, post_good_documents
from exporter.applications.services import post_product_good_on_application
from exporter.applications.views.goods.common.mixins import ApplicationMixin, GoodMixin
from exporter.applications.views.goods.common.conditionals import (
    is_pv_graded,
    is_product_document_available,
    is_document_sensitive,
    is_onward_exported,
)
from exporter.core.wizard.conditionals import C

from .constants import (
    AddGoodComponentSteps,
    AddGoodComponentToApplicationSteps,
)
from .mixins import NonFirearmsComponentFlagMixin
from .payloads import (
    AddGoodComponentPayloadBuilder,
    AddGoodComponentToApplicationPayloadBuilder,
)


logger = logging.getLogger(__name__)


class AddGoodComponent(
    LoginRequiredMixin,
    NonFirearmsComponentFlagMixin,
    ApplicationMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodComponentSteps.NAME, ProductNameForm),
        (AddGoodComponentSteps.PRODUCT_CONTROL_LIST_ENTRY, ProductControlListEntryForm),
        (AddGoodComponentSteps.PART_NUMBER, ProductPartNumberForm),
        (AddGoodComponentSteps.PV_GRADING, ProductPVGradingForm),
        (AddGoodComponentSteps.PV_GRADING_DETAILS, ProductPVGradingDetailsForm),
        (AddGoodComponentSteps.PRODUCT_USES_INFORMATION_SECURITY, ProductUsesInformationSecurityForm),
        (AddGoodComponentSteps.PRODUCT_DOCUMENT_AVAILABILITY, ProductDocumentAvailabilityForm),
        (AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY, ProductDocumentSensitivityForm),
        (AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD, ProductDocumentUploadForm),
        (AddGoodComponentSteps.PRODUCT_MILITARY_USE, ProductMilitaryUseForm),
    ]
    condition_dict = {
        AddGoodComponentSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodComponentSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodComponentSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request
        return kwargs

    def has_product_documentation(self):
        return self.condition_dict[AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD](self)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodComponentSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error with product document when creating component",
        "Unexpected error adding component",
    )
    def post_product_documentation(self, good):
        document_payload = self.get_product_document_payload()
        return post_good_documents(
            request=self.request,
            pk=good["id"],
            json=document_payload,
        )

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
        good_payload = AddGoodComponentPayloadBuilder().build(form_dict)
        return good_payload

    def get_success_url(self):
        return reverse(
            "applications:component_summary",
            kwargs={"pk": self.application["id"], "good_pk": self.good["id"]},
        )

    @expect_status(
        HTTPStatus.CREATED,
        "Error creating complete component",
        "Unexpected error adding complete component",
    )
    def post_component(self, form_dict):
        payload = self.get_payload(form_dict)

        return post_component(
            self.request,
            payload,
        )

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:
            raise service_error
        return error_page(self.request, service_error.user_message)

    def done(self, form_list, form_dict, **kwargs):
        try:
            good, _ = self.post_component(form_dict)
            self.good = good["good"]
            if self.has_product_documentation():
                self.post_product_documentation(self.good)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url())


class AddGoodComponentToApplication(
    LoginRequiredMixin,
    NonFirearmsComponentFlagMixin,
    ApplicationMixin,
    GoodMixin,
    BaseSessionWizardView,
):
    form_list = [
        (AddGoodComponentToApplicationSteps.ONWARD_EXPORTED, FirearmOnwardExportedForm),
        (AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED, FirearmOnwardAlteredProcessedForm),
        (AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED, FirearmOnwardIncorporatedForm),
        (AddGoodComponentToApplicationSteps.QUANTITY_AND_VALUE, FirearmQuantityAndValueForm),
    ]

    condition_dict = {
        AddGoodComponentToApplicationSteps.ONWARD_ALTERED_PROCESSED: is_onward_exported,
        AddGoodComponentToApplicationSteps.ONWARD_INCORPORATED: is_onward_exported,
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)
        return kwargs

    def get_success_url(self):
        return reverse(
            "applications:component_on_application_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_on_application_pk": self.good_on_application["id"],
            },
        )

    def get_payload(self, form_dict):
        good_on_application_payload = AddGoodComponentToApplicationPayloadBuilder().build(form_dict)
        return good_on_application_payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding component to application",
        "Unexpected error adding component to application",
    )
    def post_component_to_application(self, form_dict):
        payload = self.get_payload(form_dict)
        return post_product_good_on_application(
            self.request,
            self.application["id"],
            self.good["id"],
            payload,
        )

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["back_link_url"] = reverse(
            "applications:component_summary",
            kwargs={
                "pk": self.kwargs["pk"],
                "good_pk": self.good["id"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        if settings.DEBUG:  # pragma: no cover
            raise service_error
        return error_page(self.request, service_error.user_message)

    def done(self, form_list, form_dict, **kwargs):
        try:
            good_on_application, _ = self.post_component_to_application(form_dict)
            good_on_application = good_on_application["good"]
        except ServiceError as e:
            return self.handle_service_error(e)
        self.good_on_application = good_on_application

        return redirect(self.get_success_url())
