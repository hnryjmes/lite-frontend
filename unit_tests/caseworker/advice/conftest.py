import pytest

from caseworker.advice.services import LICENSING_UNIT_TEAM


@pytest.fixture
def with_lu_countersigning_enabled(settings):
    settings.FEATURE_LU_POST_CIRC_COUNTERSIGNING = True


@pytest.fixture
def with_lu_countersigning_disabled(settings):
    settings.FEATURE_LU_POST_CIRC_COUNTERSIGNING = False


@pytest.fixture
def consolidated_advice(current_user, team1_user):
    current_user["team"]["id"] = "2132131d-2432-423424"
    current_user["team"]["alias"] = LICENSING_UNIT_TEAM
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
            "third_party": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
            "countersigned_by": None,
            "countersign_comments": "",
        },
        {
            "id": "2f580ac6-07ec-46f0-836c-0bbb282e6886",
            "text": "Issue from LU",
            "note": "",
            "type": {"key": "no_licence_required", "value": "No Licence Required"},
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


@pytest.fixture
def advice_for_lu_countersign(consolidated_advice, LU_team_user):
    final_advice = [item for item in consolidated_advice if item["level"] == "final"]
    for item in final_advice:
        item["user"] = LU_team_user

    return final_advice
