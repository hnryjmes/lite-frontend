import datetime
import pytest

from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse

from exporter.core.helpers import decompose_date
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmAttachShotgunCertificateForm,
)


@pytest.fixture(autouse=True)
def setup(settings, mock_good_get, no_op_storage):
    settings.FEATURE_FLAG_PRODUCT_2_0 = True


@pytest.mark.parametrize(
    "url_name, form_class",
    (
        ("firearm_edit_firearm_certificate", FirearmAttachFirearmCertificateForm),
        ("firearm_edit_shotgun_certificate", FirearmAttachShotgunCertificateForm),
        ("firearm_edit_letter_of_authority", FirearmAttachSection5LetterOfAuthorityForm),
    ),
)
def test_edit_firearm_certificate_view_exists(
    firearm_good,
    authorized_client,
    url_name,
    form_class,
):
    url = reverse(f"goods:{url_name}", kwargs={"pk": firearm_good["id"]})
    response = authorized_client.get(url)
    assert response.status_code == 200

    form = response.context["form"]
    assert isinstance(form, form_class)


@pytest.mark.parametrize(
    "url_name, certificate_type",
    (
        ("firearm_edit_firearm_certificate", "section-one-certificate"),
        ("firearm_edit_shotgun_certificate", "section-two-certificate"),
        ("firearm_edit_letter_of_authority", "section-five-certificate"),
    ),
)
def test_edit_certificate_submission_success(
    data_organisation,
    firearm_good,
    mock_good_put,
    authorized_client,
    url_name,
    product_detail_url,
    requests_mock,
    certificate_type,
):
    post_organisation_document_matcher = requests_mock.post(
        f"/organisations/{data_organisation['id']}/documents/",
        status_code=201,
        json={},
    )
    certificate_expiry_date = datetime.date.today() + datetime.timedelta(days=5)

    url = reverse(f"goods:{url_name}", kwargs={"pk": firearm_good["id"]})
    post_data = {
        "file": SimpleUploadedFile(f"{certificate_type}.pdf", b"This is the firearm certificate"),
        "section_certificate_number": "12345",
        **decompose_date("section_certificate_date_of_expiry", certificate_expiry_date),
    }
    response = authorized_client.post(url, data=post_data)

    assert response.status_code == 302
    assert response.url == product_detail_url

    assert mock_good_put.called_once
    assert mock_good_put.last_request.json() == {
        "firearm_details": {
            "section_certificate_date_of_expiry": certificate_expiry_date.isoformat(),
            "section_certificate_missing": False,
            "section_certificate_number": "12345",
        },
    }

    assert post_organisation_document_matcher.called_once
    assert post_organisation_document_matcher.last_request.json() == {
        "document_type": certificate_type,
        "expiry_date": certificate_expiry_date.isoformat(),
        "reference_code": "12345",
        "document": {
            "name": f"{certificate_type}.pdf",
            "s3_key": f"{certificate_type}.pdf",
            "size": 0,
        },
    }
