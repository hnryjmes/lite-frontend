import pytest

from pytest_django.asserts import assertTemplateUsed
from urllib import parse

from django.urls import reverse

from caseworker.queues.views.forms import CasesFiltersForm


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_countries,
    mock_control_list_entries,
    mock_regime_entries,
):
    pass


@pytest.mark.parametrize(
    "filters_data",
    [
        ({"params": {"case_type": "siel", "status": "finalised"}}),
        ({"params": {"case_reference": "GBSIEL/2022", "status": "finalised"}}),
        ({"params": {"case_reference": "GBSIEL/2022", "flags": ["1", "2"]}}),
        ({"params": {"case_type": "siel", "country": "JP"}}),
        (
            {
                "field": "submitted_from",
                "params": {"submitted_from_0": "1", "submitted_from_1": "1", "submitted_from_2": "2022"},
            }
        ),
        ({"field": "submitted_to", "params": {"submitted_to_0": "1", "submitted_to_1": "1", "submitted_to_2": "2022"}}),
        (
            {
                "field": "finalised_from",
                "params": {"finalised_from_0": "1", "finalised_from_1": "1", "finalised_from_2": "2022"},
            }
        ),
        ({"field": "finalised_to", "params": {"finalised_to_0": "1", "finalised_to_1": "1", "finalised_to_2": "2022"}}),
        ({"params": {"export_type": "permanent", "assigned_queues": "fake-queue-id-1"}}),
        ({"params": {"case_type": "siel", "sub_status": "inform_letter_sent"}}),
    ],
)
def test_case_filters(
    authorized_client,
    requests_mock,
    mock_queues_list,
    mock_cases,
    mock_cases_head,
    filters_data,
    mock_no_bookmarks,
):
    url = reverse("core:index", kwargs={"disable_queue_lookup": True})
    query_params = f"{parse.urlencode(filters_data['params'], doseq=True)}"
    url = f"{url}?{query_params}"
    response = authorized_client.get(url)
    assertTemplateUsed(response, "queues/cases.html")
    assert isinstance(response.context["form"], CasesFiltersForm)

    case_search_request = mock_cases.request_history[0]
    assert query_params in case_search_request.url
    if filters_data.get("field"):
        key = filters_data["field"]
        # The DateInputField that we use in the form is a GDS component which shows it in a
        # decomposed manner (day, month, year as 3-tuple).
        # So if the field is 'submitted_from', it is decomposed as 'submitted_from_{0..2}'
        # When we perform the search, these are converted to day, month, year as expected by
        # the API hence assert that these parameters are also present in the query string
        date_params = {
            f"{key}_day": filters_data["params"][f"{key}_0"],
            f"{key}_month": filters_data["params"][f"{key}_1"],
            f"{key}_year": filters_data["params"][f"{key}_2"],
        }
        date_params = f"{parse.urlencode(date_params)}"
        assert parse.unquote(date_params) in case_search_request.url


def test_countries_get(authorized_client):
    url = reverse("api:countries")
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_regime_entries_get(authorized_client):
    url = reverse("api:regime-entries")
    response = authorized_client.get(url)
    assert response.status_code == 200
