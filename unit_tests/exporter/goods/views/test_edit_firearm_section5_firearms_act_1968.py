import datetime
import pytest

from django.conf import settings
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmSteps
from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmSection5Form,
)


@pytest.fixture(autouse=True)
def setup(mock_good_get, no_op_storage):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def edit_url(firearm_good):
    return reverse(
        "goods:firearm_edit_section_5_firearms_act_1968",
        kwargs={"pk": firearm_good["id"]},
    )


@pytest.fixture
def goto_step(goto_step_factory, edit_url):
    return goto_step_factory(edit_url)


@pytest.fixture
def post_to_step(post_to_step_factory, edit_url):
    return post_to_step_factory(edit_url)


def test_edit_firearm_section_5_firearms_act_set_yes_without_document(
    authorized_client,
    requests_mock,
    data_organisation,
    mock_good_put,
    post_to_step,
    edit_url,
    product_detail_url,
):
    post_organisation_document_matcher = requests_mock.post(
        f"/organisations/{data_organisation['id']}/documents/",
        status_code=201,
        json={},
    )

    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "yes",
        },
    )
    assert isinstance(response.context["form"], FirearmAttachSection5LetterOfAuthorityForm)

    section_5_letter_expiry_date = datetime.date.today() + datetime.timedelta(days=10)
    response = post_to_step(
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
        {
            "file": SimpleUploadedFile("letter_of_authority.pdf", b"This is the letter of authority"),
            "section_certificate_number": "12345",
            **decompose_date("section_certificate_date_of_expiry", section_5_letter_expiry_date),
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": section_5_letter_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
        },
    }

    assert post_organisation_document_matcher.called_once
    assert post_organisation_document_matcher.last_request.json() == {
        "document_type": "section-five-certificate",
        "expiry_date": section_5_letter_expiry_date.isoformat(),
        "reference_code": "12345",
        "document": {
            "name": "letter_of_authority.pdf",
            "s3_key": "letter_of_authority.pdf",
            "size": 0,
        },
    }


def test_edit_firearm_section_5_firearms_act_set_yes_with_document(
    organisation_with_rfd_and_section_5_document,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_detail_url,
):
    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "yes",
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url

    expiry_date = datetime.date.today() + datetime.timedelta(days=10)
    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "section_certificate_date_of_expiry": expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "section 5 ref",
        },
    }


def test_edit_section_5_firearms_act_set_no(
    organisation_with_rfd_and_section_5_document,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_detail_url,
):
    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "no",
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "is_covered_by_firearm_act_section_one_two_or_five": "No",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
        },
    }


def test_edit_firearm_section_5_firearms_act_set_dont_know(
    organisation_with_rfd_and_section_5_document,
    mock_good_put,
    post_to_step,
    edit_url,
    authorized_client,
    product_detail_url,
):
    response = authorized_client.get(edit_url)
    assert isinstance(response.context["form"], FirearmSection5Form)

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "dont_know",
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url

    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "is_covered_by_firearm_act_section_one_two_or_five": "Unsure",
        },
    }
