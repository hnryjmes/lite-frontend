import datetime
import pytest
import requests
import uuid

from dateutil.relativedelta import relativedelta
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachRFDCertificate,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
)


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"category": ['Select a firearm category, or select "None of the above"']}),
        (
            {"category": ["NON_AUTOMATIC_SHOTGUN", "NONE"]},
            False,
            {"category": ['Select a firearm category, or select "None of the above"']},
        ),
        ({"category": ["NON_AUTOMATIC_SHOTGUN", "NON_AUTOMATIC_RIM_FIRED_RIFLE"]}, True, {}),
        ({"category": ["NONE"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmCategoryForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"name": ["Enter a descriptive name"]}),
        ({"name": ["TEST NAME"]}, True, {}),
    ),
)
def test_firearm_category_form(data, is_valid, errors):
    form = FirearmNameForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.fixture
def request_with_session(rf, client):
    request = rf.get("/")
    request.session = client.session
    request.requests_session = requests.Session()

    return request


@pytest.fixture
def control_list_entries(requests_mock):
    requests_mock.get(
        "/static/control-list-entries/", json={"control_list_entries": [{"rating": "ML1"}, {"rating": "ML1a"}]}
    )


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )


def test_firearm_product_control_list_entry_form_init_control_list_entries(request_with_session, control_list_entries):
    form = FirearmProductControlListEntryForm(request=request_with_session)
    assert form.fields["control_list_entries"].choices == [("ML1", "ML1"), ("ML1a", "ML1a")]


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_good_controlled": ["Select yes if you know the products control list entry"]}),
        ({"is_good_controlled": True}, False, {"control_list_entries": ["Enter the control list entry"]}),
        ({"is_good_controlled": True, "control_list_entries": ["ML1", "ML1a"]}, True, {}),
        ({"is_good_controlled": False}, True, {}),
    ),
)
def test_firearm_product_control_list_entry_form(data, is_valid, errors, request_with_session, control_list_entries):
    form = FirearmProductControlListEntryForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_pv_graded": ["Select yes if the product has a security grading or classification"]}),
        ({"is_pv_graded": True}, True, {}),
        ({"is_pv_graded": False}, True, {}),
    ),
)
def test_firearm_pv_security_gradings_form(data, is_valid, errors):
    form = FirearmPvGradingForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        (
            {},
            False,
            {
                "grading": ["Select the security grading"],
                "issuing_authority": ["Enter the name and address of the issuing authority"],
                "reference": ["Enter the reference"],
                "date_of_issue": ["Enter the date of issue"],
            },
        ),
        (
            {"grading": "official", "reference": "ABC123"},
            False,
            {
                "issuing_authority": ["Enter the name and address of the issuing authority"],
                "date_of_issue": ["Enter the date of issue"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
            },
            False,
            {
                "date_of_issue": ["Date of issue must include a month", "Date of issue must include a year"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["Date of issue must include a month"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2040",
            },
            False,
            {
                "date_of_issue": ["Date of issue must be in the past"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "50",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["day is out of range for month"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "20",
                "date_of_issue_2": "2020",
            },
            False,
            {
                "date_of_issue": ["month must be in 1..12"],
            },
        ),
        (
            {
                "grading": "official",
                "reference": "ABC123",
                "issuing_authority": "Government entity",
                "date_of_issue_0": "20",
                "date_of_issue_1": "2",
                "date_of_issue_2": "2020",
            },
            True,
            {},
        ),
    ),
)
def test_firearm_pv_security_grading_details_form(data, is_valid, errors, request_with_session, pv_gradings):
    form = FirearmPvGradingDetailsForm(data=data, request=request_with_session)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"calibre": ["Enter the calibre"]}),
        ({"calibre": "calibre 123"}, True, {}),
    ),
)
def test_firearm_calibre_form(data, is_valid, errors):
    form = FirearmCalibreForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_replica": ["Select yes if the product is a replica firearm"]}),
        ({"is_replica": True}, False, {"replica_description": ["Enter a description"]}),
        ({"is_replica": True, "replica_description": "Replica description"}, True, {}),
        ({"is_replica": False}, True, {}),
    ),
)
def test_firearm_replica_form(data, is_valid, errors):
    form = FirearmReplicaForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_rfd_valid": ["Select yes if your registered firearms dealer certificate is still valid"]}),
        ({"is_rfd_valid": True}, True, {}),
    ),
)
def test_firearm_validity_form(data, is_valid, errors):
    rfd_certificate = {
        "id": uuid.uuid4(),
        "document": {
            "name": "TEST DOCUMENT",
        },
    }

    form = FirearmRFDValidityForm(data=data, rfd_certificate=rfd_certificate)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_registered_firearm_dealer": ["Select yes if you are a registered firearms dealer"]}),
        ({"is_registered_firearm_dealer": True}, True, {}),
    ),
)
def test_firearm_registered_firearms_dealer_form(data, is_valid, errors):
    form = FirearmRegisteredFirearmsDealerForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        (
            {},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Enter the expiry date"],
            },
        ),
        (
            decompose_date("expiry_date", datetime.date.today() - datetime.timedelta(days=10)),
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date("expiry_date", datetime.date.today()),
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be in the future"],
            },
        ),
        (
            decompose_date("expiry_date", datetime.date.today() + relativedelta(years=5, days=1)),
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be within 5 years"],
            },
        ),
        (
            {"expiry_date_1": "12", "expiry_date_2": "2022"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must include a day"],
            },
        ),
        (
            {"expiry_date_0": "1", "expiry_date_2": "2022"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must include a month"],
            },
        ),
        (
            {"expiry_date_0": "1", "expiry_date_1": "12"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must include a year"],
            },
        ),
        (
            {"expiry_date_0": "abc", "expiry_date_1": "abc", "expiry_date_2": "abc"},
            {},
            False,
            {
                "file": ["Select a registered firearms dealer certificate"],
                "reference_code": ["Enter the certificate number"],
                "expiry_date": ["Expiry date must be a real date"],
            },
        ),
        (
            {
                "reference_code": "abcdef",
                **decompose_date(
                    "expiry_date",
                    datetime.date.today() + datetime.timedelta(days=1),
                ),
            },
            {"file": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
    ),
)
def test_firearm_attach_rfd_certificate_form(data, files, is_valid, errors):
    form = FirearmAttachRFDCertificate(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_document_available": ["Select yes or no"]}),
        (
            {"is_document_available": False},
            False,
            {"no_document_comments": ["Enter a reason why you cannot upload a product document"]},
        ),
        ({"is_document_available": False, "no_document_comments": "product not manufactured yet"}, True, {}),
        (
            {"is_document_available": True},
            True,
            {},
        ),
    ),
)
def test_firearm_document_availability_form(data, is_valid, errors):
    form = FirearmDocumentAvailability(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, is_valid, errors",
    (
        ({}, False, {"is_document_sensitive": ["Select yes if the document is rated above Official-sensitive"]}),
        ({"is_document_sensitive": True}, True, {}),
        ({"is_document_sensitive": False}, True, {}),
    ),
)
def test_firearm_document_sensitivity_form(data, is_valid, errors):
    form = FirearmDocumentSensitivityForm(data=data)
    assert form.is_valid() == is_valid
    assert form.errors == errors


@pytest.mark.parametrize(
    "data, files, is_valid, errors",
    (
        ({}, {}, False, {"product_document": ["Select a document that shows what your product is designed to do"]}),
        (
            {"description": ""},
            {},
            False,
            {"product_document": ["Select a document that shows what your product is designed to do"]},
        ),
        (
            {"description": "product data sheet"},
            {"product_document": SimpleUploadedFile("test", b"test content")},
            True,
            {},
        ),
    ),
)
def test_firearm_product_document_upload_form(data, files, is_valid, errors):
    form = FirearmDocumentUploadForm(data=data, files=files)
    assert form.is_valid() == is_valid
    assert form.errors == errors
