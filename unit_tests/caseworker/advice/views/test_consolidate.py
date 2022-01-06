import pytest

from bs4 import BeautifulSoup
from django.urls import reverse
from caseworker.advice import services

from core import client
from caseworker.advice import forms
from caseworker.advice.services import LICENSING_UNIT_TEAM


@pytest.fixture
def mock_post_team_advice(requests_mock, standard_case_pk):
    url = client._build_absolute_uri(f"/cases/{standard_case_pk}/team-advice/")
    yield requests_mock.post(url=url, json={})


@pytest.fixture(autouse=True)
def setup(mock_queue, mock_case, mock_denial_reasons, mock_post_team_advice):
    yield


@pytest.fixture
def url(data_queue, data_standard_case):
    return reverse(
        "cases:consolidate_review", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def view_consolidate_outcome_url(data_queue, data_standard_case):
    return reverse(
        f"cases:consolidate_view", kwargs={"queue_pk": data_queue["id"], "pk": data_standard_case["case"]["id"]}
    )


@pytest.fixture
def advice(current_user):
    return [
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "country": None,
            "created_at": "2021-10-16T23:48:39.486679+01:00",
            "denial_reasons": [],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote": "footnotes",
            "good": good_id,
            "id": "429c5596-fe8b-4540-988b-c37805cd08de",
            "level": "user",
            "note": "additional notes",
            "proviso": "no conditions",
            "text": "meets the criteria",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": {"key": "approve", "value": "Approve"},
            "ultimate_end_user": None,
            "user": current_user,
        }
        for good_id in ("0bedd1c3-cf97-4aad-b711-d5c9a9f4586e", "6daad1c3-cf97-4aad-b711-d5c9a9f4586e")
    ]


@pytest.fixture
def consolidated_advice(current_user, team1_user):
    current_user["team"]["id"] = LICENSING_UNIT_TEAM
    return [
        {
            "id": "4f146dd1-a454-49ad-8c78-214552a45207",
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "proviso": None,
            "denial_reasons": [],
            "footnote": "firearms product for military use",
            "user": team1_user,
            "created_at": "2021-12-14T13:36:34.176613Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": "94540537-d5e9-40c9-9d8e-8e28792665e1",
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "ac914a37-ae50-4a8e-8ebb-0c31b98cfbd2",
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "proviso": None,
            "denial_reasons": [],
            "footnote": "firearms product for military use",
            "user": team1_user,
            "created_at": "2021-12-14T13:36:34.222814Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": "09d08d89-f2f4-4203-a465-11e7c597191c",
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "deb3e4f7-3704-4dad-aaa5-855a076bb16f",
            "text": "Issue from Team M",
            "note": "No additional instructions",
            "type": {"key": "approve", "value": "Approve"},
            "level": "user",
            "proviso": None,
            "denial_reasons": [],
            "footnote": "firearms product for military use",
            "user": team1_user,
            "created_at": "2021-12-14T13:36:34.262769Z",
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "56a3062a-6437-4e4f-8ce8-87ad76d5d903",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.082345Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": "94540537-d5e9-40c9-9d8e-8e28792665e1",
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "cdf5ac6d-f209-48c9-a6cd-6f7b8496f810",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.123966Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": "09d08d89-f2f4-4203-a465-11e7c597191c",
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "final",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.161135Z",
            "good": "21f9f169-606d-40a6-91b4-88652d64167e",
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": "09d08d89-f2f4-4203-a465-11e7c597191c",
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "proviso", "value": "Proviso"},
            "level": "team",
            "proviso": "no other conditions",
            "denial_reasons": [],
            "footnote": "",
            "user": current_user,
            "created_at": "2021-12-14T14:26:36.161135Z",
            "good": None,
            "goods_type": None,
            "country": None,
            "end_user": None,
            "ultimate_end_user": None,
            "consignee": None,
            "third_party": None,
            "countersigned_by": None,
            "countersign_comments": "",
        },
    ]


