import pytest

from pytest_django.asserts import assertTemplateUsed
from django.urls import reverse


@pytest.fixture(autouse=True)
def default_feature_flags(settings):
    settings.FEATURE_FLAG_NON_FIREARMS_COMPONENT_ENABLED = True


@pytest.fixture
def good(data_standard_case):
    return data_standard_case["case"]["data"]["goods"][0]


def test_component_summary_response_status_code(
    authorized_client,
    mock_application_get,
    mock_good_get,
    component_product_summary_url,
):
    response = authorized_client.get(component_product_summary_url)
    assert response.status_code == 200


def test_component_summary_template_used(
    authorized_client,
    mock_application_get,
    mock_good_get,
    component_product_summary_url,
):
    response = authorized_client.get(component_product_summary_url)
    assertTemplateUsed(response, "applications/goods/component/product-summary.html")


def test_component_product_summary_context(
    authorized_client,
    mock_application_get,
    mock_good_get,
    component_product_summary_url,
    component_summary,
    data_standard_case,
    good_id,
):
    response = authorized_client.get(component_product_summary_url)

    def _get_test_url(name):
        if not name:
            return None
        return f'/applications/{data_standard_case["case"]["id"]}/goods/{good_id}/component/edit/{name}/'

    url_map = {
        "name": "name",
        "is-good-controlled": "control-list-entries",
        "control-list-entries": "control-list-entries",
        "is-component": "component-details",
        "component-type": "component-details",
        "modified-details": "component-details",
        "part-number": "part-number",
        "is-pv-graded": "pv-grading",
        "pv-grading-prefix": "pv-grading-details",
        "pv-grading-grading": "pv-grading-details",
        "pv-grading-suffix": "pv-grading-details",
        "pv-grading-issuing-authority": "pv-grading-details",
        "pv-grading-details-reference": "pv-grading-details",
        "pv-grading-details-date-of-issue": "pv-grading-details",
        "uses-information-security": "uses-information-security",
        "uses-information-security-details": "uses-information-security",
        "has-product-document": "product-document-availability",
        "is-document-sensitive": "product-document-sensitivity",
        "product-document": "product-document",
        "product-document-description": "product-document",
        "military-use": "military-use",
    }

    summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None))) for key, value, label in component_summary
    )
    assert response.context["summary"] == summary_with_links


def test_component_product_on_application_summary_response_status_code(
    authorized_client,
    component_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good_id,
    requests_mock,
):

    response = authorized_client.get(component_on_application_summary_url)
    assert response.status_code == 200


@pytest.fixture
def component_on_application_summary():
    return (
        ("is-onward-exported", "Yes", "Will the product be onward exported to any additional countries?"),
        ("is-altered", "Yes", "Will the item be altered or processed before it is exported again?"),
        ("is-altered-comments", "I will alter it real good", "Explain how the product will be processed or altered"),
        ("is-incorporated", "Yes", "Will the product be incorporated into another item before it is onward exported?"),
        (
            "is-incorporated-comments",
            "I will onward incorporate",
            "Describe what you are incorporating the product into",
        ),
        ("number-of-items", "3", "Number of items"),
        ("total-value", "£16.32", "Total value"),
    )


def test_component_on_application_summary_context(
    authorized_client,
    component_on_application_summary_url,
    mock_application_get,
    mock_good_get,
    mock_good_on_application_get,
    application,
    good,
    good_on_application,
    requests_mock,
    component_summary,
    component_on_application_summary,
):

    response = authorized_client.get(component_on_application_summary_url)
    context = response.context

    def _get_test_url(name):
        if not name:
            return None
        return f"/applications/{application['id']}/goods/component/{good_on_application['id']}/component-on-application-summary/edit/{name}/"

    url_map = {
        "is-onward-exported": "onward-exported",
        "is-altered": "onward-altered",
        "is-altered-comments": "onward-altered",
        "is-incorporated": "onward-incorporated",
        "is-incorporated-comments": "onward-incorporated",
        "number-of-items": "quantity-value",
        "total-value": "quantity-value",
    }

    component_on_application_summary_with_links = tuple(
        (key, value, label, _get_test_url(url_map.get(key, None)))
        for key, value, label in component_on_application_summary
    )

    assert context["application"] == application
    assert context["good"] == good["good"]
    assert context["good_on_application"] == good_on_application
    assert context["product_summary"] == component_summary
    assert context["product_on_application_summary"] == component_on_application_summary_with_links