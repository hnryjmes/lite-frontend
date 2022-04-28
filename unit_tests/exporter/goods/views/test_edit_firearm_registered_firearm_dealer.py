import datetime
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.applications.views.goods.add_good_firearm.views.constants import AddGoodFirearmSteps
from exporter.core.forms import CurrentFile
from exporter.core.helpers import convert_api_date_string_to_date, decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmFirearmAct1968Form,
    FirearmRegisteredFirearmsDealerForm,
    FirearmSection5Form,
)


@pytest.fixture(autouse=True)
def setup(settings, mock_good_get, mock_good_put, mock_organisation_document_post, no_op_storage):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.fixture
def edit_firearm_good_registered_firearms_dealer_url(firearm_good):
    return reverse(
        "goods:firearm_edit_registered_firearms_dealer",
        kwargs={"pk": firearm_good["id"]},
    )


@pytest.fixture
def goto_step(goto_step_factory, edit_firearm_good_registered_firearms_dealer_url):
    return goto_step_factory(edit_firearm_good_registered_firearms_dealer_url)


@pytest.fixture
def post_to_step(post_to_step_factory, edit_firearm_good_registered_firearms_dealer_url):
    return post_to_step_factory(edit_firearm_good_registered_firearms_dealer_url)


def test_edit_firearm_good_registered_firearms_dealer_not_rfd_to_rfd(
    data_organisation,
    mock_good_get,
    mock_good_put,
    product_detail_url,
    rfd_certificate,
    requests_mock,
    post_to_step,
):
    post_organisation_document_matcher = requests_mock.post(
        f"/organisations/{data_organisation['id']}/documents/",
        status_code=201,
        json={},
    )

    delete_rfd_organisation_document_matcher = requests_mock.delete(
        f"/organisations/{data_organisation['id']}/document/{rfd_certificate['id']}/",
        status_code=204,
        json={},
    )

    response = post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": True},
    )
    assert isinstance(response.context["form"], FirearmAttachRFDCertificate)

    rfd_expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    response = post_to_step(
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE,
        {
            "reference_code": "12345",
            "file": SimpleUploadedFile("rfd_certificate.pdf", b"This is the rfd certificate"),
            **decompose_date("expiry_date", rfd_expiry_date),
        },
    )
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
            "is_registered_firearm_dealer": True,
            "section_certificate_date_of_expiry": section_5_letter_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
        },
    }

    assert post_organisation_document_matcher.call_count == 2

    section_cert_request = post_organisation_document_matcher.request_history.pop()
    assert section_cert_request.json() == {
        "document_type": "section-five-certificate",
        "expiry_date": section_5_letter_expiry_date.isoformat(),
        "reference_code": "12345",
        "document": {
            "name": "letter_of_authority.pdf",
            "s3_key": "letter_of_authority.pdf",
            "size": 0,
        },
    }

    rfd_request = post_organisation_document_matcher.request_history.pop()
    assert rfd_request.json() == {
        "document_type": "rfd-certificate",
        "expiry_date": rfd_expiry_date.isoformat(),
        "reference_code": "12345",
        "document": {
            "name": "rfd_certificate.pdf",
            "s3_key": "rfd_certificate.pdf",
            "size": 0,
        },
    }


def test_edit_registered_firearms_dealer_rfd_to_rfd_with_updated_details_and_new_files(
    organisation_with_rfd_and_section_5_document,
    data_organisation,
    mock_good_put,
    product_detail_url,
    requests_mock,
    goto_step,
    post_to_step,
    section_5_document,
    rfd_certificate,
):
    post_organisation_document_matcher = requests_mock.post(
        f"/organisations/{data_organisation['id']}/documents/",
        status_code=201,
        json={},
    )

    delete_rfd_organisation_document_matcher = requests_mock.delete(
        f"/organisations/{data_organisation['id']}/document/{rfd_certificate['id']}/",
        status_code=204,
        json={},
    )

    response = goto_step(AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER)
    form = response.context["form"]
    assert isinstance(form, FirearmRegisteredFirearmsDealerForm)
    assert form.initial == {
        "is_registered_firearm_dealer": True,
    }

    response = post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": True},
    )
    form = response.context["form"]
    assert isinstance(form, FirearmAttachRFDCertificate)
    assert form.initial["expiry_date"] == datetime.datetime.strptime(rfd_certificate["expiry_date"], "%d %B %Y").date()
    assert form.initial["reference_code"] == rfd_certificate["reference_code"]
    file = form.initial["file"]
    assert isinstance(file, CurrentFile)
    assert file.name == rfd_certificate["document"]["name"]
    assert file.safe == rfd_certificate["document"]["safe"]
    assert file.url == f"/organisation/document/{rfd_certificate['id']}/"

    rfd_expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    response = post_to_step(
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE,
        {
            "reference_code": "12345",
            "file": SimpleUploadedFile("new_rfd_certificate.pdf", b"This is the rfd certificate"),
            **decompose_date("expiry_date", rfd_expiry_date),
        },
    )
    form = response.context["form"]
    assert isinstance(form, FirearmSection5Form)
    assert form.initial == {}

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "yes",
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url
    section_certificate_date_of_expiry = convert_api_date_string_to_date(section_5_document["expiry_date"]).isoformat()
    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "is_registered_firearm_dealer": True,
            "section_certificate_date_of_expiry": section_certificate_date_of_expiry,
            "section_certificate_missing": False,
            "section_certificate_number": "section 5 ref",
        },
    }

    assert delete_rfd_organisation_document_matcher.call_count == 2
    assert post_organisation_document_matcher.called_once
    doc_request = post_organisation_document_matcher.last_request
    assert doc_request.json() == {
        "document_type": "rfd-certificate",
        "expiry_date": rfd_expiry_date.isoformat(),
        "reference_code": "12345",
        "document": {
            "name": "new_rfd_certificate.pdf",
            "s3_key": "new_rfd_certificate.pdf",
            "size": 0,
        },
    }