def to_refusal_advice(advice):
    for item in advice:
        item["type"] = {"key": "refuse", "value": "Refuse"}
        item["denial_reasons"] = (["5a", "5b"],)
    return advice


@pytest.fixture
def refusal_advice(advice):
    return to_refusal_advice(advice)


@pytest.fixture
def consolidated_refusal_outcome(consolidated_advice):
    return to_refusal_advice(consolidated_advice)


@pytest.mark.parametrize(
    "path, form_class",
    (
        ("", forms.ConsolidateApprovalForm),
        ("approve/", forms.ConsolidateApprovalForm),
        ("refuse/", forms.RefusalAdviceForm),
    ),
)
def test_consolidate_review(requests_mock, authorized_client, data_standard_case, url, advice, path, form_class):
    data_standard_case["case"]["advice"] = advice
    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json={
            "user": {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "team": {"id": LICENSING_UNIT_TEAM, "name": "Licensing Unit"},
            }
        },
    )
    response = authorized_client.get(url + path)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, form_class)


@pytest.mark.parametrize("recommendation, redirect", [("approve", "approve"), ("refuse", "refuse")])
def test_consolidate_review_refusal_advice(
    requests_mock, authorized_client, data_standard_case, url, refusal_advice, recommendation, redirect
):
    data_standard_case["case"]["advice"] = refusal_advice
    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json={
            "user": {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "team": {"id": LICENSING_UNIT_TEAM, "name": "Licensing Unit"},
            }
        },
    )
    response = authorized_client.get(url)
    assert response.status_code == 200
    form = response.context["form"]
    assert isinstance(form, forms.ConsolidateSelectAdviceForm)
    response = authorized_client.post(url, data={"recommendation": recommendation})
    assert response.status_code == 302
    assert redirect in response.url


def test_consolidate_review_approve(requests_mock, authorized_client, data_standard_case, url, advice):
    data_standard_case["case"]["advice"] = advice
    data = {"approval_reasons": "test", "countries": ["GB"]}
    response = authorized_client.post(url + "approve/", data=data)
    assert response.status_code == 302
    request = requests_mock.request_history.pop()
    assert request.method == "POST"
    assert "team-advice" in request.url
    assert request.json() == [
        {
            "type": "approve",
            "text": "test",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "test",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": [],
        },
        {
            "type": "approve",
            "text": "test",
            "proviso": "",
            "note": "",
            "footnote_required": False,
            "footnote": "",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "denial_reasons": [],
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
        {
            "denial_reasons": [],
            "footnote": "",
            "footnote_required": False,
            "good": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
            "note": "",
            "proviso": "",
            "text": "",
            "type": "no_licence_required",
        },
    ]


def test_consolidate_review_refuse(requests_mock, authorized_client, data_standard_case, url, advice):
    data_standard_case["case"]["advice"] = advice
    data = {"denial_reasons": ["1"], "refusal_reasons": "test", "countries": ["GB"]}
    response = authorized_client.post(url + "refuse/", data=data)
    assert response.status_code == 302
    request = requests_mock.request_history.pop()
    assert request.method == "POST"
    assert "team-advice" in request.url
    assert request.json() == [
        {
            "denial_reasons": ["1"],
            "end_user": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
            "footnote_required": False,
            "text": "test",
            "type": "refuse",
        },
        {
            "consignee": "cd2263b4-a427-4f14-8552-505e1d192bb8",
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "type": "refuse",
        },
        {
            "denial_reasons": ["1"],
            "footnote_required": False,
            "text": "test",
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "type": "refuse",
        },
    ]


def test_view_consolidate_approve_outcome(
    requests_mock, authorized_client, data_standard_case, view_consolidate_outcome_url, consolidated_advice
):
    data_standard_case["case"]["advice"] = consolidated_advice
    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json={
            "user": {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "team": {"id": LICENSING_UNIT_TEAM, "name": "Licensing Unit"},
            }
        },
    )
    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="table-licenceable-products")
    assert [th.text for th in table.find_all("th")] == ["Country", "Type", "Name", "Approved products"]
    assert [td.text for td in table.find_all("td")] == [
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "All",
        "United Kingdom",
        "End user",
        "End User",
        "All",
        "United Kingdom",
        "Third party",
        "Third party",
        "All",
    ]


