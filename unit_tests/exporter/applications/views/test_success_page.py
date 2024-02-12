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
def success_url(application_pk):
    return reverse("applications:success_page", kwargs={"pk": application_pk})


@pytest.fixture
def application_pk(data_standard_case):
    return data_standard_case["case"]["data"]["id"]


@pytest.fixture
def survey_id():
    return "6de657c9-e500-4791-8c8b-9f94dec2c629"  # /PS-IGNORE


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
def mock_post_survey(requests_mock, survey_id):
    survey_url = client._build_absolute_uri(f"/survey/")
    return requests_mock.post(
        survey_url,
        json={"id": survey_id},
        status_code=201,
    )


@pytest.fixture(autouse=True)
def mock_get_application(requests_mock, application_pk, application_reference_number):
    return requests_mock.get(
        client._build_absolute_uri(f"/applications/{application_pk}"),
        json={"id": application_pk, "reference_code": application_reference_number, "status": "submitted"},
        status_code=200,
    )


def test_success_view(
    authorized_client, success_url, application_reference_number, application_url, home_url, application_start_url
):
    response = authorized_client.get(success_url)

    assert response.status_code == 200

    assert isinstance(response.context["form"], HCSATminiform)
    assertTemplateUsed(response, "applications/application-submit-success.html")

    soup = BeautifulSoup(response.content, "html.parser")

    # content
    assert soup.find("h1").string.strip() == "Application submitted"
    assert soup.find("a", {"class": "govuk-back-link"})["href"] == application_url
    assert (
        soup.find("div", {"id": "application-processing-message-value"}).string.strip()
        == "ECJU reference: " + application_reference_number
    )

    # links
    links = soup.findAll("a", {"class": "success-navigation"})
    assert links[0]["href"] == reverse("applications:applications")
    assert links[1]["href"] == application_start_url
    assert links[2]["href"] == home_url

    # form exists
    assert soup.find("input", {"id": "id_recommendation_1"})
    assert soup.find("input", {"id": "submit-id-submit"})["value"] == "Submit feedback"
    # assert soup.find("a", {"id": "cancel-id-cancel"})["href"] == application_url


def test_post_survey_feedback(authorized_client, success_url, application_pk, survey_id):
    response = authorized_client.post(success_url, data={"recommendation": "NEUTRAL"})
    assert response.status_code == 302
    assert response.url == reverse("applications:application-hcsat", kwargs={"pk": application_pk, "sid": survey_id})


def test_post_survey_feedback_invalid(authorized_client, success_url):
    response = authorized_client.post(success_url, data={})
    assert response.status_code == 200
    soup = BeautifulSoup(response.content, "html.parser")
    assert soup.find("span", {"class": "govuk-error-message"}).text.strip() == "Error: Star rating is required"
