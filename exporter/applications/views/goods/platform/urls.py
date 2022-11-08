from django.urls import path

from .views import (
    add,
    edit,
    summary,
)


urlpatterns = [
    path("add-new/", add.AddGoodPlatform.as_view(), name="new_good_complete_item"),
    path(
        "<uuid:good_pk>/add-to-application/",
        add.AddGoodPlatformToApplication.as_view(),
        name="new_good_complete_item_to_application",
    ),
    path(
        "<uuid:good_pk>/attach/",
        add.AddGoodPlatformToApplication.as_view(),
        name="attach_complete_item_to_application",
    ),
    path(
        "<uuid:good_pk>/product-summary/",
        summary.PlatformProductSummary.as_view(),
        name="complete_item_product_summary",
    ),
    path(
        "<uuid:good_on_application_pk>/product-on-application-summary/",
        summary.PlatformProductOnApplicationSummary.as_view(),
        name="complete_item_on_application_summary",
    ),
    path("<uuid:good_pk>/edit/name/", edit.PlatformEditName.as_view(), name="complete_item_edit_name"),
    path(
        "<uuid:good_pk>/edit/control-list-entries/",
        edit.PlatformEditControlListEntry.as_view(),
        name="complete_item_edit_control_list_entries",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading/",
        edit.PlatformEditPVGrading.as_view(),
        name="complete_item_edit_pv_grading",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading-details/",
        edit.PlatformEditPVGradingDetails.as_view(),
        name="complete_item_edit_pv_grading_details",
    ),
    path(
        "<uuid:good_pk>/edit/uses-information-security/",
        edit.PlatformEditUsesInformationSecurity.as_view(),
        name="complete_item_edit_uses_information_security",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-availability/",
        edit.PlatformEditProductDocumentAvailability.as_view(),
        name="complete_item_edit_product_document_availability",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-sensitivity/",
        edit.PlatformEditProductDocumentSensitivity.as_view(),
        name="complete_item_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:good_pk>/edit/product-document/",
        edit.PlatformEditProductDocumentView.as_view(),
        name="complete_item_edit_product_document",
    ),
    path(
        "<uuid:good_pk>/edit/product-description/",
        edit.PlatformEditProductDescriptionView.as_view(),
        name="complete_item_edit_product_description",
    ),
    path(
        "<uuid:good_pk>/edit/part-number/",
        edit.PlatformEditPartNumberView.as_view(),
        name="complete_item_edit_part_number",
    ),
    path(
        "<uuid:good_pk>/edit/military-use/",
        edit.PlatformEditMilitaryUseView.as_view(),
        name="complete_item_edit_military_use",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        edit.PlatformOnApplicationSummaryEditOnwardExported.as_view(),
        name="complete_item_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        edit.PlatformOnApplicationSummaryEditOnwardAltered.as_view(),
        name="complete_item_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        edit.PlatformOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="complete_item_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        edit.PlatformOnApplicationSummaryEditQuantityValue.as_view(),
        name="complete_item_on_application_summary_edit_quantity_value",
    ),
]
