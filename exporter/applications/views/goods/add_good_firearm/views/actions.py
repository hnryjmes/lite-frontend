from http import HTTPStatus

from exporter.applications.services import (
    delete_additional_document,
    post_additional_document,
    post_application_document,
)
from exporter.core.constants import DocumentType
from exporter.core.forms import CurrentFile
from exporter.core.helpers import (
    get_document_data,
    get_firearm_act_document,
    get_rfd_certificate,
    has_firearm_act_document,
    has_valid_rfd_certificate,
)
from exporter.organisation.services import (
    delete_document_on_organisation,
    update_document_on_organisation,
)

from .decorators import expect_status


class FirearmActCertificateAction:
    def __init__(self, document_type, view, cleaned_data):
        self.document_type = document_type
        self.view = view
        self.request = view.request
        self.application = view.application
        self.good = view.good
        self.cleaned_data = cleaned_data

    def has_firearm_act_certificate(self):
        attach_firearm_certificate = self.cleaned_data
        return bool(attach_firearm_certificate.get("file"))

    def has_existing_firearm_act_certificate(self):
        return has_firearm_act_document(self.application, self.document_type)

    def has_replacement_file(self):
        file = self.cleaned_data["file"]
        return not isinstance(file, CurrentFile)

    def get_firearm_act_certificate_payload(self):
        data = self.cleaned_data
        certificate = data["file"]
        payload = {
            **get_document_data(certificate),
            "document_on_organisation": {
                "expiry_date": data["section_certificate_date_of_expiry"].isoformat(),
                "reference_code": data["section_certificate_number"],
                "document_type": self.document_type,
            },
        }
        return payload

    @expect_status(
        HTTPStatus.CREATED,
        "Error adding firearm certificate when creating firearm",
        "Unexpected error adding firearm certificate",
    )
    def post_firearm_act_certificate(self):
        firearm_certificate_payload = self.get_firearm_act_certificate_payload()
        return post_application_document(
            request=self.request,
            pk=self.application["id"],
            good_pk=self.good["id"],
            data=firearm_certificate_payload,
        )

    def get_organisation_document_payload(self):
        firearm_certificate_cleaned_data = self.cleaned_data
        expiry_date = firearm_certificate_cleaned_data["section_certificate_date_of_expiry"]
        reference_code = firearm_certificate_cleaned_data["section_certificate_number"]

        firearm_certificate_payload = {
            "expiry_date": expiry_date.isoformat(),
            "reference_code": reference_code,
            "document_type": self.document_type,
        }
        return firearm_certificate_payload

    @expect_status(
        HTTPStatus.OK,
        "Error updating firearm certificate when editing firearm",
        "Unexpected error updating firearm certificate",
    )
    def update_firearm_act_certificate(self):
        document = get_firearm_act_document(self.application, self.document_type)
        document_payload = self.get_organisation_document_payload()
        return update_document_on_organisation(
            request=self.request,
            organisation_id=document["organisation"],
            document_id=document["id"],
            data=document_payload,
        )

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting existing firearm act document",
        "Unexpected error editing firearm",
    )
    def delete_existing_organisation_firearm_act_certificate(self):
        certificate_data = get_firearm_act_document(self.application, self.document_type)
        status_code = delete_document_on_organisation(
            self.request,
            organisation_id=certificate_data["organisation"],
            document_id=certificate_data["id"],
        )
        return {}, status_code

    def run(self):
        if not self.has_firearm_act_certificate():
            return

        if not self.has_existing_firearm_act_certificate():
            self.post_firearm_act_certificate()
            return

        if not self.has_replacement_file():
            self.update_firearm_act_certificate()
            return

        self.delete_existing_organisation_firearm_act_certificate()
        self.post_firearm_act_certificate()


def delete_existing_organisation_rfd_certificate(request, application):
    organisation_rfd_certificate_data = get_rfd_certificate(application)
    status_code = delete_document_on_organisation(
        request,
        organisation_id=organisation_rfd_certificate_data["organisation"],
        document_id=organisation_rfd_certificate_data["id"],
    )
    return {}, status_code


