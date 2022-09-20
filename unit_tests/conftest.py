import datetime
import pytest
import os

from core import client
from core.constants import OrganisationDocumentType


@pytest.fixture(autouse=True)
def add_test_template_dirs(settings):
    template_dir = os.path.join(settings.BASE_DIR, "unit_tests", "core", "summaries", "templates")
    settings.TEMPLATES[0]["DIRS"].append(template_dir)


@pytest.fixture
def data_control_list_entries():
    # in relity there are around 3000 CLCs
    return {
        "control_list_entries": [
            {"rating": "ML1", "text": "Smooth-bore weapons with a calibre of less than 20mm, other firearms..."},
            {"rating": "ML1a", "text": "Rifles and combination guns, handguns, machine, sub-machine and volley guns"},
        ]
    }


@pytest.fixture
def mock_control_list_entries(requests_mock, data_control_list_entries):
    url = client._build_absolute_uri("/static/control-list-entries/")
    yield requests_mock.get(url=url, json=data_control_list_entries)


@pytest.fixture
def mock_pv_gradings(requests_mock):
    url = client._build_absolute_uri("/static/private-venture-gradings/")
    yield requests_mock.get(url=url, json={"pv_gradings": []})


@pytest.fixture
def data_open_case():
    return {
        "case": {
            "id": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000001",
                "reference": {"key": "oiel", "value": "Open Individual Export Licence"},
                "type": {"key": "application", "value": "Application"},
                "sub_type": {"key": "open", "value": "Open Licence"},
            },
            "flags": [
                {
                    "id": "00000000-0000-0000-0000-000000000007",
                    "name": "Firearms",
                    "colour": "default",
                    "label": None,
                    "priority": 0,
                    "removable_by": "Anyone",
                },
                {
                    "id": "00000000-0000-0000-0000-000000000014",
                    "name": "Enforcement Check Req",
                    "colour": "default",
                    "label": None,
                    "priority": 0,
                    "removable_by": "Anyone",
                },
            ],
            "queues": ["0149b643-d38a-4d1a-b259-7f73ff4f7b97"],
            "queue_names": ["queue 20200629162022"],
            "assigned_users": {},
            "has_advice": {"user": False, "my_user": False, "team": False, "my_team": False, "final": False},
            "advice": [],
            "all_flags": [
                {
                    "id": "0149b643-d38a-4d1a-b259-7f73ff4f7b97",
                    "name": "Item not verified",
                    "alias": None,
                    "label": None,
                    "colour": "default",
                    "priority": 0,
                    "level": "Good",
                },
                {
                    "name": "Destination20200629144727",
                    "alias": None,
                    "label": "Test label",
                    "colour": "blue",
                    "priority": 0,
                    "level": "Destination",
                    "removable_by": "Anyone",
                },
                {
                    "id": "564f2c59-13a0-4d28-b2d1-749ec45c7c7d",
                    "name": "Enforcement Check Req",
                    "label": None,
                    "colour": "default",
                    "priority": 0,
                    "level": "Case",
                },
                {
                    "id": "f097dab7-2b5d-49cd-a0a2-310e70ae0892",
                    "name": "Firearms",
                    "alias": None,
                    "label": None,
                    "colour": "default",
                    "priority": 0,
                    "level": "Case",
                },
                {
                    "id": "de8fcf9f-15c1-447d-9144-adc484b4a1c5",
                    "name": "Organisation2020062916081",
                    "alias": None,
                    "label": "Test label",
                    "colour": "pink",
                    "priority": 0,
                    "level": "Organisation",
                    "removable_by": "Anyone",
                },
            ],
            "case_officer": None,
            "audit_notification": None,
            "reference_code": "GBOIEL/2020/0000045/P",
            "copy_of": None,
            "sla_days": 0,
            "sla_remaining_days": 60,
            "data": {
                "id": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
                "name": "aggregate proactive architectures",
                "organisation": {
                    "id": "9bc26604-35ee-4383-9f58-74f8cab67443",
                    "documents": [],
                    "primary_site": {
                        "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                        "name": "Headquarters",
                        "address": {
                            "id": "3f611bdb-ee89-41b5-a6f0-26f8b1182016",
                            "address_line_1": "42 Question Road",
                            "address_line_2": "",
                            "city": "London",
                            "region": "London",
                            "postcode": "Islington",
                            "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
                        },
                        "records_located_at": {
                            "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                            "name": "Headquarters",
                            "address": {
                                "address_line_1": "42 Question Road",
                                "address_line_2": "",
                                "region": "London",
                                "postcode": "Islington",
                                "city": "London",
                                "country": {"name": "United Kingdom"},
                            },
                        },
                    },
                    "type": {"key": "commercial", "value": "Commercial Organisation"},
                    "flags": [
                        {
                            "id": "25d7b462-0066-4a7d-bd7d-a9b0122fae09",
                            "name": "Organisation2020062916081",
                            "colour": "pink",
                            "label": "Test label",
                            "priority": 0,
                            "removable_by": "Anyone",
                        }
                    ],
                    "status": {"key": "active", "value": "Active"},
                    "created_at": "2020-06-29T09:30:58.425994Z",
                    "updated_at": "2020-06-29T09:30:58.429528Z",
                    "name": "Archway Communications",
                    "eori_number": "1234567890AAA",
                    "sic_number": "2345",
                    "vat_number": "GB123456789",
                    "registration_number": "09876543",
                },
                "case_type": {
                    "id": "00000000-0000-0000-0000-000000000001",
                    "reference": {"key": "oiel", "value": "Open Individual Export Licence"},
                    "type": {"key": "application", "value": "Application"},
                    "sub_type": {"key": "open", "value": "Open Licence"},
                },
                "export_type": {"key": "permanent", "value": "Permanent"},
                "created_at": "2020-08-03T12:52:34.255494Z",
                "updated_at": "2020-08-03T12:52:37.708891Z",
                "submitted_at": "2020-08-03T12:52:37.703607Z",
                "submitted_by": "Automated Test",
                "status": {"key": "submitted", "value": "Submitted"},
                "case": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
                "reference_code": "GBOIEL/2020/0000045/P",
                "is_major_editable": False,
                "goods_locations": {
                    "type": "sites",
                    "data": [
                        {
                            "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                            "name": "Headquarters",
                            "address": {
                                "id": "3f611bdb-ee89-41b5-a6f0-26f8b1182016",
                                "address_line_1": "42 Question Road",
                                "address_line_2": "",
                                "city": "London",
                                "region": "London",
                                "postcode": "Islington",
                                "country": {
                                    "id": "GB",
                                    "name": "United Kingdom",
                                    "type": "gov.uk Country",
                                    "is_eu": True,
                                },
                            },
                            "records_located_at": {
                                "id": "81a8b5ca-aaa1-4c7d-91c3-627109acfb2d",
                                "name": "Headquarters",
                                "address": {
                                    "address_line_1": "42 Question Road",
                                    "address_line_2": "",
                                    "region": "London",
                                    "postcode": "Islington",
                                    "city": "London",
                                    "country": {"name": "United Kingdom"},
                                },
                            },
                        }
                    ],
                },
                "case_officer": None,
                "end_user": None,
                "ultimate_end_users": [
                    {
                        "id": "87fd61c4-ae4e-45c8-b635-40bd893e93d3",
                        "name": "Mary Example",
                        "address": "123 Fakse street",
                        "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
                        "website": "https://example.com/",
                        "type": "ultimate_end_user",
                        "organisation": "9bc26604-35ee-4383-9f58-74f8cab67443",
                        "document": {
                            "created_at": "2020-08-03T12:52:34.775Z",
                            "updated_at": "2020-08-03T12:52:37.396Z",
                            "id": "cd8d932a-ee7f-4162-9f74-4b614e1a285b",
                            "name": "Party document",
                            "s3_key": "lite-e2e-test-file.txt",
                            "size": None,
                            "virus_scanned_at": "2020-08-03T12:52:37.396Z",
                            "safe": True,
                            "document_ptr_id": "cd8d932a-ee7f-4162-9f74-4b614e1a285b",
                            "party_id": "87fd61c4-ae4e-45c8-b635-40bd893e93d3",
                        },
                        "sub_type": {"key": "commercial", "value": "Commercial Organisation"},
                        "role": {"key": "other", "value": "Other"},
                        "flags": [],
                        "copy_of": None,
                        "deleted_at": None,
                        "clearance_level": None,
                        "descriptors": None,
                    }
                ],
                "third_parties": [],
                "consignee": None,
                "inactive_parties": [],
                "activity": "Trading",
                "usage": None,
                "goods_types": [
                    {
                        "id": "3461adb9-0cc1-4097-b663-e06ac06198a2",
                        "description": "tool to assist peasants seize the means of production",
                        "is_good_controlled": {"key": "False", "value": "No"},
                        "is_good_incorporated": True,
                        "control_list_entries": [
                            {
                                "rating": "ML1a",
                                "text": "Outmoded bourgeois reactionaries",
                            }
                        ],
                        "countries": [{"id": "US", "name": "United States", "type": "gov.uk Country", "is_eu": False}],
                        "document": None,
                        "end_use_control": ["MEND"],
                        "flags": [
                            {
                                "id": "00000000-0000-0000-0000-000000000004",
                                "name": "Item not verified",
                                "colour": "default",
                                "label": None,
                                "removable_by": "Anyone",
                            }
                        ],
                        "comment": None,
                        "report_summary": None,
                    }
                ],
                "additional_documents": [
                    {
                        "id": "bd95f6a1-24ea-4f98-8190-649d4189e612",
                        "created_at": "2020-08-03T12:52:35.345826Z",
                        "updated_at": "2020-08-03T12:52:37.462645Z",
                        "name": "judge farmers on political purity instead of horticultural ability.",
                        "s3_key": "lite-e2e-test-file.txt",
                        "size": None,
                        "virus_scanned_at": "2020-08-03T12:52:37.462286Z",
                        "safe": True,
                        "description": "this is a test additional document",
                        "application": "094eed9a-23cc-478a-92ad-9a05ac17fad0",
                    }
                ],
                "is_military_end_use_controls": False,
                "military_end_use_controls_ref": None,
                "is_informed_wmd": False,
                "informed_wmd_ref": None,
                "is_suspected_wmd": False,
                "suspected_wmd_ref": None,
                "intended_end_use": "intended end use",
                "licence": {"start_date": None, "duration": None, "status": None},
                "is_shipped_waybill_or_lading": True,
                "non_waybill_or_lading_route_details": None,
                "temp_export_details": None,
                "is_temp_direct_control": None,
                "temp_direct_control_details": None,
                "proposed_return_date": None,
                "trade_control_activity": {"key": None, "value": None},
                "trade_control_product_categories": [],
                "goodstype_category": {"key": "military", "value": "Military or dual use"},
                "contains_firearm_goods": True,
                "destinations": {
                    "type": "countries",
                    "data": [
                        {
                            "id": "cef005ab-9081-4669-9396-585160bd06db",
                            "country": {
                                "id": "US",
                                "name": "United States",
                                "flags": [
                                    {
                                        "colour": "blue",
                                        "name": "Destination20200629144727",
                                        "label": "Test label",
                                        "id": "a25d23e5-e0e0-4245-a611-d546edb140f8",
                                        "removable_by": "Anyone",
                                    }
                                ],
                            },
                            "flags": [],
                            "contract_types": ["aircraft_manufacturers", "air_force"],
                            "other_contract_type_text": None,
                        }
                    ],
                },
            },
            "next_review_date": None,
            "licences": [],
        }
    }