def test_edit_registered_firearms_dealer_rfd_to_rfd_with_updated_details_keeping_existing_files(
    organisation_with_rfd_and_section_5_document,
    data_organisation,
    mock_good_put,
    product_detail_url,
    requests_mock,
    goto_step,
    post_to_step,
    rfd_certificate,
    section_5_document,
):
    put_rfd_document_matcher = requests_mock.put(
        f"/organisations/{data_organisation['id']}/document/{rfd_certificate['id']}/",
        status_code=200,
        json={},
    )

    response = goto_step(AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER)
    form = response.context["form"]
    assert isinstance(form, FirearmRegisteredFirearmsDealerForm)
    assert form.initial == {
        "is_registered_firearm_dealer": True,
    }

    response = post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": True},
    )
    form = response.context["form"]
    assert isinstance(form, FirearmAttachRFDCertificate)
    assert form.initial["expiry_date"] == datetime.datetime.strptime(rfd_certificate["expiry_date"], "%d %B %Y").date()
    assert form.initial["reference_code"] == rfd_certificate["reference_code"]
    file = form.initial["file"]
    assert isinstance(file, CurrentFile)
    assert file.name == rfd_certificate["document"]["name"]
    assert file.safe == rfd_certificate["document"]["safe"]
    assert file.url == f"/organisation/document/{rfd_certificate['id']}/"

    rfd_expiry_date = datetime.date.today() + datetime.timedelta(days=5)
    response = post_to_step(
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE,
        {
            "reference_code": "67890",
            **decompose_date("expiry_date", rfd_expiry_date),
        },
    )
    form = response.context["form"]
    assert isinstance(form, FirearmSection5Form)
    assert form.initial == {}

    response = post_to_step(
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5,
        {
            "is_covered_by_section_5": "yes",
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url
    section_certificate_date_of_expiry = convert_api_date_string_to_date(section_5_document["expiry_date"]).isoformat()
    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "firearms_act_section": "firearms_act_section5",
            "is_covered_by_firearm_act_section_one_two_or_five": "Yes",
            "is_covered_by_firearm_act_section_one_two_or_five_explanation": "",
            "is_registered_firearm_dealer": True,
            "section_certificate_date_of_expiry": section_certificate_date_of_expiry,
            "section_certificate_missing": False,
            "section_certificate_number": "section 5 ref",
        },
    }

    assert put_rfd_document_matcher.called_once
    last_request = put_rfd_document_matcher.last_request
    assert last_request.json() == {
        "expiry_date": rfd_expiry_date.isoformat(),
        "reference_code": "67890",
        "document_type": "rfd-certificate",
    }


def test_edit_registered_firearms_dealer_rfd_to_not_rfd(
    organisation_with_rfd_and_section_5_document,
    data_organisation,
    product_detail_url,
    requests_mock,
    post_to_step,
    rfd_certificate,
):
    delete_rfd_organisation_document_matcher = requests_mock.delete(
        f"/organisations/{data_organisation['id']}/document/{rfd_certificate['id']}/",
        status_code=204,
        json={},
    )

    response = post_to_step(
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER,
        {"is_registered_firearm_dealer": False},
    )
    form = response.context["form"]
    assert isinstance(form, FirearmFirearmAct1968Form)
    assert form.initial == {}

    response = post_to_step(
        AddGoodFirearmSteps.FIREARM_ACT_1968,
        {
            "firearms_act_section": "dont_know",
            "not_covered_explanation": "firearms act not covered explanation",
        },
    )

    assert response.status_code == 302
    assert response.url == product_detail_url

    assert delete_rfd_organisation_document_matcher.called_once
