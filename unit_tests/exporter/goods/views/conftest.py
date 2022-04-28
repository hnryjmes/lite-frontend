import datetime
import pytest
import uuid

from django.urls import reverse

from core import client


@pytest.fixture
def mock_good_get(requests_mock, firearm_good):
    url = client._build_absolute_uri(f'/goods/{firearm_good["id"]}/')
    return requests_mock.get(url=url, json={"good": firearm_good})


@pytest.fixture
def mock_good_put(requests_mock, firearm_good):
    url = client._build_absolute_uri(f'/goods/{firearm_good["id"]}/')
    return requests_mock.put(url=url, json={})


@pytest.fixture
def mock_control_list_entries_get(requests_mock):
    url = client._build_absolute_uri(f"/static/control-list-entries/")
    return requests_mock.get(url=url, json={"control_list_entries": [{"rating": "ML1a"}, {"rating": "ML22b"}]})


@pytest.fixture
def pv_gradings(requests_mock):
    requests_mock.get(
        "/static/private-venture-gradings/v2/",
        json={"pv_gradings": [{"official": "Official"}, {"restricted": "Restricted"}]},
    )


@pytest.fixture
def mock_good_document_post(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/documents/')
    yield requests_mock.post(url=url, json={}, status_code=201)


@pytest.fixture
def mock_good_document_put(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    document_pk = good["documents"][0]["id"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/documents/{document_pk}/')
    yield requests_mock.put(url=url, json={})


@pytest.fixture
def mock_good_document_delete(requests_mock, data_standard_case):
    good = data_standard_case["case"]["data"]["goods"][0]["good"]
    document_pk = good["documents"][0]["id"]
    url = client._build_absolute_uri(f'/goods/{good["id"]}/documents/{document_pk}/')
    yield requests_mock.delete(url=url, json={})


@pytest.fixture
def mock_organisation_document_post(requests_mock, data_organisation):
    url = client._build_absolute_uri(f"/organisations/{data_organisation['id']}/documents/")
    yield requests_mock.post(url=url, json={}, status_code=201)


@pytest.fixture
def organisation_id():
    return str(uuid.uuid4())


@pytest.fixture
def rfd_certificate(organisation_id):
    expiry_date = datetime.date.today() + datetime.timedelta(days=100)
    return {
        "id": "b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a",
        "document": {
            "name": "rfd_certificate.txt",
            "s3_key": "rfd_certificate.txt.s3_key",
            "safe": True,
            "size": 3,
            "id": "9c2222db-98e5-47e8-9e01-653354e95322",
        },
        "document_type": "rfd-certificate",
        "is_expired": False,
        "organisation": organisation_id,
        "expiry_date": expiry_date.strftime("%d %B %Y"),
        "reference_code": "RFD123",
    }


@pytest.fixture
def section_5_document(organisation_id):
    expiry_date = datetime.date.today() + datetime.timedelta(days=10)
    return {
        "id": str(uuid.uuid4()),
        "document": {
            "name": "section5.txt",
            "s3_key": "section5.txt.s3_key",
            "safe": True,
            "size": 3,
        },
        "document_type": "section-five-certificate",
        "is_expired": False,
        "organisation": organisation_id,
        "reference_code": "section 5 ref",
        "expiry_date": expiry_date.strftime("%d %B %Y"),
    }


@pytest.fixture
def application(data_standard_case, requests_mock):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    matcher = requests_mock.get(url=app_url, json=data_standard_case["case"])
    return matcher


@pytest.fixture
def application_with_organisation_rfd_document(data_standard_case, requests_mock, rfd_certificate):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [rfd_certificate],
    }
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.fixture
def application_with_organisation_and_application_rfd_document(data_standard_case, requests_mock, rfd_certificate):
    app_url = client._build_absolute_uri(f"/applications/{data_standard_case['case']['id']}/")
    case = data_standard_case["case"]
    case["organisation"] = {
        "documents": [rfd_certificate],
    }
    case["additional_documents"] = [
        {
            "document_type": "rfd-certificate",
        }
    ]
    matcher = requests_mock.get(url=app_url, json=case)
    return matcher


@pytest.fixture
def application_without_rfd_document(application):
    return application


@pytest.fixture
def product_detail_url(firearm_good):
    return reverse(
        "goods:good",
        kwargs={
            "pk": firearm_good["id"],
        },
    )


@pytest.fixture
def organisation_with_rfd_and_section_5_document(data_organisation, requests_mock, rfd_certificate, section_5_document):
    app_url = client._build_absolute_uri(f"/organisations/{data_organisation['id']}/")
    data_organisation["documents"] = [
        rfd_certificate,
        section_5_document,
    ]
    matcher = requests_mock.get(url=app_url, json=data_organisation)
    return matcher
