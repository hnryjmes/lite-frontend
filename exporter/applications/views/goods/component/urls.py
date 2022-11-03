from django.urls import path

from .views import (
    add,
    edit,
    summary,
)


urlpatterns = [
    path("add-new/", add.AddGoodComponent.as_view(), name="new_good_component"),
    path(
        "<uuid:good_pk>/add-to-application/",
        add.AddGoodComponentToApplication.as_view(),
        name="new_good_component_to_application",
    ),
    path(
        "<uuid:good_pk>/attach/",
        add.AddGoodComponentToApplication.as_view(),
        name="attach_component_to_application",
    ),
    path(
        "<uuid:good_pk>/product-summary/",
        summary.ComponentProductSummary.as_view(),
        name="component_product_summary",
    ),
    path(
        "<uuid:good_on_application_pk>/product-on-application-summary/",
        summary.ComponentProductOnApplicationSummary.as_view(),
        name="component_on_application_summary",
    ),
    path("<uuid:good_pk>/edit/name/", edit.ComponentEditName.as_view(), name="component_edit_name"),
    path(
        "<uuid:good_pk>/edit/component-details/",
        edit.ComponentEditComponentDetails.as_view(),
        name="component_edit_component_details",
    ),
    path(
        "<uuid:good_pk>/edit/control-list-entries/",
        edit.ComponentEditControlListEntry.as_view(),
        name="component_edit_control_list_entries",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading/",
        edit.ComponentEditPVGrading.as_view(),
        name="component_edit_pv_grading",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading-details/",
        edit.ComponentEditPVGradingDetails.as_view(),
        name="component_edit_pv_grading_details",
    ),
    path(
        "<uuid:good_pk>/edit/uses-information-security/",
        edit.ComponentEditUsesInformationSecurity.as_view(),
        name="component_edit_uses_information_security",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-availability/",
        edit.ComponentEditProductDocumentAvailability.as_view(),
        name="component_edit_product_document_availability",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-sensitivity/",
        edit.ComponentEditProductDocumentSensitivity.as_view(),
        name="component_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:good_pk>/edit/product-document/",
        edit.ComponentEditProductDocumentView.as_view(),
        name="component_edit_product_document",
    ),
    path(
        "<uuid:good_pk>/edit/product-description/",
        edit.ComponentEditProductDescriptionView.as_view(),
        name="component_edit_product_description",
    ),
    path(
        "<uuid:good_pk>/edit/part-number/",
        edit.ComponentEditPartNumberView.as_view(),
        name="component_edit_part_number",
    ),
    path(
        "<uuid:good_pk>/edit/military-use/",
        edit.ComponentEditMilitaryUseView.as_view(),
        name="component_edit_military_use",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        edit.ComponentOnApplicationSummaryEditOnwardExported.as_view(),
        name="component_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        edit.ComponentOnApplicationSummaryEditOnwardAltered.as_view(),
        name="component_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        edit.ComponentOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="component_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        edit.ComponentOnApplicationSummaryEditQuantityValue.as_view(),
        name="component_on_application_summary_edit_quantity_value",
    ),
]
