import pytest
from django.http import Http404
from django.urls import reverse
from exporter.applications.forms.hcsat import HCSATminiform
from http import HTTPStatus
from pytest_django.asserts import assertContains, assertTemplateUsed
from bs4 import BeautifulSoup
from unittest.mock import patch
from core import client


@pytest.fixture
def survey_id():
    return "6de657c9-e500-4791-8c8b-9f94dec2c629"  # /PS-IGNORE


@pytest.fixture
def hcsat_url(survey_id, application_pk):
    return reverse("applications:application-hcsat", kwargs={"sid": survey_id, "pk": application_pk})


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def application_url(application_pk):
    return reverse("applications:application", kwargs={"pk": application_pk})


@pytest.fixture
def application_start_url():
    return reverse("apply_for_a_licence:start")


@pytest.fixture
def home_url():
    return reverse("core:home")


@pytest.fixture
def application_reference_number(data_standard_case):
    return data_standard_case["case"]["reference_code"]


@pytest.fixture(autouse=True)
def mock_update_survey(requests_mock, survey_id):
    survey_url = client._build_absolute_uri(f"/survey/{survey_id}")
    return requests_mock.put(
        survey_url,
        json={"id": survey_id},
        status_code=200,
    )


@pytest.fixture(autouse=True)
def mock_get_survey(requests_mock, survey_id):
    survey_url = client._build_absolute_uri(f"/survey/{survey_id}")
    return requests_mock.get(
        survey_url,
        json={"id": survey_id},
        status_code=200,
    )


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, application_pk, application_reference_number):
    return requests_mock.get(
        client._build_absolute_uri(f"/applications/{application_pk}"),
        json={"id": application_pk, "reference_code": application_reference_number, "status": "submitted"},
        status_code=200,
    )


def test_hcsat_view(authorized_client, hcsat_url, application_url):
    response = authorized_client.get(hcsat_url)

    assert response.status_code == 200

    assert isinstance(response.context["form"], HCSATminiform)
    assertTemplateUsed(response, "applications/hcsat_form.html")

    soup = BeautifulSoup(response.content, "html.parser")

    # content
    assert soup.find("h1").string.strip() == "Give feedback on this service"
    assert soup.find("a", {"class": "govuk-back-link"})["href"] == application_url

    # form exists
    assert soup.find("input", {"id": "id_recommendation_1"})
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Submit feedback"
    assert soup.find("a", {"class": "govuk-button--secondary"})["href"] == reverse("core:home")


def test_post_survey_feedback(authorized_client, hcsat_url, application_pk, survey_id):
    response = authorized_client.post(hcsat_url, data={"recommendation": "NEUTRAL"})
    assert response.status_code == 302
    assert response.url == reverse("core:home")


def test_post_survey_feedback_invalid(authorized_client, hcsat_url):
    response = authorized_client.post(hcsat_url, data={})
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("span", {"class": "govuk-error-message"}).text.strip() == "Error: Star rating is required"
