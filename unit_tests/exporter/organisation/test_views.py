import io

from unittest import mock
from django.urls import reverse
from django.core.files.uploadedfile import SimpleUploadedFile

from core import client
from unit_tests.helpers import mocked_now


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
def test_upload_firearm_registered_dealer_certificate(mock_timezone, authorized_client, requests_mock, organisation_pk):
    requests_mock.post(client._build_absolute_uri(f"/organisations/{organisation_pk}/documents/"), status_code=200)

    url = reverse("organisation:upload-firearms-certificate")
    data = {
        "expiry_date_0": 1,  # day
        "expiry_date_1": 1,  # month
        "expiry_date_2": 2022,  # year
        "reference_code": "1234",
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")


@mock.patch("django.utils.timezone.now", side_effect=mocked_now)
def test_upload_section_five_certificate(mock_timezone, authorized_client, requests_mock, organisation_pk):
    requests_mock.post(client._build_absolute_uri(f"/organisations/{organisation_pk}/documents/"), status_code=200)

    url = reverse("organisation:upload-section-five-certificate")
    data = {
        "expiry_date_0": 1,  # day
        "expiry_date_1": 1,  # month
        "expiry_date_2": 2022,  # year
        "reference_code": "1234",
        "file": SimpleUploadedFile("file.txt", b"abc", content_type="text/plain"),
    }

    response = authorized_client.post(url, data)

    assert response.status_code == 302
    assert response.url == reverse("organisation:details")


@mock.patch("core.services.s3_client")
def test_download_docoument_on_organisation(mock_s3_client_class, authorized_client, requests_mock, organisation_pk):
    mock_s3_client_class().get_object.return_value = {
        "ContentType": "application/text",
        "Body": io.BytesIO(b"test"),
    }
    requests_mock.get(
        client._build_absolute_uri(f"/organisations/{organisation_pk}/document/00acebbf-2077-4b80-8b95-37ff7f46c6d0/"),
        json={"document": {"s3_key": "123", "name": "testfile.txt"}},
    )

    url = reverse("organisation:document", kwargs={"pk": "00acebbf-2077-4b80-8b95-37ff7f46c6d0"})

    response = authorized_client.get(url)

    assert response.status_code == 200
    assert b"".join(c for c in response.streaming_content) == b"test"


def test_new_site_form_view(authorized_client, mock_exporter_user_me):
    url = reverse("organisation:sites:new")
    response = authorized_client.get(url)
    assert response.status_code == 200
