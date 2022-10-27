from django.urls import path

from .views import (
    add,
    edit,
    summary,
)


urlpatterns = [
    path("add-new/", add.AddGoodSoftware.as_view(), name="new_good_software"),
    path(
        "<uuid:good_pk>/add-to-application/",
        add.AddGoodSoftwareToApplication.as_view(),
        name="new_good_software_to_application",
    ),
    path(
        "<uuid:good_pk>/attach/",
        add.AddGoodSoftwareToApplication.as_view(),
        name="attach_software_to_application",
    ),
    path(
        "<uuid:good_pk>/product-summary/",
        summary.SoftwareProductSummary.as_view(),
        name="software_product_summary",
    ),
    path(
        "<uuid:good_on_application_pk>/product-on-application-summary/",
        summary.SoftwareProductOnApplicationSummary.as_view(),
        name="software_on_application_summary",
    ),
    path("<uuid:good_pk>/edit/name/", edit.SoftwareEditName.as_view(), name="software_edit_name"),
    path(
        "<uuid:good_pk>/edit/control-list-entries/",
        edit.SoftwareEditControlListEntry.as_view(),
        name="software_edit_control_list_entries",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading/",
        edit.SoftwareEditPVGrading.as_view(),
        name="software_edit_pv_grading",
    ),
    path(
        "<uuid:good_pk>/edit/pv-grading-details/",
        edit.SoftwareEditPVGradingDetails.as_view(),
        name="software_edit_pv_grading_details",
    ),
    path(
        "<uuid:good_pk>/edit/security-features/",
        edit.SoftwareEditSecurityFeatures.as_view(),
        name="software_edit_security_features",
    ),
    path(
        "<uuid:good_pk>/edit/declared-at-customs/",
        edit.SoftwareEditDeclaredAtCustoms.as_view(),
        name="software_edit_declared_at_customs",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-availability/",
        edit.SoftwareEditProductDocumentAvailability.as_view(),
        name="software_edit_product_document_availability",
    ),
    path(
        "<uuid:good_pk>/edit/product-document-sensitivity/",
        edit.SoftwareEditProductDocumentSensitivity.as_view(),
        name="software_edit_product_document_sensitivity",
    ),
    path(
        "<uuid:good_pk>/edit/product-document/",
        edit.SoftwareEditProductDocumentView.as_view(),
        name="software_edit_product_document",
    ),
    path(
        "<uuid:good_pk>/edit/product-description/",
        edit.SoftwareEditProductDescriptionView.as_view(),
        name="software_edit_product_description",
    ),
    path(
        "<uuid:good_pk>/edit/part-number/",
        edit.SoftwareEditPartNumberView.as_view(),
        name="software_edit_part_number",
    ),
    path(
        "<uuid:good_pk>/edit/military-use/",
        edit.SoftwareEditMilitaryUseView.as_view(),
        name="software_edit_military_use",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-exported/",
        edit.SoftwareOnApplicationSummaryEditOnwardExported.as_view(),
        name="software_on_application_summary_edit_onward_exported",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-altered/",
        edit.SoftwareOnApplicationSummaryEditOnwardAltered.as_view(),
        name="software_on_application_summary_edit_onward_altered",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/onward-incorporated/",
        edit.SoftwareOnApplicationSummaryEditOnwardIncorporated.as_view(),
        name="software_on_application_summary_edit_onward_incorporated",
    ),
    path(
        "<uuid:good_on_application_pk>/<str:summary_type>/edit/quantity-value/",
        edit.SoftwareOnApplicationSummaryEditQuantityValue.as_view(),
        name="software_on_application_summary_edit_quantity_value",
    ),
]
