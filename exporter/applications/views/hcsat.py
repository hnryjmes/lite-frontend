from http import HTTPStatus
from django.urls import reverse, reverse_lazy
from django.views.generic import FormView
from django.http import Http404
from core.decorators import expect_status
from exporter.applications.services import (
    get_application,
    post_survey_feedback,
)

from exporter.applications.forms.hcsat import HCSATApplicationForm
from core.auth.views import LoginRequiredMixin


class HCSATApplicationPage(LoginRequiredMixin, FormView):

    template_name = "applications/hcsat_form.html"
    form_class = HCSATApplicationForm

    def get_application_url(self):
        return reverse(
            "applications:application",
            kwargs={"pk": self.kwargs["pk"]},
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context["form_title"] = "Application submitted"
        context["back_link_url"] = self.get_application_url()
        return context

    @expect_status(
        HTTPStatus.OK,
        "Error sending feedback",
        "Unexpected error sending feedback",
    )
    def post_survey_feedback(self, request, application_pk, data):
        return post_survey_feedback(request, application_pk, data)

    def form_valid(self, form):
        self.post_survey_feedback(self.request, self.kwargs["pk"], form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:home")