def delete_existing_application_rfd_certificate(request, application):
    organisation_rfd_certificate_data = get_rfd_certificate(application)
    document = organisation_rfd_certificate_data["document"]
    status_code = delete_additional_document(
        request,
        pk=application["id"],
        doc_pk=document["id"],
    )
    return {}, status_code


class IsRfdAction:
    def __init__(self, step_name, wizard):
        self.wizard = wizard
        self.request = wizard.request
        self.application = wizard.application
        self.step_name = step_name

    def is_registered_firearm_dealer(self):
        cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        return cleaned_data["is_registered_firearm_dealer"]

    def has_existing_certificate(self):
        return has_valid_rfd_certificate(self.application)

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting existing rfd certificate on organisation",
        "Unexpected error editing firearm",
    )
    def delete_existing_organisation_rfd_certificate(self):
        return delete_existing_organisation_rfd_certificate(self.request, self.application)

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting existing rfd certificate on application",
        "Unexpected error editing firearm",
    )
    def delete_existing_application_rfd_certificate(self):
        return delete_existing_application_rfd_certificate(self.request, self.application)

    def run(self):
        if self.is_registered_firearm_dealer():
            return

        if not self.has_existing_certificate():
            return

        self.delete_existing_organisation_rfd_certificate()
        self.delete_existing_application_rfd_certificate()


class RfdCertificateAction:
    def __init__(self, step_name, wizard):
        self.wizard = wizard
        self.request = wizard.request
        self.application = wizard.application
        self.step_name = step_name

    def has_organisation_rfd_certificate_data(self):
        return bool(self.wizard.get_cleaned_data_for_step(self.step_name))

    def has_existing_certificate(self):
        return has_valid_rfd_certificate(self.application)

    def get_rfd_certificate_payload(self):
        rfd_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
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

    @expect_status(
        HTTPStatus.CREATED,
        "Error rfd certificate when creating firearm",
        "Unexpected error updating firearm",
    )
    def post_rfd_certificate(self):
        rfd_certificate_payload = self.get_rfd_certificate_payload()
        return post_additional_document(
            request=self.request,
            pk=self.application["id"],
            json=rfd_certificate_payload,
        )

    def has_replacement_file(self):
        attach_rfd_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        file = attach_rfd_certificate_cleaned_data["file"]
        return not isinstance(file, CurrentFile)

    def get_organisation_document_payload(self):
        rfd_certificate_cleaned_data = self.wizard.get_cleaned_data_for_step(self.step_name)
        expiry_date = rfd_certificate_cleaned_data["expiry_date"]
        reference_code = rfd_certificate_cleaned_data["reference_code"]

        rfd_certificate_payload = {
            "expiry_date": expiry_date.isoformat(),
            "reference_code": reference_code,
            "document_type": DocumentType.RFD_CERTIFICATE,
        }
        return rfd_certificate_payload

    @expect_status(
        HTTPStatus.OK,
        "Error updating rfd certificate when creating firearm",
        "Unexpected error updating firearm",
    )
    def update_rfd_certificate(self):
        rfd_document = get_rfd_certificate(self.application)
        rfd_certificate_payload = self.get_organisation_document_payload()
        return update_document_on_organisation(
            request=self.request,
            organisation_id=rfd_document["organisation"],
            document_id=rfd_document["id"],
            data=rfd_certificate_payload,
        )

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting existing rfd certificate on organisation",
        "Unexpected error adding firearm",
    )
    def delete_existing_organisation_rfd_certificate(self):
        return delete_existing_organisation_rfd_certificate(self.request, self.application)

    @expect_status(
        HTTPStatus.NO_CONTENT,
        "Error deleting existing rfd certificate on application",
        "Unexpected error adding firearm",
    )
    def delete_existing_application_rfd_certificate(self):
        return delete_existing_application_rfd_certificate(self.request, self.application)

    def run(self):
        if not self.has_organisation_rfd_certificate_data():
            return

        if not self.has_existing_certificate():
            self.post_rfd_certificate()
            return

        if not self.has_replacement_file():
            self.update_rfd_certificate()
            return

        self.delete_existing_organisation_rfd_certificate()
        self.delete_existing_application_rfd_certificate()
        self.post_rfd_certificate()
