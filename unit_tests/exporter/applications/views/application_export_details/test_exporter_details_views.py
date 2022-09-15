import pytest

from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from exporter.applications.views.application_export_details.constants import ExportDetailsSteps
from exporter.applications.views.application_export_details.forms import (
    F680ReferenceNumberForm,
    F1686DetailsForm,
    SecurityOtherDetailsForm,
)


@pytest.fixture(autouse=True)
def setup(no_op_storage):
    pass


@pytest.fixture(autouse=True)
def set_feature_flags(settings):
    settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED = True


@pytest.fixture
def application_export_details_url(data_standard_case):
    application_id = data_standard_case["case"]["data"]["id"]
    return reverse(
        "applications:application_export_details",
        kwargs={
            "pk": application_id,
        },
    )


@pytest.fixture
def goto_step(goto_step_factory, application_export_details_url):
    return goto_step_factory(application_export_details_url)


@pytest.fixture
def post_to_step(post_to_step_factory, application_export_details_url):
    return post_to_step_factory(application_export_details_url)


def test_application_export_details_access_denied_without_feature_flag(
    settings,
    authorized_client,
    application_export_details_url,
):
    settings.FEATURE_FLAG_F680_SECURITY_CLASSIFIED_ENABLED = False
    response = authorized_client.get(application_export_details_url)
    assert response.status_code == 404


def test_application_export_details_end_to_end(
    authorized_client,
    data_standard_case,
    application_export_details_url,
    mock_application_get,
    mock_application_put,
    post_to_step,
):
    authorized_client.get(application_export_details_url)

    response = post_to_step(
        ExportDetailsSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": ["F680", "F1686", "Other"],
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], F680ReferenceNumberForm)

    response = post_to_step(
        ExportDetailsSteps.F680_REFERENCE_NUMBER,
        {
            "f680_reference_number": "dummy ref",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], F1686DetailsForm)

    response = post_to_step(
        ExportDetailsSteps.F1686_DETAILS,
        {
            "f1686_contracting_authority": "dummy contracting authority",
            "is_f1686_approval_document_available": True,
            "f1686_approval_document": SimpleUploadedFile("data sheet", b"This is a an approval document"),
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], SecurityOtherDetailsForm)

    response = post_to_step(
        ExportDetailsSteps.SECURITY_OTHER_DETAILS,
        {
            "other_security_approval_details": "dummy other details",
            "other_security_approval_document": SimpleUploadedFile("data sheet", b"Other approval document"),
        },
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": ["F680", "F1686", "Other"],
        "is_mod_security_approved": True,
        "f680_reference_number": "dummy ref",
        "f1686_contracting_authority": "dummy contracting authority",
        "other_security_approval_details": "dummy other details",
    }

    assert response.url == reverse(
        "applications:locations_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


def test_application_export_details_end_to_end_alternative(
    authorized_client,
    data_standard_case,
    application_export_details_url,
    mock_application_get,
    mock_application_put,
    post_to_step,
):
    authorized_client.get(application_export_details_url)

    response = post_to_step(
        ExportDetailsSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": True,
            "security_approvals": ["F1686", "Other"],
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], F1686DetailsForm)

    response = post_to_step(
        ExportDetailsSteps.F1686_DETAILS,
        {
            "f1686_contracting_authority": "dummy contracting authority",
            "is_f1686_approval_document_available": False,
            "f1686_reference_number": "dummy f1686 reference number",
            "f1686_approval_date_0": "02",
            "f1686_approval_date_1": "02",
            "f1686_approval_date_2": "2020",
        },
    )

    assert response.status_code == 200
    assert isinstance(response.context["form"], SecurityOtherDetailsForm)

    response = post_to_step(
        ExportDetailsSteps.SECURITY_OTHER_DETAILS,
        {
            "other_security_approval_details": "dummy other details",
        },
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": ["F1686", "Other"],
        "is_mod_security_approved": True,
        "f1686_contracting_authority": "dummy contracting authority",
        "f1686_reference_number": "dummy f1686 reference number",
        "f1686_approval_date": "2020-02-02",
        "other_security_approval_details": "dummy other details",
    }

    assert response.url == reverse(
        "applications:locations_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )


def test_application_export_details_short(
    authorized_client,
    data_standard_case,
    application_export_details_url,
    mock_application_get,
    mock_application_put,
    post_to_step,
):
    authorized_client.get(application_export_details_url)

    response = post_to_step(
        ExportDetailsSteps.SECURITY_CLASSIFIED,
        {
            "is_mod_security_approved": False,
        },
    )

    assert response.status_code == 302

    assert mock_application_put.called_once
    last_request = mock_application_put.last_request

    assert last_request.json() == {
        "security_approvals": [],
        "is_mod_security_approved": False,
    }
    assert response.url == reverse(
        "applications:locations_summary",
        kwargs={
            "pk": data_standard_case["case"]["id"],
        },
    )
