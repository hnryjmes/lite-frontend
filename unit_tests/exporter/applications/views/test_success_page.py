import pytest
from django.urls import reverse
from django.test import RequestFactory
from exporter.applications.views.common import ApplicationSubmitSuccessPage
from exporter.applications.forms import HCSATminiform


@pytest.fixture
def application_submit_success_page():
    factory = RequestFactory()
    request = factory.get(reverse("applications:application-submit-success", kwargs={"pk": 1}))
    view = ApplicationSubmitSuccessPage.as_view()
    return view(request, pk=1)


def test_application_submit_success_page_template(application_submit_success_page):
    response = application_submit_success_page.render()
    assert response.status_code == 200
    assert "applications/application-submit-success.html" in response.template_name


def test_application_submit_success_page_form_class(application_submit_success_page):
    assert application_submit_success_page.form_class == HCSATminiform


def test_application_submit_success_page_get_application_url(application_submit_success_page):
    url = application_submit_success_page.get_application_url()
    assert url == reverse("applications:application", kwargs={"pk": 1})


def test_application_submit_success_page_get_context_data(application_submit_success_page):
    context = application_submit_success_page.get_context_data()
    assert "form_title" in context
    assert "back_link_url" in context
    assert "reference_code" in context
    assert "links" in context


def test_application_submit_success_page_form_valid(application_submit_success_page):
    form = HCSATminiform()
    response = application_submit_success_page.form_valid(form)
    assert response.status_code == 302
    assert response.url == reverse("applications:application-hcsat", kwargs={"pk": 1})


def test_application_submit_success_page_get_success_url(application_submit_success_page):
    url = application_submit_success_page.get_success_url()
    assert url == reverse("applications:application-hcsat", kwargs={"pk": 1})
