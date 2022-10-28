from django.urls import path

from .views import (
    add,
    edit,
    summary,
)


urlpatterns = [
    path("add-new/", add.AddGoodMaterial.as_view(), name="new_good_material"),
    path(
        "<uuid:good_pk>/add-to-application/",
        add.AddGoodMaterialToApplication.as_view(),
        name="new_good_material_to_application",
    ),
    path(
        "<uuid:good_pk>/attach/",
        add.AddGoodMaterialToApplication.as_view(),
        name="attach_material_to_application",
    ),
    path(
        "<uuid:good_pk>/product-summary/",
        summary.MaterialProductSummary.as_view(),
        name="material_product_summary",
    ),
    path(
        "<uuid:good_on_application_pk>/product-on-application-summary/",
        summary.MaterialProductOnApplicationSummary.as_view(),
        name="material_on_application_summary",
    ),
    path("<uuid:good_pk>/edit/name/", edit.MaterialEditName.as_view(), name="material_edit_name"),
    path(
        "<uuid:good_pk>/edit/control-list-entries/",
        edit.MaterialEditControlListEntry.as_view(),
        name="material_edit_control_list_entries",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading/",
        edit.MaterialEditPVGrading.as_view(),
        name="material_edit_pv_grading",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading-details/",
        edit.MaterialEditPVGradingDetails.as_view(),
        name="material_edit_pv_grading_details",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-availability/",
        edit.MaterialEditProductDocumentAvailability.as_view(),
        name="material_edit_product_document_availability",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-sensitivity/",
        edit.MaterialEditProductDocumentSensitivity.as_view(),
        name="material_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:good_pk>/edit/product-document/",
        edit.MaterialEditProductDocumentView.as_view(),
        name="material_edit_product_document",
    ),
    path(
        "<uuid:good_pk>/edit/product-description/",
        edit.MaterialEditProductDescriptionView.as_view(),
        name="material_edit_product_description",
    ),
    path(
        "<uuid:good_pk>/edit/part-number/",
        edit.MaterialEditPartNumberView.as_view(),
        name="material_edit_part_number",
    ),
    path(
        "<uuid:good_pk>/edit/military-use/",
        edit.MaterialEditMilitaryUseView.as_view(),
        name="material_edit_military_use",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        edit.MaterialOnApplicationSummaryEditOnwardExported.as_view(),
        name="material_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        edit.MaterialOnApplicationSummaryEditOnwardAltered.as_view(),
        name="material_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        edit.MaterialOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="material_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/unit-quantity-value/",
        edit.MaterialOnApplicationSummaryEditUnitQuantityValue.as_view(),
        name="material_on_application_summary_edit_unit_quantity_value",
    ),
]
