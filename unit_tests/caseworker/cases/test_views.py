from copy import deepcopy
from bs4 import BeautifulSoup

from django.urls import reverse

import pytest

from core import client


approve = {"key": "approve", "value": "Approve"}
proviso = {"key": "proviso", "value": "Approve with proviso"}
refuse = {"key": "refuse", "value": "Refuse"}
conflicting = {"key": "conflicting", "value": "Conflicting"}

john_smith = {
    "email": "john.smith@example.com",
    "first_name": "John",
    "id": "63c74ddd-c119-48cc-8696-d196218ca583",
    "last_name": "Smith",
    "role_name": "Super User",
    "status": "Active",
    "team": {"id": "136cbb1f-390b-4f78-bfca-86300edec300", "name": "team1", "part_of_ecju": None},
}


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_case_activity_system_user,
    mock_case,
    mock_control_list_entries,
    mock_application_search,
    mock_good_on_appplication,
    mock_good_on_appplication_documents,
):
    yield


def test_case_audit_trail_system_user(authorized_client, open_case_pk, queue_pk):
    # given the case has activity from system user
    url = reverse("cases:case", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    # when the case is viewed
    response = authorized_client.get(url)

    # then it does not error
    assert response.status_code == 200


good_review_parametrize_data = (
    # all field present, nothing special
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
            "is_precedent": False,
        },
    ),
    # multiple control list entries
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a", "ML1"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a", "ML1"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # no comment
    (
        {
            "comment": "",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # not controlled and no control list entries
    (
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "does_not_have_control_list_entries": True,
            "is_good_controlled": False,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "is_good_controlled": False,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # is controlled but no control list entries
    (
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "does_not_have_control_list_entries": True,
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
        {
            "comment": "Some comment",
            "control_list_entries": [],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": [],
            "is_precedent": False,
        },
    ),
    # backwards compat, if API is not sending is_precedent
    (
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
        },
        {
            "comment": "Some comment",
            "control_list_entries": ["ML1a"],
            "is_good_controlled": True,
            "report_summary": "some-report-summary-id",
            "end_use_control": ["MEND", "MEND1"],
            "is_precedent": False,
        },
    ),
)


@pytest.mark.parametrize("data,expected", good_review_parametrize_data)
def test_standard_review_goods(
    authorized_client,
    requests_mock,
    standard_case_pk,
    queue_pk,
    data,
    expected,
    data_standard_case,
    mock_product_more_like_this,
):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{standard_case_pk}/", json={})
    good_pk = data_standard_case["case"]["data"]["goods"][0]["good"]["id"]
    good_on_application_pk = data_standard_case["case"]["data"]["goods"][0]["id"]

    step_data = build_wizard_step_data(
        view_name="review_standard_application_good_wizard_view", step_name=good_pk, data=data,
    )
    url = reverse("cases:review_standard_application_goods", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk})

    response = authorized_client.get(f"{url}?goods={good_pk}")

    assert response.status_code == 200

    response = authorized_client.post(f"{url}?goods={good_pk}", step_data)

    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected, "objects": [good_pk]}

    assert good_on_application_pk in mock_product_more_like_this.request_history[0].url


@pytest.mark.parametrize("data,expected", good_review_parametrize_data)
def test_open_review_goods(
    authorized_client,
    requests_mock,
    open_case_pk,
    queue_pk,
    data,
    expected,
    data_open_case,
    mock_product_more_like_this,
):
    requests_mock_instance = requests_mock.post(f"/goods/control-list-entries/{open_case_pk}/", json={})
    good_pk = data_open_case["case"]["data"]["goods_types"][0]["id"]
    step_data = build_wizard_step_data(
        view_name="review_open_application_good_wizard_view", step_name=good_pk, data=data,
    )
    url = reverse("cases:review_open_application_goods", kwargs={"queue_pk": queue_pk, "pk": open_case_pk})

    response = authorized_client.get(f"{url}?goods_types={good_pk}")

    assert response.status_code == 200

    response = authorized_client.post(f"{url}?goods_types={good_pk}", step_data)

    assert response.status_code == 302
    assert requests_mock_instance.call_count == 1
    assert requests_mock_instance.request_history[0].json() == {**expected, "objects": [good_pk]}
    assert good_pk in mock_product_more_like_this.request_history[0].url


def build_wizard_step_data(view_name, step_name, data):
    step_data = {f"{view_name}-current_step": step_name}
    step_data.update({f"{step_name}-{key}": value for key, value in data.items()})
    return step_data


def test_good_on_application_detail(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_search,
    data_good_on_application,
    data_standard_case,
):
    # given I access good on application details for a good with control list entries and a part number
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same part number and control list entries
    assert mock_application_search.request_history[0].qs == {"part": ["44"], "clc_rating": ["ml1", "ml2"]}
    # and the view exposes the data that the template needs
    assert response.context_data["good_on_application"] == data_good_on_application
    assert response.context_data["other_cases"] == data_search
    assert response.context_data["case"] == data_standard_case["case"]
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'part:"44" clc_rating:"ML1" clc_rating:"ML2"'


