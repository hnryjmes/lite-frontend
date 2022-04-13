import logging
import requests

from http import HTTPStatus

from django.conf import settings
from django.http import Http404
from django.shortcuts import redirect
from django.urls import reverse

from core.auth.views import LoginRequiredMixin
from lite_forms.generators import error_page

from exporter.applications.services import (
    get_application,
    post_additional_document,
    post_application_document,
)
from exporter.core.constants import (
    DocumentType,
    FirearmsActDocumentType,
    FirearmsActSections,
)
from exporter.core.helpers import (
    convert_api_date_string_to_date,
    has_valid_rfd_certificate as has_valid_organisation_rfd_certificate,
    get_document_data,
    get_organisation_documents,
    get_rfd_certificate,
)
from exporter.core.wizard.conditionals import C
from exporter.core.wizard.views import BaseSessionWizardView
from exporter.goods.forms.firearms import (
    FirearmAttachFirearmCertificateForm,
    FirearmAttachRFDCertificate,
    FirearmAttachSection5LetterOfAuthorityForm,
    FirearmAttachShotgunCertificateForm,
    FirearmCalibreForm,
    FirearmCategoryForm,
    FirearmDocumentAvailability,
    FirearmDocumentSensitivityForm,
    FirearmDocumentUploadForm,
    FirearmFirearmAct1968Form,
    FirearmNameForm,
    FirearmProductControlListEntryForm,
    FirearmPvGradingForm,
    FirearmPvGradingDetailsForm,
    FirearmRegisteredFirearmsDealerForm,
    FirearmReplicaForm,
    FirearmRFDValidityForm,
    FirearmSection5Form,
)
from exporter.goods.services import (
    post_firearm,
    post_good_documents,
)
from exporter.organisation.services import delete_document_on_organisation

from .conditionals import (
    has_application_rfd_certificate,
    has_firearm_act_document,
    has_organisation_rfd_certificate,
    is_document_sensitive,
    is_product_covered_by_firearm_act_section,
    is_product_document_available,
    is_registered_firearms_dealer,
    is_rfd_certificate_invalid,
    is_pv_graded,
    should_display_is_registered_firearms_dealer_step,
)
from .constants import AddGoodFirearmSteps
from .exceptions import ServiceError
from .payloads import AddGoodFirearmPayloadBuilder


logger = logging.getLogger(__name__)


def get_product_document(good):
    is_document_available = good["is_document_available"]
    is_document_sensitive = good["is_document_sensitive"]
    if not is_document_available or (is_document_available and is_document_sensitive):
        return None

    if not good["documents"]:
        return None

    # when creating new product we can only add one document but we save it as
    # a list because from the product detail page user can add multiple documents
    return good["documents"][0]