def test_view_consolidate_refuse_outcome(
    requests_mock, authorized_client, data_standard_case, view_consolidate_outcome_url, consolidated_refusal_outcome
):
    data_standard_case["case"]["advice"] = consolidated_refusal_outcome
    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json={
            "user": {
                "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                "team": {"id": LICENSING_UNIT_TEAM, "name": "Licensing Unit"},
            }
        },
    )
    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    table = soup.find("table", id="table-licenceable-products")
    assert [th.text for th in table.find_all("th")] == [
        "Country",
        "Type",
        "Name",
        "Refused products",
        "Refusal criteria",
    ]
    assert [td.text for td in table.find_all("td")] == [
        "Abu Dhabi",
        "Consignee",
        "Consignee",
        "All",
        "['5a', '5b']",
        "United Kingdom",
        "End user",
        "End User",
        "All",
        "['5a', '5b']",
        "United Kingdom",
        "Third party",
        "Third party",
        "All",
        "['5a', '5b']",
    ]


@pytest.mark.parametrize(
    "path, form_class",
    (
        ("", forms.ConsolidateApprovalForm),
        ("approve/", forms.ConsolidateApprovalForm),
        ("refuse/", forms.RefusalAdviceForm),
    ),
)
def test_consolidate_raises_exception_for_other_team(
    authorized_client, data_standard_case, url, advice, path, form_class
):
    data_standard_case["case"]["advice"] = advice

    with pytest.raises(Exception) as err:
        authorized_client.get(url + path)

    assert str(err.value) == "Consolidate/combine operation not allowed for team 00000000-0000-0000-0000-000000000001"


@pytest.mark.parametrize(
    "team_id, team_name", ((services.LICENSING_UNIT_TEAM, "LU Team"), (services.MOD_ECJU_TEAM, "MoD Team"),),
)
def test_view_consolidate_approve_outcome_countersign_warning_message(
    requests_mock,
    authorized_client,
    data_standard_case,
    view_consolidate_outcome_url,
    consolidated_advice,
    team_id,
    team_name,
):
    data_standard_case["case"]["advice"] = consolidated_advice
    data_standard_case["case"]["all_flags"] = [
        {
            "colour": "default",
            "id": "318d9c76-f772-4517-bda8-296cdf3191c0",
            "label": "",
            "level": "Good",
            "name": "Small Arms",
            "priority": 0,
        },
        {
            "colour": "default",
            "id": "bbf29b42-0aae-4ebc-b77a-e502ddea30a8",
            "label": "",
            "level": "Destination",
            "name": "LU Countersign Required",
            "priority": 0,
        },
        {
            "colour": "default",
            "id": "a7736911-f604-4256-b109-dadd2f6bc316",
            "label": "",
            "level": "Destination",
            "name": "Green Countries",
            "priority": 20,
        },
        {
            "colour": "default",
            "id": "00000000-0000-0000-0000-000000000007",
            "label": None,
            "level": "Case",
            "name": "Firearms",
            "priority": 0,
        },
    ]

    requests_mock.get(
        client._build_absolute_uri("/gov-users/2a43805b-c082-47e7-9188-c8b3e1a83cb0"),
        json={"user": {"id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0", "team": {"id": team_id, "name": team_name},}},
    )

    response = authorized_client.get(view_consolidate_outcome_url)
    assert response.status_code == 200

    if team_id == services.LICENSING_UNIT_TEAM:
        assert response.context["lu_countersign_required"] == True
        assert response.context["finalise_case"] == False
    else:
        assert response.context["lu_countersign_required"] == False
        assert response.context["finalise_case"] == False