def test_good_on_application_detail_no_part_number(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    # given I access good on application details for a good with control list entries but no part number
    data_good_on_application["good"]["part_number"] = ""
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same control list entries
    assert mock_application_search.request_history[0].qs == {"clc_rating": ["ml1", "ml2"]}
    # and the form is pre-populated with the part number and control list entries
    assert response.context_data["form"]["search_string"].initial == 'clc_rating:"ML1" clc_rating:"ML2"'


def test_good_on_application_detail_no_part_number_no_control_list_entries(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    # given I access good on application details for a good with neither part number of control list entries
    data_good_on_application["good"]["part_number"] = ""
    data_good_on_application["control_list_entries"] = []
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is not requested
    assert len(mock_application_search.request_history) == 0
    # and the form is left blank
    assert response.context_data["form"]["search_string"].initial == ""


def test_good_on_application_detail_not_rated_at_application_level(
    authorized_client,
    mock_application_search,
    queue_pk,
    standard_case_pk,
    good_on_application_pk,
    data_good_on_application,
):
    # given I access good on application details for a good that has not been rated at application level
    data_good_on_application["control_list_entries"] = []
    data_good_on_application["good"]["part_number"] = ""
    data_good_on_application["good"]["control_list_entries"] = ({"rating": "ML1", "text": "Smooth-bore..."},)
    url = reverse(
        "cases:good", kwargs={"queue_pk": queue_pk, "pk": standard_case_pk, "good_pk": good_on_application_pk}
    )
    response = authorized_client.get(url)

    assert response.status_code == 200
    # then the search endpoint is requested for cases with goods with the same control list entries as canonical good
    assert mock_application_search.request_history[0].qs == {"clc_rating": ["ml1"]}
    # and the form is pre-populated with the canonical good control list entries
    assert response.context_data["form"]["search_string"].initial == 'clc_rating:"ML1"'


def test_search_denials(authorized_client, data_standard_case, requests_mock, queue_pk, standard_case_pk):
    end_user_id = data_standard_case["case"]["data"]["end_user"]["id"]
    end_user_name = data_standard_case["case"]["data"]["end_user"]["name"]
    end_user_address = data_standard_case["case"]["data"]["end_user"]["address"]

    requests_mock.get(
        client._build_absolute_uri(f"/external-data/denial-search/?search={end_user_name}&search={end_user_address}"),
        json={"hits": {"hits": []}},
    )

    url = reverse("cases:denials", kwargs={"pk": standard_case_pk, "queue_pk": queue_pk})

    response = authorized_client.get(f"{url}?end_user={end_user_id}")

    assert response.status_code == 200


@pytest.mark.parametrize(
    "product_1_advice,product_2_advice,end_user_advice,can_finalise,show_warning",
    (
        (
            [approve, refuse], refuse, approve, False, True
        ),
        (
            [approve, proviso], refuse, approve, True, False
        ),
        (
            [approve, refuse], approve, approve, False, True
        ),
    ),
)
def test_case_conflicting_advice(
    product_1_advice,
    product_2_advice,
    end_user_advice,
    can_finalise,
    show_warning,
    requests_mock,
    authorized_client,
    queue_pk,
    mock_all_standard_case_data,
    data_standard_case,
):
    url = reverse(
        "cases:case", kwargs={"queue_pk": queue_pk, "pk": data_standard_case["case"]["id"], "tab": "final-advice"}
    )

    blocking_flags_url = client._build_absolute_uri("/flags/")
    requests_mock.get(url=blocking_flags_url, json=[])

    mock_case = {**data_standard_case}

    product_1_id = "8b730c06-ab4e-401c-aeb0-32b3c92e912c"
    product_2_id = "880178cd-83ec-4773-8829-c19065912565"
    end_user_id = "95d3ea36-6ab9-41ea-a744-7284d17b9cc5"

    product_2 = deepcopy(mock_case["case"]["data"]["goods"][0])
    product_2["good"]["id"] = product_2_id
    product_2["good"]["id"] = product_2_id
    mock_case["case"]["data"]["goods"].append(product_2)

    product_1_advice_1 = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "text": "",
        "note": "",
        "type": product_1_advice[0],
        "level": "final",
        "proviso": None,
        "denial_reasons": [],
        "footnote": None,
        "user": john_smith,
        "created_at": "2021-03-18T11:27:56.625251Z",
        "good": product_1_id,
        "goods_type": None,
        "country": None,
        "end_user": None,
        "ultimate_end_user": None,
        "consignee": None,
        "third_party": None,
    }
    product_1_advice_2 = {**product_1_advice_1}
    product_1_advice_2["type"] = product_1_advice[1]

    product_2_advice = {
        "id": "8993476f-9849-49d1-973e-62b185085a64",
        "text": "",
        "note": "",
        "type": product_2_advice,
        "level": "final",
        "proviso": None,
        "denial_reasons": [],
        "footnote": None,
        "user": john_smith,
        "created_at": "2021-03-18T11:27:56.625251Z",
        "good": product_2_id,
        "goods_type": None,
        "country": None,
        "end_user": None,
        "ultimate_end_user": None,
        "consignee": None,
        "third_party": None,
    }
    end_user_advice = {
        "id": "0093476f-9849-49d1-973e-62b185085a64",
        "text": "",
        "note": "",
        "type": end_user_advice,
        "level": "final",
        "proviso": None,
        "denial_reasons": [],
        "footnote": None,
        "user": john_smith,
        "created_at": "2021-03-18T11:27:56.625251Z",
        "good": None,
        "goods_type": None,
        "country": None,
        "end_user": end_user_id,
        "ultimate_end_user": None,
        "consignee": None,
        "third_party": None,
    }

    mock_case["case"]["advice"] = [product_1_advice_1, product_1_advice_2, product_2_advice, end_user_advice]

    requests_mock.get(url=url, json=mock_case)

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")

    if can_finalise:
        assert "app-advice__disabled-buttons" not in soup.find(id="button-finalise").parent["class"]
    else:
        assert "app-advice__disabled-buttons" in soup.find(id="button-finalise").parent["class"]

    if show_warning:
        assert "This application contains conflicting advice and cannot be finalised." in str(response.content)
    else:
        assert "This application contains conflicting advice and cannot be finalised." not in str(response.content)
