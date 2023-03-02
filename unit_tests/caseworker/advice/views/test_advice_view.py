import pytest
from bs4 import BeautifulSoup
from django.urls import reverse

from core import client


@pytest.fixture(autouse=True)
def setup(
    mock_queue,
    mock_denial_reasons,
    mock_application_good_documents,
):
    yield


@pytest.fixture(autouse=True)
def assign_users_to_cases(
    mock_gov_user,
    mock_gov_beis_nuclear_user,
    data_standard_case_with_all_trigger_list_products_assessed,
    data_standard_case_with_potential_trigger_list_product,
):
    for case in [
        data_standard_case_with_all_trigger_list_products_assessed,
        data_standard_case_with_potential_trigger_list_product,
    ]:
        case["case"]["assigned_users"]["queue"] = [mock_gov_user["user"]]


@pytest.fixture
def url(data_standard_case):
    return reverse(
        "cases:advice_view",
        kwargs={"queue_pk": "566fd526-bd6d-40c1-94bd-60d10c967cf7", "pk": data_standard_case["case"]["id"]},
    )


@pytest.fixture
def mock_application(requests_mock):
    def _setup_mock_application(data):
        application_id = data["case"]["id"]
        requests_mock.get(client._build_absolute_uri(f"/cases/{application_id}"), json=data)

    return _setup_mock_application


def test_user_in_context(
    authorized_client,
    data_standard_case_with_all_trigger_list_products_assessed,
    mock_gov_user,
    url,
    mock_application,
):
    mock_application(data_standard_case_with_all_trigger_list_products_assessed)
    response = authorized_client.get(url)
    # "current_user" passed in from caseworker context processor
    # used to test rule "can_user_change_case"
    assert response.context["current_user"] == mock_gov_user["user"]


def test_advice_view_shows_no_assessed_trigger_list_goods_if_some_are_not_assessed(
    authorized_client,
    url,
    data_standard_case_with_potential_trigger_list_product,
    mock_gov_beis_nuclear_user,
    mock_application,
):
    mock_application(data_standard_case_with_potential_trigger_list_product)

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is None


def test_advice_view_shows_assessed_trigger_list_goods_if_all_are_assessed(
    authorized_client,
    requests_mock,
    url,
    data_standard_case_with_all_trigger_list_products_assessed,
    mock_gov_beis_nuclear_user,
    mock_application,
):
    mock_application(data_standard_case_with_all_trigger_list_products_assessed)

    response = authorized_client.get(url)

    assert response.status_code == 200

    soup = BeautifulSoup(response.content, "html.parser")
    product_table = soup.find(id="assessed-products")
    assert product_table is not None

    rows = product_table.tbody.find_all("tr")
    assert len(rows) == len(data_standard_case_with_all_trigger_list_products_assessed["case"]["data"]["goods"])