class AddGoodFirearm(LoginRequiredMixin, BaseSessionWizardView):
    form_list = [
        (AddGoodFirearmSteps.CATEGORY, FirearmCategoryForm),
        (AddGoodFirearmSteps.NAME, FirearmNameForm),
        (AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY, FirearmProductControlListEntryForm),
        (AddGoodFirearmSteps.PV_GRADING, FirearmPvGradingForm),
        (AddGoodFirearmSteps.PV_GRADING_DETAILS, FirearmPvGradingDetailsForm),
        (AddGoodFirearmSteps.CALIBRE, FirearmCalibreForm),
        (AddGoodFirearmSteps.IS_REPLICA, FirearmReplicaForm),
        (AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID, FirearmRFDValidityForm),
        (AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER, FirearmRegisteredFirearmsDealerForm),
        (AddGoodFirearmSteps.FIREARM_ACT_1968, FirearmFirearmAct1968Form),
        (AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE, FirearmAttachRFDCertificate),
        (AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5, FirearmSection5Form),
        (AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE, FirearmAttachFirearmCertificateForm),
        (AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE, FirearmAttachShotgunCertificateForm),
        (AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY, FirearmAttachSection5LetterOfAuthorityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_AVAILABILITY, FirearmDocumentAvailability),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY, FirearmDocumentSensitivityForm),
        (AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD, FirearmDocumentUploadForm),
    ]
    condition_dict = {
        AddGoodFirearmSteps.PV_GRADING_DETAILS: is_pv_graded,
        AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID: C(has_organisation_rfd_certificate)
        & ~C(has_application_rfd_certificate),
        AddGoodFirearmSteps.IS_REGISTERED_FIREARMS_DEALER: should_display_is_registered_firearms_dealer_step,
        AddGoodFirearmSteps.IS_COVERED_BY_SECTION_5: (
            C(has_organisation_rfd_certificate) & ~C(is_rfd_certificate_invalid)
        )
        | C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.FIREARM_ACT_1968: C(should_display_is_registered_firearms_dealer_step)
        & ~C(is_registered_firearms_dealer),
        AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_1)
        )
        & ~C(has_firearm_act_document(FirearmsActDocumentType.SECTION_1)),
        AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_2)
        )
        & ~C(has_firearm_act_document(FirearmsActDocumentType.SECTION_2)),
        AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY: C(
            is_product_covered_by_firearm_act_section(FirearmsActSections.SECTION_5)
        )
        & ~C(has_firearm_act_document(FirearmsActDocumentType.SECTION_5)),
        AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE: is_registered_firearms_dealer,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_SENSITIVITY: is_product_document_available,
        AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD: C(is_product_document_available) & ~C(is_document_sensitive),
    }

    def dispatch(self, request, *args, **kwargs):
        if not settings.FEATURE_FLAG_PRODUCT_2_0:
            raise Http404

        try:
            self.application = get_application(self.request, self.kwargs["pk"])
        except requests.exceptions.HTTPError:
            raise Http404

        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, form, **kwargs):
        ctx = super().get_context_data(form, **kwargs)

        ctx["hide_step_count"] = True
        ctx["back_link_url"] = reverse(
            "applications:new_good",
            kwargs={
                "pk": self.kwargs["pk"],
            },
        )
        ctx["title"] = form.Layout.TITLE

        return ctx

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == AddGoodFirearmSteps.PRODUCT_CONTROL_LIST_ENTRY:
            kwargs["request"] = self.request

        if step == AddGoodFirearmSteps.PV_GRADING_DETAILS:
            kwargs["request"] = self.request

        if step == AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID:
            kwargs["rfd_certificate"] = get_rfd_certificate(self.application)

        return kwargs

    def has_skipped_firearms_attach_step(self, form_dict, firearm_details, section_value, attach_step_name):
        firearms_act_section = firearm_details["firearms_act_section"]
        return firearms_act_section == section_value and attach_step_name not in form_dict

    def get_payload(self, form_dict):
        payload = AddGoodFirearmPayloadBuilder().build(form_dict)

        firearm_details = payload["firearm_details"]
        if firearm_details.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes":
            for section_value, attach_step_name, document_type in (
                (
                    FirearmsActSections.SECTION_1,
                    AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_1,
                ),
                (
                    FirearmsActSections.SECTION_2,
                    AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_2,
                ),
                (
                    FirearmsActSections.SECTION_5,
                    AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
                    FirearmsActDocumentType.SECTION_5,
                ),
            ):
                if self.has_skipped_firearms_attach_step(form_dict, firearm_details, section_value, attach_step_name):
                    certificate = get_organisation_documents(self.application)[document_type]
                    firearm_details.update(
                        {
                            "section_certificate_missing": False,
                            "section_certificate_number": certificate["reference_code"],
                            "section_certificate_date_of_expiry": convert_api_date_string_to_date(
                                certificate["expiry_date"]
                            ).isoformat(),
                        }
                    )
                    break

        return payload

    def has_organisation_rfd_certificate_data(self):
        return bool(self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE))

    def get_rfd_certificate_payload(self):
        rfd_certificate_cleaned_data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.ATTACH_RFD_CERTIFICATE)
        cert_file = rfd_certificate_cleaned_data["file"]
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            **get_document_data(cert_file),
            "description": "Registered firearm dealer certificate",
            "document_type": DocumentType.RFD_CERTIFICATE,
            "document_on_organisation": {
                "expiry_date": expiry_date.isoformat(),
                "reference_code": reference_code,
                "document_type": DocumentType.RFD_CERTIFICATE,
            },
        }
        return rfd_certificate_payload

    def has_product_documentation(self):
        return self.condition_dict[AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD](self)

    def get_product_document_payload(self):
        data = self.get_cleaned_data_for_step(AddGoodFirearmSteps.PRODUCT_DOCUMENT_UPLOAD)
        document = data["product_document"]
        payload = {
            **get_document_data(document),
            "description": data["description"],
        }
        return payload

    def get_success_url(self, pk, good_pk):
        return reverse(
            "applications:product_summary",
            kwargs={"pk": pk, "good_pk": good_pk},
        )

    def post_firearm(self, form_dict):
        payload = self.get_payload(form_dict)
        api_resp_data, status_code = post_firearm(
            self.request,
            payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error creating firearm - response was: %s - %s",
                "Unexpected error adding firearm",
            )

        application_pk = str(self.kwargs["pk"])
        good_pk = api_resp_data["good"]["id"]

        return application_pk, good_pk

    def has_existing_valid_organisation_rfd_certificate(self, application):
        if not has_valid_organisation_rfd_certificate(application):
            return False

        is_rfd_certificate_valid_cleaned_data = self.get_cleaned_data_for_step(
            AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID
        )
        return is_rfd_certificate_valid_cleaned_data.get("is_rfd_certificate_valid", False)

    def is_existing_organisation_rfd_certificate_invalid(self, application):
        if not has_valid_organisation_rfd_certificate(application):
            return False

        is_rfd_certificate_valid_cleaned_data = self.get_cleaned_data_for_step(
            AddGoodFirearmSteps.IS_RFD_CERTIFICATE_VALID
        )
        return is_rfd_certificate_valid_cleaned_data.get("is_rfd_certificate_valid") is False

    def delete_existing_organisation_rfd_certificate(self, application):
        organisation_rfd_certificate_data = get_rfd_certificate(self.application)
        status_code = delete_document_on_organisation(
            self.request,
            organisation_id=organisation_rfd_certificate_data["organisation"],
            document_id=organisation_rfd_certificate_data["id"],
        )
        if status_code != HTTPStatus.NO_CONTENT:
            raise ServiceError(
                status_code,
                {},
                "Error deleting existing rfd certificate to application - response was: %s - %s",
                "Unexpected error adding firearm",
            )

    def attach_rfd_certificate_to_application(self, application):
        organisation_rfd_certificate_data = get_rfd_certificate(self.application)
        document = organisation_rfd_certificate_data["document"]
        api_resp_data, status_code = post_additional_document(
            self.request,
            pk=application["id"],
            json={
                "name": document["name"],
                "s3_key": document["s3_key"],
                "safe": document["safe"],
                "size": document["size"],
                "document_type": DocumentType.RFD_CERTIFICATE,
                "description": "Registered firearm dealer certificate",
            },
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error attaching existing rfd certificate to application - response was: %s - %s",
                "Unexpected error adding firearm",
            )

    def post_rfd_certificate(self, application):
        rfd_certificate_payload = self.get_rfd_certificate_payload()
        api_resp_data, status_code = post_additional_document(
            request=self.request,
            pk=application["id"],
            json=rfd_certificate_payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error rfd certificate when creating firearm - response was: %s - %s",
                "Unexpected error adding firearm",
            )

    def post_product_documentation(self, good_pk):
        document_payload = self.get_product_document_payload()
        api_resp_data, status_code = post_good_documents(
            request=self.request,
            pk=good_pk,
            json=document_payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error product document when creating firearm - response was: %s - %s",
                "Unexpected error adding document to firearm",
            )

    def has_firearm_act_certificate(self, step_name):
        attach_firearm_certificate = self.get_cleaned_data_for_step(step_name)
        return bool(attach_firearm_certificate.get("file"))

    def get_firearm_act_certificate_payload(self, step_name, document_type):
        data = self.get_cleaned_data_for_step(step_name)
        certificate = data["file"]
        payload = {
            **get_document_data(certificate),
            "document_on_organisation": {
                "expiry_date": data["section_certificate_date_of_expiry"].isoformat(),
                "reference_code": data["section_certificate_number"],
                "document_type": document_type,
            },
        }
        return payload

    def post_firearm_act_certificate(self, step_name, document_type, application_pk, good_pk):
        firearm_certificate_payload = self.get_firearm_act_certificate_payload(step_name, document_type)
        api_resp_data, status_code = post_application_document(
            request=self.request,
            pk=application_pk,
            good_pk=good_pk,
            data=firearm_certificate_payload,
        )
        if status_code != HTTPStatus.CREATED:
            raise ServiceError(
                status_code,
                api_resp_data,
                "Error adding firearm certificate when creating firearm - response was: %s - %s",
                "Unexpected error adding firearm certificate",
            )

    def handle_service_error(self, service_error):
        logger.error(
            service_error.log_message,
            service_error.status_code,
            service_error.response,
            exc_info=True,
        )
        return error_page(self.request, service_error.user_message)

    def done(self, form_list, form_dict, **kwargs):
        try:
            application_pk, good_pk = self.post_firearm(form_dict)

            if self.has_existing_valid_organisation_rfd_certificate(self.application):
                self.attach_rfd_certificate_to_application(self.application)
            else:
                if self.is_existing_organisation_rfd_certificate_invalid(self.application):
                    self.delete_existing_organisation_rfd_certificate(self.application)
                if self.has_organisation_rfd_certificate_data():
                    self.post_rfd_certificate(self.application)

            if self.has_firearm_act_certificate(AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE):
                self.post_firearm_act_certificate(
                    AddGoodFirearmSteps.ATTACH_FIREARM_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_1,
                    application_pk,
                    good_pk,
                )

            if self.has_firearm_act_certificate(AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE):
                self.post_firearm_act_certificate(
                    AddGoodFirearmSteps.ATTACH_SHOTGUN_CERTIFICATE,
                    FirearmsActDocumentType.SECTION_2,
                    application_pk,
                    good_pk,
                )

            if self.has_firearm_act_certificate(AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY):
                self.post_firearm_act_certificate(
                    AddGoodFirearmSteps.ATTACH_SECTION_5_LETTER_OF_AUTHORITY,
                    FirearmsActDocumentType.SECTION_5,
                    application_pk,
                    good_pk,
                )

            if self.has_product_documentation():
                self.post_product_documentation(good_pk)
        except ServiceError as e:
            return self.handle_service_error(e)

        return redirect(self.get_success_url(application_pk, good_pk))