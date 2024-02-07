from django.test import TestCase
from django.urls import reverse
from django.http import Http404
from unittest.mock import patch

from exporter.applications.views.hcsat import HCSATApplicationPage


class HCSATFullFormTestCase(TestCase):
    def setUp(self):
        self.application_id = 1
        self.url = reverse("applications:application", kwargs={"pk": self.application_id})
        self.view = HCSATApplicationPage()

    def test_get_application_url(self):
        self.assertEqual(self.view.get_application_url(), self.url)

    def test_get_context_data(self):
        context = self.view.get_context_data(pk=self.application_id)
        self.assertEqual(context["form_title"], "Application submitted")
        self.assertEqual(context["back_link_url"], self.url)
        self.assertEqual(context["reference_code"], "your_reference_code")
        self.assertEqual(
            context["links"],
            {
                "View your list of applications": reverse("applications:applications"),
                "Apply for another licence or clearance": reverse("apply_for_a_licence:start"),
                "Return to your export control account dashboard": reverse("core:home"),
            },
        )

    @patch("applications.views.hcsat.post_survey_feedback")
    def test_form_valid(self, mock_post_survey_feedback):
        form = self.view.form_class(data={"field1": "value1", "field2": "value2"})
        self.assertTrue(form.is_valid())

        self.view.request = self.client.request()
        self.view.kwargs = {"pk": self.application_id}
        self.view.form_valid(form)

        mock_post_survey_feedback.assert_called_once_with(self.view.request, self.application_id, form.cleaned_data)

    def test_get_success_url(self):
        self.assertEqual(self.view.get_success_url(), reverse("core:home"))

    def test_get_context_data_draft_status(self):
        self.view.request = self.client.request()
        self.view.kwargs = {"pk": self.application_id}
        with self.assertRaises(Http404):
            self.view.get_context_data(pk=self.application_id)
