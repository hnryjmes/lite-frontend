import pytest
import re

from bs4 import BeautifulSoup

from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case):
    pass


@pytest.fixture(autouse=True)
def mock_application_good_documents(data_standard_case, requests_mock):
    requests_mock.get(
        re.compile(
            rf"/applications/{data_standard_case['case']['id']}/goods/[0-9a-fA-F-]+/documents/",
        ),
        json={"documents": []},
    )


@pytest.fixture(autouse=True)
def mock_mtcr_entries_get(requests_mock):
    requests_mock.get(
        "/static/regimes/mtcr/entries/",
        json={"entries": [("MTCR1", "mtcr1-value")]},
    )


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:tau:edit",
        kwargs={
            "queue_pk": data_queue["id"],
            "pk": data_standard_case["case"]["id"],
            "good_id": data_standard_case["case"]["data"]["goods"][1]["id"],
        },
    )


@pytest.fixture
def mock_cle_post(requests_mock, data_standard_case):
    yield requests_mock.post(
        client._build_absolute_uri(f"/goods/control-list-entries/{data_standard_case['case']['id']}"), json={}
    )


def get_cells(soup, table_id):
    return [td.text for td in soup.find(id=table_id).find_all("td")]


def test_tau_edit_auth(authorized_client, url, mock_control_list_entries, mock_precedents_api):
    """GET edit should return 200 with an authorised client"""
    response = authorized_client.get(url)
    assert response.status_code == 200


def test_tau_home_noauth(client, url):
    """GET edit should return 302 with an unauthorised client"""
    response = client.get(url)
    assert response.status_code == 302


def test_form(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_control_list_entries,
    mock_precedents_api,
):
    """
    Tests the submission of a valid form only. More tests on the form itself are in test_forms.py
    """
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]
    # Get the edit form
    response = authorized_client.get(url)
    soup = BeautifulSoup(response.content, "html.parser")

    # Check if the form fields contain sane values
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    # Check control list entries
    edit_good_cle = [cle["rating"] for cle in edit_good["control_list_entries"]]
    form_cle = [cle.attrs["value"] for cle in soup.find("form").find_all("option") if "selected" in cle.attrs]
    assert edit_good_cle == form_cle
    # Check report summary
    assert edit_good["report_summary"] == soup.find("form").find(id="report_summary").attrs["value"]
    # Check comments
    assert edit_good["comment"] == soup.find("form").find(id="id_comment").text.strip()

    response = authorized_client.post(
        url, data={"report_summary": "test", "does_not_have_control_list_entries": True, "comment": "test"}
    )

    # Check response and API payload
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary": "test",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "regime_entries": [],
    }


@pytest.mark.parametrize(
    "regimes_form_data, regime_entries",
    (
        ({}, []),
        ({"regimes": ["MTCR"], "mtcr_entries": ["MTCR1"]}, ["MTCR1"]),
    ),
)
def test_form_regime_entries(
    authorized_client,
    url,
    data_standard_case,
    requests_mock,
    mock_cle_post,
    mock_control_list_entries,
    mock_precedents_api,
    regimes_form_data,
    regime_entries,
):
    # Remove assessment from a good
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    edit_good = data_standard_case["case"]["data"]["goods"][1]
    edit_good["control_list_entries"] = [{"rating": "ML1"}, {"rating": "ML1a"}]

    response = authorized_client.post(
        url,
        data={
            "report_summary": "test",
            "does_not_have_control_list_entries": True,
            "comment": "test",
            **regimes_form_data,
        },
    )

    # Check response and API payload
    assert response.status_code == 302
    assert requests_mock.last_request.json() == {
        "control_list_entries": [],
        "report_summary": "test",
        "comment": "test",
        "current_object": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
        "objects": ["6a7fc61f-698b-46b6-9876-6ac0fddfb1a2"],
        "is_good_controlled": False,
        "regime_entries": regime_entries,
    }


def test_control_list_suggestions_json(
    authorized_client,
    url,
    mock_control_list_entries,
    mock_precedents_api,
    mocker,
    data_standard_case,
):
    good = data_standard_case["case"]["data"]["goods"][0]
    good["is_good_controlled"] = None
    good["control_list_entries"] = []
    good["firearm_details"]["year_of_manufacture"] = "1930"

    mock_get_cle_suggestions_json = mocker.patch("caseworker.tau.views.get_cle_suggestions_json")
    mock_get_cle_suggestions_json.return_value = {"mock": "suggestion"}

    response = authorized_client.get(url)
    assert response.context["cle_suggestions_json"] == {"mock": "suggestion"}