@pytest.fixture
def data_standard_case():
    return {
        "case": {
            "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",
            "case_type": {
                "id": "00000000-0000-0000-0000-000000000004",
                "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                "type": {"key": "application", "value": "Application"},
                "sub_type": {"key": "standard", "value": "Standard Licence"},
            },
            "flags": [
                {
                    "id": "00000000-0000-0000-0000-000000000014",
                    "name": "Enforcement Check Req",
                    "alias": "ENF_CHECK_REQ",
                    "colour": "default",
                    "label": None,
                    "priority": 0,
                    "removable_by": "Anyone",
                }
            ],
            "queues": ["1b926457-5c9e-4916-8497-51886e51863a", "c270b79b-370c-4c5e-b8b6-4d5210a58956"],
            "queue_names": ["queue", "queue 20200818000000"],
            "queue_details": [
                {"id": "f458094c-1fed-4222-ac70-ff5fa20ff649", "name": "queue", "alias": "FCDO_CASES_TO_REVIEW"},
                {"id": "c270b79b-370c-4c5e-b8b6-4d5210a58956", "name": "queue 20200818000000", "alias": "QUEUE_2"},
            ],
            "assigned_users": {},
            "has_advice": {
                "user": False,
                "my_user": False,
                "team": False,
                "my_team": False,
                "final": False,
            },
            "advice": [],
            "all_flags": [
                {
                    "id": "2d2ba1de-3178-4c94-a823-ef6a3dba79af",
                    "name": "Enforcement Check Req",
                    "alias": "ENF_CHECK_REQ",
                    "label": None,
                    "colour": "default",
                    "priority": 0,
                    "level": "Case",
                    "removable_by": "Anyone",
                }
            ],
            "case_officer": None,
            "audit_notification": None,
            "reference_code": "GBSIEL/2020/0002687/T",
            "copy_of": None,
            "sla_days": 2,
            "sla_remaining_days": 18,
            "data": {
                "id": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                "name": "444",
                "organisation": {
                    "id": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                    "documents": [],
                    "primary_site": {
                        "id": "c86d3df2-5f48-40cd-a720-e76322df71a9",
                        "name": "Rich org",
                        "address": {
                            "id": "8d8a7631-32fc-4873-9a1f-d5e9afeecc0e",
                            "address_line_1": "jim",
                            "address_line_2": "",
                            "city": "jim",
                            "region": "Richardaho",
                            "postcode": "Dn22 6uh",
                            "country": {
                                "id": "GB",
                                "name": "United Kingdom",
                                "type": "gov.uk Country",
                                "is_eu": True,
                            },
                        },
                        "records_located_at": {
                            "id": "c86d3df2-5f48-40cd-a720-e76322df71a9",
                            "name": "Rich org",
                            "address": {
                                "address_line_1": "jim",
                                "address_line_2": "",
                                "region": "Richardaho",
                                "postcode": "Dn22 6uh",
                                "city": "jim",
                                "country": {"name": "United Kingdom"},
                            },
                        },
                    },
                    "type": {"key": "commercial", "value": "Commercial Organisation"},
                    "flags": [],
                    "status": {"key": "active", "value": "Active"},
                    "created_at": "2020-09-15T10:04:02.741198+01:00",
                    "updated_at": "2020-09-15T10:04:27.663252+01:00",
                    "name": "jim",
                    "eori_number": "GB123456789000",
                    "sic_number": "99715",
                    "vat_number": "GB980941362",
                    "registration_number": "37718958",
                },
                "case_type": {
                    "id": "00000000-0000-0000-0000-000000000004",
                    "reference": {"key": "siel", "value": "Standard Individual Export Licence"},
                    "type": {"key": "application", "value": "Application"},
                    "sub_type": {"key": "standard", "value": "Standard Licence"},
                },
                "export_type": {"key": "temporary", "value": "Temporary"},
                "created_at": "2020-10-01T16:53:58.578579+01:00",
                "updated_at": "2020-10-01T16:57:11.127857+01:00",
                "submitted_at": "2020-10-01T16:57:11.125297+01:00",
                "submitted_by": "rich tier",
                "status": {"key": "submitted", "value": "Submitted"},
                "case": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                "reference_code": "GBSIEL/2020/0002687/T",
                "is_major_editable": False,
                "goods_starting_point": "GB",
                "goods_locations": {
                    "type": "external_locations",
                    "data": [
                        {
                            "id": "149edce6-529e-41c1-a4b3-48df06bfe5a1",
                            "name": "44",
                            "address": "44",
                            "country": {"id": "BN", "name": "Brunei", "type": "gov.uk Country", "is_eu": False},
                            "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                        }
                    ],
                },
                "case_officer": None,
                "end_user": {
                    "id": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                    "name": "End User",
                    "address": "44",
                    "country": {
                        "id": "GB",
                        "name": "United Kingdom",
                        "type": "gov.uk Country",
                        "is_eu": True,
                    },
                    "website": "",
                    "type": "end_user",
                    "type_display_value": "End-user",
                    "signatory_name_euu": "John Doe",
                    "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                    "document": None,
                    "documents": [],
                    "sub_type": {"key": "individual", "value": "Individual"},
                    "sub_type_other": None,
                    "end_user_document_available": False,
                    "end_user_document_missing_reason": "Products details not available as they are not manufactured yet",
                    "product_differences_note": "",
                    "document_in_english": True,
                    "document_on_letterhead": True,
                    "ec3_missing_reason": "",
                    "role": {"key": "other", "value": "Other"},
                    "role_other": None,
                    "flags": [],
                    "copy_of": None,
                    "deleted_at": None,
                    "clearance_level": None,
                    "descriptors": None,
                },
                "ultimate_end_users": [],
                "third_parties": [
                    {
                        "id": "95c2d6b7-5cfd-47e8-b3c8-dc76e1ac9747",
                        "name": "Third party",
                        "address": "44",
                        "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
                        "website": "",
                        "type": "third_party",
                        "type_display_value": "Third party",
                        "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                        "document": None,
                        "sub_type": {"key": "individual", "value": "Individual"},
                        "sub_type_other": None,
                        "role": {"key": "consultant", "value": "Consultant"},
                        "role_other": None,
                        "flags": [],
                        "copy_of": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                        "deleted_at": None,
                        "clearance_level": None,
                        "descriptors": None,
                    }
                ],
                "consignee": {
                    "id": "cd2263b4-a427-4f14-8552-505e1d192bb8",
                    "name": "Consignee",
                    "address": "44",
                    "country": {
                        "id": "AE-AZ",
                        "name": "Abu Dhabi",
                        "type": "gov.uk Territory",
                        "is_eu": False,
                    },
                    "website": "",
                    "type": "consignee",
                    "type_display_value": "Consignee",
                    "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                    "document": None,
                    "sub_type": {"key": "individual", "value": "Individual"},
                    "sub_type_other": None,
                    "role": {"key": "other", "value": "Other"},
                    "role_other": None,
                    "flags": [],
                    "copy_of": None,
                    "deleted_at": None,
                    "clearance_level": None,
                    "descriptors": None,
                },
                "inactive_parties": [],
                "goods": [
                    {
                        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
                        "good": {
                            "id": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
                            "name": "p1",
                            "description": "444",
                            "part_number": "44",
                            "control_list_entries": [{"rating": "ML1a"}, {"rating": "ML22b"}],
                            "comment": None,
                            "is_good_controlled": {"key": "True", "value": "Yes"},
                            "report_summary": "scale compelling technologies",
                            "flags": [],
                            "is_pv_graded": "yes",
                            "documents": [
                                {
                                    "id": "6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335",
                                    "name": "data_sheet.pdf",
                                    "description": "product data sheet",
                                    "safe": True,
                                }
                            ],
                            "grading_comment": None,
                            "pv_grading_details": {
                                "prefix": "NATO",
                                "suffix": "SUFFIX",
                                "grading": {"key": "official", "value": "Official"},
                                "issuing_authority": "Government entity",
                                "reference": "GR123",
                                "date_of_issue": "2020-02-20",
                            },
                            "has_declared_at_customs": True,
                            "has_security_features": True,
                            "security_feature_details": "security features",
                            "is_document_available": True,
                            "no_document_comments": "",
                            "is_document_sensitive": False,
                            "design_details": "some design details",
                            "status": {"key": "verified", "value": "Verified"},
                            "item_category": {"key": "group1_device", "value": "Device, equipment or object"},
                            "is_military_use": {"key": "no", "value": "No"},
                            "is_component": {"key": "yes_modified", "value": "This has been modified"},
                            "uses_information_security": False,
                            "modified_military_use_details": None,
                            "component_details": "modified details",
                            "information_security_details": None,
                            "missing_document_reason": {
                                "key": "OFFICIAL_SENSITIVE",
                                "value": "Document is above OFFICIAL-SENSITIVE",
                            },
                            "software_or_technology_details": None,
                            "firearm_details": {
                                "type": {"key": "firearms", "value": "Firearms"},
                                "calibre": "0.25",
                                "is_replica": False,
                                "replica_description": None,
                                "category": [
                                    {"key": "NON_AUTOMATIC_SHOTGUN", "value": "Non automatic shotgun"},
                                    {
                                        "key": "NON_AUTOMATIC_RIM_FIRED_HANDGUN",
                                        "value": "Non automatic rim-fired handgun",
                                    },
                                ],
                                "number_of_items": 2,
                                "serial_numbers_available": "AVAILABLE",
                                "serial_numbers": ["12345", "ABC-123"],
                                "is_covered_by_firearm_act_section_one_two_or_five": "Don't know",
                                "is_covered_by_firearm_act_section_one_two_or_five_explanation": "Not covered by firearm act sections",
                            },
                        },
                        "application": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                        "quantity": 444.0,
                        "unit": {"key": "GRM", "value": "Gram(s)"},
                        "value": "444.00",
                        "is_good_incorporated": False,
                        "flags": [],
                        "item_type": None,
                        "other_item_type": None,
                        "end_use_control": ["MEND"],
                        "is_good_controlled": {"key": "False", "value": "No"},
                        "control_list_entries": [
                            {"rating": "ML8a", "text": '"Explosives" and mixtures of explosive substances'},
                            {"rating": "ML9a", "text": 'Naval "vessels" and components'},
                        ],
                        "comment": "test comment",
                        "report_summary": "firearms (2)",
                        "audit_trail": [],
                        "good_application_internal_documents": [],
                        "firearm_details": {
                            "type": {"key": "firearms", "value": "Firearms"},
                            "calibre": "0.25",
                            "is_replica": False,
                            "replica_description": None,
                            "category": [
                                {"key": "NON_AUTOMATIC_SHOTGUN", "value": "Non automatic shotgun"},
                                {
                                    "key": "NON_AUTOMATIC_RIM_FIRED_HANDGUN",
                                    "value": "Non automatic rim-fired handgun",
                                },
                            ],
                            "number_of_items": 2,
                            "serial_numbers_available": "AVAILABLE",
                            "serial_numbers": ["12345", "ABC-123"],
                            "year_of_manufacture": "1990",
                            "is_onward_exported": False,
                            "is_deactivated": False,
                        },
                    },
                    {
                        "id": "6daad1c3-cf97-4aad-b711-d5c9a9f4586e",
                        "good": {
                            "id": "6a7fc61f-698b-46b6-9876-6ac0fddfb1a2",
                            "name": "p2",
                            "description": "444",
                            "part_number": "44",
                            "control_list_entries": [],
                            "comment": None,
                            "is_good_controlled": {"key": "False", "value": "No"},
                            "report_summary": "scale compelling technologies",
                            "flags": [],
                            "documents": [],
                            "is_pv_graded": "no",
                            "grading_comment": None,
                            "pv_grading_details": None,
                            "status": {"key": "verified", "value": "Verified"},
                            "item_category": {"key": "group1_device", "value": "Device, equipment or object"},
                            "is_military_use": {"key": "no", "value": "No"},
                            "is_component": {"key": "no", "value": "No"},
                            "uses_information_security": False,
                            "modified_military_use_details": None,
                            "component_details": None,
                            "information_security_details": None,
                            "missing_document_reason": {
                                "key": "OFFICIAL_SENSITIVE",
                                "value": "Document is above OFFICIAL-SENSITIVE",
                            },
                            "software_or_technology_details": None,
                            "firearm_details": None,
                        },
                        "application": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                        "quantity": 444.0,
                        "unit": {"key": "GRM", "value": "Gram(s)"},
                        "value": "444.00",
                        "is_good_incorporated": False,
                        "flags": [],
                        "item_type": None,
                        "other_item_type": None,
                        "end_use_control": ["MEND"],
                        "is_good_controlled": {"key": "False", "value": "No"},
                        "control_list_entries": [
                            {"rating": "ML8a", "text": '"Explosives" and mixtures of explosive substances'},
                            {"rating": "ML9a", "text": 'Naval "vessels" and components'},
                        ],
                        "comment": "test assesment note",
                        "report_summary": "scale compelling technologies",
                        "audit_trail": [],
                        "good_application_internal_documents": [],
                    },
                ],
                "have_you_been_informed": "no",
                "reference_number_on_information_form": None,
                "activity": "Brokering",
                "usage": None,
                "destinations": {
                    "type": "end_user",
                    "data": {
                        "id": "95d3ea36-6ab9-41ea-a744-7284d17b9cc5",
                        "name": "End User",
                        "address": "44",
                        "country": {
                            "id": "GB",
                            "name": "United Kingdom",
                            "type": "gov.uk Country",
                            "is_eu": True,
                        },
                        "website": "",
                        "type": "end_user",
                        "organisation": "b7175103-d0ae-4b59-9c6a-190a2ed7f5e7",
                        "document": None,
                        "sub_type": {"key": "individual", "value": "Individual"},
                        "sub_type_other": None,
                        "role": {"key": "other", "value": "Other"},
                        "role_other": None,
                        "flags": [],
                        "copy_of": None,
                        "deleted_at": None,
                        "clearance_level": None,
                        "descriptors": None,
                    },
                },
                "additional_documents": [],
                "is_military_end_use_controls": False,
                "military_end_use_controls_ref": None,
                "is_informed_wmd": False,
                "informed_wmd_ref": None,
                "is_suspected_wmd": False,
                "suspected_wmd_ref": None,
                "is_eu_military": False,
                "is_compliant_limitations_eu": None,
                "compliant_limitations_eu_ref": None,
                "intended_end_use": "44",
                "licence": None,
                "is_shipped_waybill_or_lading": False,
                "non_waybill_or_lading_route_details": "44",
                "is_mod_security_approved": None,
                "security_approvals": None,
                "f680_reference_number": None,
                "f1686_contracting_authority": None,
                "is_f1686_approval_document_available": None,
                "f1686_reference_number": None,
                "f1686_approval_date": None,
                "other_security_approval_details": None,
                "is_temp_direct_control": False,
                "temp_direct_control_details": "44",
                "proposed_return_date": "2021-01-01",
                "trade_control_activity": {"key": None, "value": None},
                "trade_control_product_categories": [],
                "denial_matches": [
                    {
                        "id": "a7175133-d0ae-4c59-9c6a-190a2ed7f5e7",
                        "application": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                        "denial": {
                            "id": "e1175133-d0ae-4c59-9c6a-190a2ed7f5e7",
                            "created_by": "",
                            "name": "",
                            "address": "",
                            "reference": "",
                            "notifying_government": "",
                            "final_destination": "",
                            "item_list_codes": "",
                            "item_description": "",
                            "consignee_name": "",
                            "end_use": "",
                            "data": "",
                            "is_revoked": "",
                            "is_revoked_comment": "",
                        },
                        "category": "Partial",
                    },
                    {
                        "id": "c8175133-d0ae-4c59-9c6a-190a2ed7f5e7",
                        "application": "8fb76bed-fd45-4293-95b8-eda9468aa254",
                        "denial": {
                            "id": "f1175133-d0ae-4c59-9c6a-190a2ed7f5e7",
                            "created_by": "",
                            "name": "",
                            "address": "",
                            "reference": "",
                            "notifying_government": "",
                            "final_destination": "",
                            "item_list_codes": "",
                            "item_description": "",
                            "consignee_name": "",
                            "end_use": "",
                            "data": "",
                            "is_revoked": "",
                            "is_revoked_comment": "",
                        },
                        "category": "Exact",
                    },
                ],
                "sanction_matches": [],
                "agreed_to_foi": "True",
                "foi_reason": "internal details",
                "agreed_to_declaration_text": "I AGREE",
            },
            "next_review_date": None,
            "licences": [],
        }
    }


@pytest.fixture
def data_good_on_application(data_standard_case):
    return {
        "id": "0bedd1c3-cf97-4aad-b711-d5c9a9f4586e",
        "good": {
            "id": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
            "description": "444",
            "part_number": "44",
            "control_list_entries": [
                {"rating": "ML4", "text": "Rifle for research and development..."},
                {"rating": "ML5", "text": "Smart ammunition..."},
            ],
            "comment": None,
            "is_good_controlled": {"key": "False", "value": "No"},
            "report_summary": "",
            "flags": [],
            "documents": [],
            "is_pv_graded": "no",
            "grading_comment": None,
            "pv_grading_details": None,
            "status": {"key": "verified", "value": "Verified"},
            "item_category": {"key": "group1_device", "value": "Device, equipment or object"},
            "is_military_use": {"key": "no", "value": "No"},
            "is_component": {"key": "no", "value": "No"},
            "uses_information_security": False,
            "modified_military_use_details": None,
            "component_details": None,
            "information_security_details": None,
            "missing_document_reason": {"key": "OFFICIAL_SENSITIVE", "value": "Document is above OFFICIAL-SENSITIVE"},
            "software_or_technology_details": None,
            "firearm_details": None,
        },
        "application": data_standard_case["case"]["id"],
        "quantity": 444.0,
        "unit": {"key": "GRM", "value": "Gram(s)"},
        "value": "444.00",
        "is_good_incorporated": False,
        "flags": [],
        "item_type": None,
        "other_item_type": None,
        "is_good_controlled": {"key": "True", "value": "Yes"},
        "control_list_entries": [
            {"rating": "ML1", "text": "Smooth-bore weapons..."},
            {"rating": "ML2", "text": "Smooth-bore weapons..."},
        ],
        "end_use_control": ["MEND"],
        "comment": "",
        "report_summary": "",
        "is_precedent": False,
        "good_on_application_documents": [],
        "audit_trail": [
            {
                "id": "86f4d159-a282-4a25-b236-7e3d195356be",
                "created_at": "2020-10-07T15:26:36.976341+01:00",
                "user": {
                    "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                    "first_name": "Richard",
                    "last_name": "Tier",
                    "type": "internal",
                },
                "text": 'good was reviewed: 444 control code changed from "ML1" to "ML1, ML2".',
                "additional_text": "",
            },
            {
                "id": "fcd4f521-18b2-4efc-b011-aac841195a76",
                "created_at": "2020-10-07T15:22:09.786473+01:00",
                "user": {
                    "id": "2a43805b-c082-47e7-9188-c8b3e1a83cb0",
                    "first_name": "Richard",
                    "last_name": "Tier",
                    "type": "internal",
                },
                "text": 'good was reviewed: 444 control code changed from "ML1, ML2" to "ML1".',
                "additional_text": "",
            },
        ],
    }


@pytest.fixture
def firearm_good():
    return {
        "id": "8b730c06-ab4e-401c-aeb0-32b3c92e912c",
        "name": "Bolt action rifle",
        "description": "Action rifle",
        "part_number": "BN-12345",
        "control_list_entries": [{"rating": "ML1a"}, {"rating": "ML22b"}],
        "comment": None,
        "is_good_controlled": {"key": "True", "value": "Yes"},
        "report_summary": "firearms",
        "flags": [],
        "is_pv_graded": {"key": "yes", "value": "Yes"},
        "documents": [
            {
                "id": "6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335",
                "name": "data_sheet.pdf",
                "description": "product data sheet",
                "safe": True,
            }
        ],
        "grading_comment": None,
        "pv_grading_details": {
            "prefix": "NATO",
            "grading": {"key": "official", "value": "Official"},
            "issuing_authority": "Government entity",
            "reference": "GR123",
            "date_of_issue": "2020-02-20",
        },
        "is_document_available": True,
        "no_document_comments": "",
        "is_document_sensitive": False,
        "status": {"key": "verified", "value": "Verified"},
        "item_category": {"key": "group1_device", "value": "Device, equipment or object"},
        "is_military_use": {"key": "no", "value": "No"},
        "is_component": {"key": "no", "value": "No"},
        "uses_information_security": False,
        "modified_military_use_details": None,
        "component_details": None,
        "information_security_details": None,
        "missing_document_reason": {
            "key": "OFFICIAL_SENSITIVE",
            "value": "Document is above OFFICIAL-SENSITIVE",
        },
        "software_or_technology_details": None,
        "firearm_details": {
            "type": {"key": "firearms", "value": "Firearms"},
            "calibre": "0.25",
            "is_replica": False,
            "replica_description": None,
            "category": [
                {"key": "NON_AUTOMATIC_SHOTGUN", "value": "Non automatic shotgun"},
                {
                    "key": "NON_AUTOMATIC_RIM_FIRED_HANDGUN",
                    "value": "Non automatic rim-fired handgun",
                },
            ],
            "number_of_items": 2,
            "serial_numbers_available": "AVAILABLE",
            "serial_numbers": ["12345", "ABC-123"],
        },
    }


@pytest.fixture
def data_countries():
    return {
        "countries": [
            {"id": "AE-AZ", "name": "Abu Dhabi", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AF", "name": "Afghanistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-AJ", "name": "Ajman", "type": "gov.uk Territory", "is_eu": False},
            {"id": "XQZ", "name": "Akrotiri", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AX", "name": "Åland Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AL", "name": "Albania", "type": "gov.uk Country", "is_eu": False},
            {"id": "DZ", "name": "Algeria", "type": "gov.uk Country", "is_eu": False},
            {"id": "AS", "name": "American Samoa", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AD", "name": "Andorra", "type": "gov.uk Country", "is_eu": False},
            {"id": "AO", "name": "Angola", "type": "gov.uk Country", "is_eu": False},
            {"id": "AI", "name": "Anguilla", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AQ", "name": "Antarctica", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AG", "name": "Antigua and Barbuda", "type": "gov.uk Country", "is_eu": False},
            {"id": "AR", "name": "Argentina", "type": "gov.uk Country", "is_eu": False},
            {"id": "AM", "name": "Armenia", "type": "gov.uk Country", "is_eu": False},
            {"id": "AW", "name": "Aruba", "type": "gov.uk Territory", "is_eu": False},
            {"id": "SH-AC", "name": "Ascension", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AU", "name": "Australia", "type": "gov.uk Country", "is_eu": False},
            {"id": "AT", "name": "Austria", "type": "gov.uk Country", "is_eu": True},
            {"id": "AZ", "name": "Azerbaijan", "type": "gov.uk Country", "is_eu": False},
            {"id": "BH", "name": "Bahrain", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-81", "name": "Baker Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "BD", "name": "Bangladesh", "type": "gov.uk Country", "is_eu": False},
            {"id": "BB", "name": "Barbados", "type": "gov.uk Country", "is_eu": False},
            {"id": "BY", "name": "Belarus", "type": "gov.uk Country", "is_eu": False},
            {"id": "BE", "name": "Belgium", "type": "gov.uk Country", "is_eu": True},
            {"id": "BZ", "name": "Belize", "type": "gov.uk Country", "is_eu": False},
            {"id": "BJ", "name": "Benin", "type": "gov.uk Country", "is_eu": False},
            {"id": "BM", "name": "Bermuda", "type": "gov.uk Territory", "is_eu": False},
            {"id": "BT", "name": "Bhutan", "type": "gov.uk Country", "is_eu": False},
            {"id": "BO", "name": "Bolivia", "type": "gov.uk Country", "is_eu": False},
            {"id": "BQ-BO", "name": "Bonaire", "type": "gov.uk Territory", "is_eu": False},
            {"id": "BA", "name": "Bosnia and Herzegovina", "type": "gov.uk Country", "is_eu": False},
            {"id": "BW", "name": "Botswana", "type": "gov.uk Country", "is_eu": False},
            {"id": "BV", "name": "Bouvet Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "BR", "name": "Brazil", "type": "gov.uk Country", "is_eu": False},
            {"id": "BAT", "name": "British Antarctic Territory", "type": "gov.uk Territory", "is_eu": False},
            {"id": "IO", "name": "British Indian Ocean Territory", "type": "gov.uk Territory", "is_eu": False},
            {"id": "VG", "name": "British Virgin Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "BN", "name": "Brunei", "type": "gov.uk Country", "is_eu": False},
            {"id": "BG", "name": "Bulgaria", "type": "gov.uk Country", "is_eu": True},
            {"id": "BF", "name": "Burkina Faso", "type": "gov.uk Country", "is_eu": False},
            {"id": "MM", "name": "Burma", "type": "gov.uk Country", "is_eu": False},
            {"id": "BI", "name": "Burundi", "type": "gov.uk Country", "is_eu": False},
            {"id": "KH", "name": "Cambodia", "type": "gov.uk Country", "is_eu": False},
            {"id": "CM", "name": "Cameroon", "type": "gov.uk Country", "is_eu": False},
            {"id": "CA", "name": "Canada", "type": "gov.uk Country", "is_eu": False},
            {"id": "CV", "name": "Cape Verde", "type": "gov.uk Country", "is_eu": False},
            {"id": "KY", "name": "Cayman Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "CF", "name": "Central African Republic", "type": "gov.uk Country", "is_eu": False},
            {"id": "ES-CE", "name": "Ceuta", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TD", "name": "Chad", "type": "gov.uk Country", "is_eu": False},
            {"id": "CL", "name": "Chile", "type": "gov.uk Country", "is_eu": False},
            {"id": "CN", "name": "China", "type": "gov.uk Country", "is_eu": False},
            {"id": "CX", "name": "Christmas Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "CC", "name": "Cocos (Keeling) Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "CO", "name": "Colombia", "type": "gov.uk Country", "is_eu": False},
            {"id": "KM", "name": "Comoros", "type": "gov.uk Country", "is_eu": False},
            {"id": "CG", "name": "Congo", "type": "gov.uk Country", "is_eu": False},
            {"id": "CD", "name": "Congo (Democratic Republic)", "type": "gov.uk Country", "is_eu": False},
            {"id": "CK", "name": "Cook Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "CR", "name": "Costa Rica", "type": "gov.uk Country", "is_eu": False},
            {"id": "HR", "name": "Croatia", "type": "gov.uk Country", "is_eu": True},
            {"id": "CU", "name": "Cuba", "type": "gov.uk Country", "is_eu": False},
            {"id": "CW", "name": "Curaçao", "type": "gov.uk Territory", "is_eu": False},
            {"id": "CY", "name": "Cyprus", "type": "gov.uk Country", "is_eu": True},
            {"id": "CZ", "name": "Czechia", "type": "gov.uk Country", "is_eu": True},
            {"id": "DK", "name": "Denmark", "type": "gov.uk Country", "is_eu": True},
            {"id": "XXD", "name": "Dhekelia", "type": "gov.uk Territory", "is_eu": False},
            {"id": "DJ", "name": "Djibouti", "type": "gov.uk Country", "is_eu": False},
            {"id": "DM", "name": "Dominica", "type": "gov.uk Country", "is_eu": False},
            {"id": "DO", "name": "Dominican Republic", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-DU", "name": "Dubai", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TL", "name": "East Timor", "type": "gov.uk Country", "is_eu": False},
            {"id": "EC", "name": "Ecuador", "type": "gov.uk Country", "is_eu": False},
            {"id": "EG", "name": "Egypt", "type": "gov.uk Country", "is_eu": False},
            {"id": "SV", "name": "El Salvador", "type": "gov.uk Country", "is_eu": False},
            {"id": "GQ", "name": "Equatorial Guinea", "type": "gov.uk Country", "is_eu": False},
            {"id": "ER", "name": "Eritrea", "type": "gov.uk Country", "is_eu": False},
            {"id": "EE", "name": "Estonia", "type": "gov.uk Country", "is_eu": True},
            {"id": "SZ", "name": "Eswatini", "type": "gov.uk Country", "is_eu": False},
            {"id": "ET", "name": "Ethiopia", "type": "gov.uk Country", "is_eu": False},
            {"id": "FK", "name": "Falkland Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "FO", "name": "Faroe Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "FJ", "name": "Fiji", "type": "gov.uk Country", "is_eu": False},
            {"id": "FI", "name": "Finland", "type": "gov.uk Country", "is_eu": True},
            {"id": "FR", "name": "France", "type": "gov.uk Country", "is_eu": True},
            {"id": "GF", "name": "French Guiana", "type": "gov.uk Territory", "is_eu": False},
            {"id": "PF", "name": "French Polynesia", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TF", "name": "French Southern Territories", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AE-FU", "name": "Fujairah", "type": "gov.uk Territory", "is_eu": False},
            {"id": "GA", "name": "Gabon", "type": "gov.uk Country", "is_eu": False},
            {"id": "GE", "name": "Georgia", "type": "gov.uk Country", "is_eu": False},
            {"id": "DE", "name": "Germany", "type": "gov.uk Country", "is_eu": True},
            {"id": "GH", "name": "Ghana", "type": "gov.uk Country", "is_eu": False},
            {"id": "GI", "name": "Gibraltar", "type": "gov.uk Territory", "is_eu": False},
            {"id": "GR", "name": "Greece", "type": "gov.uk Country", "is_eu": True},
            {"id": "GL", "name": "Greenland", "type": "gov.uk Territory", "is_eu": False},
            {"id": "GD", "name": "Grenada", "type": "gov.uk Country", "is_eu": False},
            {"id": "GP", "name": "Guadeloupe", "type": "gov.uk Territory", "is_eu": False},
            {"id": "GU", "name": "Guam", "type": "gov.uk Territory", "is_eu": False},
            {"id": "GT", "name": "Guatemala", "type": "gov.uk Country", "is_eu": False},
            {"id": "GG", "name": "Guernsey", "type": "gov.uk Territory", "is_eu": False},
            {"id": "GN", "name": "Guinea", "type": "gov.uk Country", "is_eu": False},
            {"id": "GW", "name": "Guinea-Bissau", "type": "gov.uk Country", "is_eu": False},
            {"id": "GY", "name": "Guyana", "type": "gov.uk Country", "is_eu": False},
            {"id": "HT", "name": "Haiti", "type": "gov.uk Country", "is_eu": False},
            {"id": "HM", "name": "Heard Island and McDonald Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "HN", "name": "Honduras", "type": "gov.uk Country", "is_eu": False},
            {"id": "HK", "name": "Hong Kong", "type": "gov.uk Territory", "is_eu": False},
            {"id": "UM-84", "name": "Howland Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "HU", "name": "Hungary", "type": "gov.uk Country", "is_eu": True},
            {"id": "IS", "name": "Iceland", "type": "gov.uk Country", "is_eu": False},
            {"id": "IN", "name": "India", "type": "gov.uk Country", "is_eu": False},
            {"id": "ID", "name": "Indonesia", "type": "gov.uk Country", "is_eu": False},
            {"id": "IR", "name": "Iran", "type": "gov.uk Country", "is_eu": False},
            {"id": "IQ", "name": "Iraq", "type": "gov.uk Country", "is_eu": False},
            {"id": "IE", "name": "Ireland", "type": "gov.uk Country", "is_eu": True},
            {"id": "IM", "name": "Isle of Man", "type": "gov.uk Territory", "is_eu": False},
            {"id": "IL", "name": "Israel", "type": "gov.uk Country", "is_eu": False},
            {"id": "IT", "name": "Italy", "type": "gov.uk Country", "is_eu": True},
            {"id": "CI", "name": "Ivory Coast", "type": "gov.uk Country", "is_eu": False},
            {"id": "JM", "name": "Jamaica", "type": "gov.uk Country", "is_eu": False},
            {"id": "JP", "name": "Japan", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-86", "name": "Jarvis Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "JE", "name": "Jersey", "type": "gov.uk Territory", "is_eu": False},
            {"id": "UM-67", "name": "Johnston Atoll", "type": "gov.uk Territory", "is_eu": False},
            {"id": "JO", "name": "Jordan", "type": "gov.uk Country", "is_eu": False},
            {"id": "KZ", "name": "Kazakhstan", "type": "gov.uk Country", "is_eu": False},
            {"id": "KE", "name": "Kenya", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-89", "name": "Kingman Reef", "type": "gov.uk Territory", "is_eu": False},
            {"id": "KI", "name": "Kiribati", "type": "gov.uk Country", "is_eu": False},
            {"id": "XK", "name": "Kosovo", "type": "gov.uk Country", "is_eu": False},
            {"id": "KW", "name": "Kuwait", "type": "gov.uk Country", "is_eu": False},
            {"id": "KG", "name": "Kyrgyzstan", "type": "gov.uk Country", "is_eu": False},
            {"id": "LA", "name": "Laos", "type": "gov.uk Country", "is_eu": False},
            {"id": "LV", "name": "Latvia", "type": "gov.uk Country", "is_eu": True},
            {"id": "LB", "name": "Lebanon", "type": "gov.uk Country", "is_eu": False},
            {"id": "LS", "name": "Lesotho", "type": "gov.uk Country", "is_eu": False},
            {"id": "LR", "name": "Liberia", "type": "gov.uk Country", "is_eu": False},
            {"id": "LY", "name": "Libya", "type": "gov.uk Country", "is_eu": False},
            {"id": "LI", "name": "Liechtenstein", "type": "gov.uk Country", "is_eu": False},
            {"id": "LT", "name": "Lithuania", "type": "gov.uk Country", "is_eu": True},
            {"id": "LU", "name": "Luxembourg", "type": "gov.uk Country", "is_eu": True},
            {"id": "MO", "name": "Macao", "type": "gov.uk Territory", "is_eu": False},
            {"id": "MG", "name": "Madagascar", "type": "gov.uk Country", "is_eu": False},
            {"id": "MW", "name": "Malawi", "type": "gov.uk Country", "is_eu": False},
            {"id": "MY", "name": "Malaysia", "type": "gov.uk Country", "is_eu": False},
            {"id": "MV", "name": "Maldives", "type": "gov.uk Country", "is_eu": False},
            {"id": "ML", "name": "Mali", "type": "gov.uk Country", "is_eu": False},
            {"id": "MT", "name": "Malta", "type": "gov.uk Country", "is_eu": True},
            {"id": "MH", "name": "Marshall Islands", "type": "gov.uk Country", "is_eu": False},
            {"id": "MQ", "name": "Martinique", "type": "gov.uk Territory", "is_eu": False},
            {"id": "MR", "name": "Mauritania", "type": "gov.uk Country", "is_eu": False},
            {"id": "MU", "name": "Mauritius", "type": "gov.uk Country", "is_eu": False},
            {"id": "YT", "name": "Mayotte", "type": "gov.uk Territory", "is_eu": False},
            {"id": "ES-ML", "name": "Melilla", "type": "gov.uk Territory", "is_eu": False},
            {"id": "MX", "name": "Mexico", "type": "gov.uk Country", "is_eu": False},
            {"id": "FM", "name": "Micronesia", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-71", "name": "Midway Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "MD", "name": "Moldova", "type": "gov.uk Country", "is_eu": False},
            {"id": "MC", "name": "Monaco", "type": "gov.uk Country", "is_eu": False},
            {"id": "MN", "name": "Mongolia", "type": "gov.uk Country", "is_eu": False},
            {"id": "ME", "name": "Montenegro", "type": "gov.uk Country", "is_eu": False},
            {"id": "MS", "name": "Montserrat", "type": "gov.uk Territory", "is_eu": False},
            {"id": "MA", "name": "Morocco", "type": "gov.uk Country", "is_eu": False},
            {"id": "MZ", "name": "Mozambique", "type": "gov.uk Country", "is_eu": False},
            {"id": "NA", "name": "Namibia", "type": "gov.uk Country", "is_eu": False},
            {"id": "NR", "name": "Nauru", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-76", "name": "Navassa Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "NP", "name": "Nepal", "type": "gov.uk Country", "is_eu": False},
            {"id": "NL", "name": "Netherlands", "type": "gov.uk Country", "is_eu": True},
            {"id": "NC", "name": "New Caledonia", "type": "gov.uk Territory", "is_eu": False},
            {"id": "NZ", "name": "New Zealand", "type": "gov.uk Country", "is_eu": False},
            {"id": "NI", "name": "Nicaragua", "type": "gov.uk Country", "is_eu": False},
            {"id": "NE", "name": "Niger", "type": "gov.uk Country", "is_eu": False},
            {"id": "NG", "name": "Nigeria", "type": "gov.uk Country", "is_eu": False},
            {"id": "NU", "name": "Niue", "type": "gov.uk Territory", "is_eu": False},
            {"id": "NF", "name": "Norfolk Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "KP", "name": "North Korea", "type": "gov.uk Country", "is_eu": False},
            {"id": "MK", "name": "North Macedonia", "type": "gov.uk Country", "is_eu": False},
            {"id": "MP", "name": "Northern Mariana Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "NO", "name": "Norway", "type": "gov.uk Country", "is_eu": False},
            {"id": "PS", "name": "Occupied Palestinian Territories", "type": "gov.uk Territory", "is_eu": False},
            {"id": "OM", "name": "Oman", "type": "gov.uk Country", "is_eu": False},
            {"id": "PK", "name": "Pakistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "PW", "name": "Palau", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-95", "name": "Palmyra Atoll", "type": "gov.uk Territory", "is_eu": False},
            {"id": "PA", "name": "Panama", "type": "gov.uk Country", "is_eu": False},
            {"id": "PG", "name": "Papua New Guinea", "type": "gov.uk Country", "is_eu": False},
            {"id": "PY", "name": "Paraguay", "type": "gov.uk Country", "is_eu": False},
            {"id": "PE", "name": "Peru", "type": "gov.uk Country", "is_eu": False},
            {"id": "PH", "name": "Philippines", "type": "gov.uk Country", "is_eu": False},
            {
                "id": "PN",
                "name": "Pitcairn, Henderson, Ducie and Oeno Islands",
                "type": "gov.uk Territory",
                "is_eu": False,
            },
            {"id": "PL", "name": "Poland", "type": "gov.uk Country", "is_eu": True},
            {"id": "PT", "name": "Portugal", "type": "gov.uk Country", "is_eu": True},
            {"id": "PR", "name": "Puerto Rico", "type": "gov.uk Territory", "is_eu": False},
            {"id": "QA", "name": "Qatar", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-RK", "name": "Ras al-Khaimah", "type": "gov.uk Territory", "is_eu": False},
            {"id": "RE", "name": "Réunion", "type": "gov.uk Territory", "is_eu": False},
            {"id": "RO", "name": "Romania", "type": "gov.uk Country", "is_eu": True},
            {"id": "RU", "name": "Russia", "type": "gov.uk Country", "is_eu": False},
            {"id": "RW", "name": "Rwanda", "type": "gov.uk Country", "is_eu": False},
            {"id": "BQ-SA", "name": "Saba", "type": "gov.uk Territory", "is_eu": False},
            {"id": "BL", "name": "Saint Barthélemy", "type": "gov.uk Territory", "is_eu": False},
            {"id": "SH-HL", "name": "Saint Helena", "type": "gov.uk Territory", "is_eu": False},
            {"id": "PM", "name": "Saint Pierre and Miquelon", "type": "gov.uk Territory", "is_eu": False},
            {"id": "MF", "name": "Saint-Martin (French part)", "type": "gov.uk Territory", "is_eu": False},
            {"id": "WS", "name": "Samoa", "type": "gov.uk Country", "is_eu": False},
            {"id": "SM", "name": "San Marino", "type": "gov.uk Country", "is_eu": False},
            {"id": "ST", "name": "Sao Tome and Principe", "type": "gov.uk Country", "is_eu": False},
            {"id": "SA", "name": "Saudi Arabia", "type": "gov.uk Country", "is_eu": False},
            {"id": "SN", "name": "Senegal", "type": "gov.uk Country", "is_eu": False},
            {"id": "RS", "name": "Serbia", "type": "gov.uk Country", "is_eu": False},
            {"id": "SC", "name": "Seychelles", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-SH", "name": "Sharjah", "type": "gov.uk Territory", "is_eu": False},
            {"id": "SL", "name": "Sierra Leone", "type": "gov.uk Country", "is_eu": False},
            {"id": "SG", "name": "Singapore", "type": "gov.uk Country", "is_eu": False},
            {"id": "BQ-SE", "name": "Sint Eustatius", "type": "gov.uk Territory", "is_eu": False},
            {"id": "SX", "name": "Sint Maarten (Dutch part)", "type": "gov.uk Territory", "is_eu": False},
            {"id": "SK", "name": "Slovakia", "type": "gov.uk Country", "is_eu": True},
            {"id": "SI", "name": "Slovenia", "type": "gov.uk Country", "is_eu": True},
            {"id": "SB", "name": "Solomon Islands", "type": "gov.uk Country", "is_eu": False},
            {"id": "SO", "name": "Somalia", "type": "gov.uk Country", "is_eu": False},
            {"id": "ZA", "name": "South Africa", "type": "gov.uk Country", "is_eu": False},
            {
                "id": "GS",
                "name": "South Georgia and South Sandwich Islands",
                "type": "gov.uk Territory",
                "is_eu": False,
            },
            {"id": "KR", "name": "South Korea", "type": "gov.uk Country", "is_eu": False},
            {"id": "SS", "name": "South Sudan", "type": "gov.uk Country", "is_eu": False},
            {"id": "ES", "name": "Spain", "type": "gov.uk Country", "is_eu": True},
            {"id": "LK", "name": "Sri Lanka", "type": "gov.uk Country", "is_eu": False},
            {"id": "KN", "name": "St Kitts and Nevis", "type": "gov.uk Country", "is_eu": False},
            {"id": "LC", "name": "St Lucia", "type": "gov.uk Country", "is_eu": False},
            {"id": "VC", "name": "St Vincent", "type": "gov.uk Country", "is_eu": False},
            {"id": "SD", "name": "Sudan", "type": "gov.uk Country", "is_eu": False},
            {"id": "SR", "name": "Suriname", "type": "gov.uk Country", "is_eu": False},
            {"id": "SJ", "name": "Svalbard and Jan Mayen", "type": "gov.uk Territory", "is_eu": False},
            {"id": "SE", "name": "Sweden", "type": "gov.uk Country", "is_eu": True},
            {"id": "CH", "name": "Switzerland", "type": "gov.uk Country", "is_eu": False},
            {"id": "SY", "name": "Syria", "type": "gov.uk Country", "is_eu": False},
            {"id": "TW", "name": "Taiwan", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TJ", "name": "Tajikistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "TZ", "name": "Tanzania", "type": "gov.uk Country", "is_eu": False},
            {"id": "TH", "name": "Thailand", "type": "gov.uk Country", "is_eu": False},
            {"id": "BS", "name": "The Bahamas", "type": "gov.uk Country", "is_eu": False},
            {"id": "GM", "name": "The Gambia", "type": "gov.uk Country", "is_eu": False},
            {"id": "TG", "name": "Togo", "type": "gov.uk Country", "is_eu": False},
            {"id": "TK", "name": "Tokelau", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TO", "name": "Tonga", "type": "gov.uk Country", "is_eu": False},
            {"id": "TT", "name": "Trinidad and Tobago", "type": "gov.uk Country", "is_eu": False},
            {"id": "SH-TA", "name": "Tristan da Cunha", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TN", "name": "Tunisia", "type": "gov.uk Country", "is_eu": False},
            {"id": "TR", "name": "Turkey", "type": "gov.uk Country", "is_eu": False},
            {"id": "TM", "name": "Turkmenistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "TC", "name": "Turks and Caicos Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "TV", "name": "Tuvalu", "type": "gov.uk Country", "is_eu": False},
            {"id": "UG", "name": "Uganda", "type": "gov.uk Country", "is_eu": False},
            {"id": "UA", "name": "Ukraine", "type": "gov.uk Country", "is_eu": False},
            {"id": "AE-UQ", "name": "Umm al-Quwain", "type": "gov.uk Territory", "is_eu": False},
            {"id": "AE", "name": "United Arab Emirates", "type": "gov.uk Country", "is_eu": False},
            {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
            {"id": "US", "name": "United States", "type": "gov.uk Country", "is_eu": False},
            {"id": "VI", "name": "United States Virgin Islands", "type": "gov.uk Territory", "is_eu": False},
            {"id": "UY", "name": "Uruguay", "type": "gov.uk Country", "is_eu": False},
            {"id": "UZ", "name": "Uzbekistan", "type": "gov.uk Country", "is_eu": False},
            {"id": "VU", "name": "Vanuatu", "type": "gov.uk Country", "is_eu": False},
            {"id": "VA", "name": "Vatican City", "type": "gov.uk Country", "is_eu": False},
            {"id": "VE", "name": "Venezuela", "type": "gov.uk Country", "is_eu": False},
            {"id": "VN", "name": "Vietnam", "type": "gov.uk Country", "is_eu": False},
            {"id": "UM-79", "name": "Wake Island", "type": "gov.uk Territory", "is_eu": False},
            {"id": "WF", "name": "Wallis and Futuna", "type": "gov.uk Territory", "is_eu": False},
            {"id": "EH", "name": "Western Sahara", "type": "gov.uk Territory", "is_eu": False},
            {"id": "YE", "name": "Yemen", "type": "gov.uk Country", "is_eu": False},
            {"id": "ZM", "name": "Zambia", "type": "gov.uk Country", "is_eu": False},
            {"id": "ZW", "name": "Zimbabwe", "type": "gov.uk Country", "is_eu": False},
        ]
    }


@pytest.fixture
def mock_get_countries(requests_mock, data_countries):
    url = client._build_absolute_uri("/static/countries/")
    yield requests_mock.get(url=url, json={"countries": data_countries["countries"]})


@pytest.fixture
def data_organisation():
    expiry_date = datetime.date.today() + datetime.timedelta(days=100)

    return {
        "id": "f65fbf49-c14b-482b-833f-fe39bb26a51d",
        "primary_site": {
            "id": "40f1315e-1283-424a-9295-decf69716379",
            "name": "Headquarters",
            "address": {
                "id": "4966212d-5b52-4a6d-9e06-e589ab9dc221",
                "address_line_1": "42 Question Road",
                "address_line_2": "",
                "city": "London",
                "region": "Greater London",
                "postcode": "SW1A 0AA",
                "country": {"id": "GB", "name": "United Kingdom", "type": "gov.uk Country", "is_eu": True},
            },
            "records_located_at": {
                "id": "40f1315e-1283-424a-9295-decf69716379",
                "name": "Headquarters",
                "address": {
                    "address_line_1": "42 Question Road",
                    "address_line_2": "",
                    "region": "Greater London",
                    "postcode": "SW1A 0AA",
                    "city": "London",
                    "country": {"name": "United Kingdom"},
                },
            },
        },
        "type": {"key": "commercial", "value": "Commercial Organisation"},
        "flags": [
            {
                "id": "6bdbee80-1560-42f8-baca-05bea6f175f4",
                "name": "Org flag",
                "colour": "yellow",
                "label": "Yellow",
                "priority": 0,
                "removable_by": "Anyone",
            },
            {
                "id": "739be3dd-eecc-4303-b4c5-5eadf2476b8c",
                "name": "Org flag 2",
                "colour": "red",
                "label": "Label",
                "priority": 0,
                "removable_by": "Anyone",
            },
        ],
        "status": {"key": "active", "value": "Active"},
        "created_at": "2020-09-29T15:51:03.043852+01:00",
        "updated_at": "2020-09-29T15:51:03.048352+01:00",
        "name": "Archway Communications",
        "eori_number": "1234567890AAA",
        "sic_number": "2345",
        "vat_number": "GB123456789",
        "registration_number": "09876543",
        "documents": [
            {
                "id": "b4a2da59-c0bc-4b6d-8ed9-4ca28ffbf65a",
                "document_type": OrganisationDocumentType.RFD_CERTIFICATE,
                "expiry_date": expiry_date.strftime("%d %B %Y"),
                "reference_code": "RFD123",
                "is_expired": False,
                "document": {
                    "id": "9c2222db-98e5-47e8-9e01-653354e95322",
                    "name": "rfd_certificate.txt",
                    "s3_key": "rfd_certificate.txt.s3_key",
                    "size": 0,
                    "safe": True,
                },
            }
        ],
    }


@pytest.fixture
def organisation_pk(data_organisation):
    return data_organisation["id"]


@pytest.fixture(autouse=True)
def mock_get_organisation(requests_mock, data_organisation, organisation_pk):
    url = client._build_absolute_uri(f"/organisations/{organisation_pk}/")
    yield requests_mock.get(url=url, json=data_organisation)


@pytest.fixture
def mock_organisation_document_post(requests_mock, data_organisation):
    url = client._build_absolute_uri(f"/organisations/{data_organisation['id']}/documents/")
    yield requests_mock.post(url=url, json={}, status_code=201)


@pytest.fixture
def standard_firearm_expected_product_summary():
    return (
        ("firearm-type", "Firearms", "Select the type of firearm product"),
        ("firearm-category", "Non automatic shotgun, Non automatic rim-fired handgun", "Firearm category"),
        ("name", "p1", "Give the product a descriptive name"),
        ("is-good-controlled", "Yes", "Do you know the product's control list entry?"),
        ("control-list-entries", "ML1a, ML22b", "Enter the control list entry"),
        ("is-pv-graded", "Yes", "Does the product have a government security grading or classification?"),
        ("pv-grading-prefix", "NATO", "Enter a prefix (optional)"),
        ("pv-grading-grading", "Official", "What is the security grading or classification?"),
        ("pv-grading-suffix", "SUFFIX", "Enter a suffix (optional)"),
        ("pv-grading-issuing-authority", "Government entity", "Name and address of the issuing authority"),
        ("pv-grading-details-reference", "GR123", "Reference"),
        ("pv-grading-details-date-of-issue", "20 February 2020", "Date of issue"),
        ("calibre", "0.25", "What is the calibre of the product?"),
        ("is-replica", "No", "Is the product a replica firearm?"),
        ("is-registered-firearms-dealer", "No", "Are you a registered firearms dealer?"),
        (
            "firearms-act-1968-section",
            "Don't know",
            "Which section of the Firearms Act 1968 is the product covered by?",
        ),
        (
            "is-covered-by-firearm-act-section-one-two-or-five-explanation",
            "Not covered by firearm act sections",
            "Explain",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s " "designed to do?",
        ),
        ("is-document-sensitive", "No", "Is the document rated above Official-sensitive?"),
        (
            "product-document",
            {
                "description": "product data sheet",
                "id": "6c48a2cc-1ed9-49a5-8ca7-df8af5fc2335",
                "name": "data_sheet.pdf",
                "safe": True,
            },
            "Upload a document that shows what your product is designed to do",
        ),
        ("product-document-description", "product data sheet", "Description (optional)"),
    )


@pytest.fixture
def standard_firearm_expected_product_on_application_summary():
    return (
        ("manufacture-year", "1990", "What year was it made?"),
        ("is-onward-exported", "No", "Will the product be onward exported to any additional countries?"),
        ("is-deactivated", "No", "Has the product been deactivated?"),
        ("number-of-items", 2, "Number of items"),
        ("total-value", "£444.00", "Total value"),
        (
            "has-serial-numbers",
            "Yes, I can add serial numbers now",
            "Will each product have a serial number or other identification marking?",
        ),
        (
            "serial-numbers",
            "\n"
            "\n"
            "\n"
            '    <details class="govuk-details govuk-!-margin-bottom-0" '
            'data-module="govuk-details">\n'
            '        <summary class="govuk-details__summary">\n'
            '            <span class="govuk-details__summary-text">\n'
            "                View serial numbers\n"
            "            </span>\n"
            "        </summary>\n"
            '        <div class="govuk-details__text">\n'
            "            \n"
            "                1. 12345<br>\n"
            "            \n"
            "                2. ABC-123\n"
            "            \n"
            "        </div>\n"
            "    </details>\n"
            "\n",
            "Enter serial numbers or other identification markings",
        ),
    )


@pytest.fixture
def standard_platform_expected_product_summary():
    return (
        (
            "is-firearm-product",
            "No",
            "Is it a firearm product?",
        ),
        (
            "product-category",
            "It's a complete product",
            "Select the product category",
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "part-number",
            "44",
            "Part number",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "uses-information-security",
            "No",
            "Does the product include security features to protect information?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "product-document",
            "link",
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def standard_platform_expected_product_on_application_summary():
    return (
        (
            "is-onward-exported",
            "Yes",
            "Will the product be onward exported to any additional countries?",
        ),
        (
            "is-altered",
            "Yes",
            "Will the item be altered or processed before it is exported again?",
        ),
        (
            "is-altered-comments",
            "Will be altered",
            "Explain how the product will be processed or altered",
        ),
        (
            "is-incorporated",
            "Yes",
            "Will the product be incorporated into another item before it is onward exported?",
        ),
        (
            "is-incorporated-comments",
            "Will be incorporated",
            "Describe what you are incorporating the product into",
        ),
        (
            "number-of-items",
            "444",
            "Number of items",
        ),
        (
            "total-value",
            "£444.00",
            "Total value",
        ),
    )


@pytest.fixture
def standard_component_expected_product_summary():
    return (
        (
            "is-firearm-product",
            "No",
            "Is it a firearm product?",
        ),
        ("product-category", "It forms part of a product", "Select the product category"),
        ("is-material-substance", "No, it's a component, accessory or module", "Is it a material or substance?"),
        ("name", "p1", "Give the product a descriptive name"),
        ("is-component", "Yes", "Is the product a component?"),
        ("component-type", "Modified for hardware", "What type of component is it?"),
        ("modified-details", "modified details", "Provide details of the modifications and the specific hardware"),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "part-number",
            "44",
            "Part number",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "uses-information-security",
            "No",
            "Does the product include security features to protect information?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "product-document",
            "link",
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def standard_component_expected_product_on_application_summary():
    return (
        (
            "is-onward-exported",
            "Yes",
            "Will the product be onward exported to any additional countries?",
        ),
        (
            "is-altered",
            "Yes",
            "Will the item be altered or processed before it is exported again?",
        ),
        (
            "is-altered-comments",
            "Will be altered",
            "Explain how the product will be processed or altered",
        ),
        (
            "is-incorporated",
            "Yes",
            "Will the product be incorporated into another item before it is onward exported?",
        ),
        (
            "is-incorporated-comments",
            "Will be incorporated",
            "Describe what you are incorporating the product into",
        ),
        (
            "number-of-items",
            "444",
            "Number of items",
        ),
        (
            "total-value",
            "£444.00",
            "Total value",
        ),
    )


@pytest.fixture
def standard_material_expected_product_summary():
    return (
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "part-number",
            "44",
            "Part number",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "product-document",
            "link",
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def standard_material_expected_product_on_application_summary():
    return (
        (
            "is-onward-exported",
            "Yes",
            "Will the product be onward exported to any additional countries?",
        ),
        (
            "is-altered",
            "Yes",
            "Will the item be altered or processed before it is exported again?",
        ),
        (
            "is-altered-comments",
            "Will be altered",
            "Explain how the product will be processed or altered",
        ),
        (
            "is-incorporated",
            "Yes",
            "Will the product be incorporated into another item before it is onward exported?",
        ),
        (
            "is-incorporated-comments",
            "Will be incorporated",
            "Describe what you are incorporating the product into",
        ),
        (
            "unit",
            "Gram(s)",
            "Unit of measurement",
        ),
        (
            "quantity",
            "444",
            "Quantity",
        ),
        (
            "total-value",
            "£444.00",
            "Total value",
        ),
    )


@pytest.fixture
def standard_software_expected_product_summary():
    return (
        (
            "is-firearm-product",
            "No",
            "Is it a firearm product?",
        ),
        (
            "non-firearm-category",
            "It helps to operate a product",
            "Select the product category",
        ),
        (
            "name",
            "p1",
            "Give the product a descriptive name",
        ),
        (
            "is-good-controlled",
            "Yes",
            "Do you know the product's control list entry?",
        ),
        (
            "control-list-entries",
            "ML1a, ML22b",
            "Enter the control list entry",
        ),
        (
            "is-pv-graded",
            "Yes",
            "Does the product have a government security grading or classification?",
        ),
        (
            "pv-grading-prefix",
            "NATO",
            "Enter a prefix (optional)",
        ),
        (
            "pv-grading-grading",
            "Official",
            "What is the security grading or classification?",
        ),
        (
            "pv-grading-suffix",
            "SUFFIX",
            "Enter a suffix (optional)",
        ),
        (
            "pv-grading-issuing-authority",
            "Government entity",
            "Name and address of the issuing authority",
        ),
        (
            "pv-grading-details-reference",
            "GR123",
            "Reference",
        ),
        (
            "pv-grading-details-date-of-issue",
            "20 February 2020",
            "Date of issue",
        ),
        (
            "security-features",
            "Yes",
            "Does the product include security features to protect information?",
        ),
        (
            "security-feature-details",
            "security features",
            "Provide details of the information security features",
        ),
        (
            "declared-at-customs",
            "Yes",
            "Will the product be declared at customs?",
        ),
        (
            "has-product-document",
            "Yes",
            "Do you have a document that shows what your product is and what it’s designed to do?",
        ),
        (
            "is-document-sensitive",
            "No",
            "Is the document rated above Official-sensitive?",
        ),
        (
            "design-details",
            "some design details",
            "Describe the product and what it is designed to do",
        ),
        (
            "product-document",
            "link",
            "Upload a document that shows what your product is designed to do",
        ),
        (
            "product-document-description",
            "product data sheet",
            "Description (optional)",
        ),
        (
            "military-use",
            "No",
            "Is the product specially designed or modified for military use?",
        ),
    )


@pytest.fixture
def standard_software_expected_product_on_application_summary():
    return (
        (
            "is-onward-exported",
            "Yes",
            "Will the product be onward exported to any additional countries?",
        ),
        (
            "is-altered",
            "Yes",
            "Will the item be altered or processed before it is exported again?",
        ),
        (
            "is-altered-comments",
            "Will be altered",
            "Explain how the product will be processed or altered",
        ),
        (
            "is-incorporated",
            "Yes",
            "Will the product be incorporated into another item before it is onward exported?",
        ),
        (
            "is-incorporated-comments",
            "Will be incorporated",
            "Describe what you are incorporating the product into",
        ),
        (
            "number-of-items",
            "444",
            "Number of items",
        ),
        (
            "total-value",
            "£444.00",
            "Total value",
        ),
    )
