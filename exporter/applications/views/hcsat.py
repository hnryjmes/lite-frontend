from http import HTTPStatus
from django.urls import reverse
from django.views.generic import FormView
from core.decorators import expect_status
from exporter.applications.services import (
    get_survey,
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
    def post_survey_feedback(self, request, data):
        return post_survey_feedback(request, data)

    @expect_status(
        HTTPStatus.OK,
        "Error getting application",
        "Unexpected error getting application",
    )
    def get_survey(self, request, survey_id):
        return get_survey(request, survey_id)

    def get_initial(self):
        self.object_pk = self.kwargs["pk"]
        self.survey, _ = self.get_survey(self.request, self.kwargs["sid"])
        initial = super().get_initial()
        initial["recommendation"] = self.survey.get("recommendation")
        return initial

    def form_valid(self, form):
        form_data = form.cleaned_data.copy()
        form_data["id"] = self.survey.get("id")
        self.post_survey_feedback(self.request, form_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("core:home")
