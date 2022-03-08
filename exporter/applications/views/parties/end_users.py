import logging

from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.functional import cached_property
from django.views.generic import TemplateView, FormView
from formtools.wizard.views import SessionWizardView
from http import HTTPStatus

from exporter.applications.forms.parties import new_party_form_group
from exporter.applications.forms.parties import (
    PartyReuseForm,
    PartySubTypeSelectForm,
    PartyNameForm,
    PartyWebsiteForm,
    PartyAddressForm,
    PartySignatoryNameForm,
    PartyDocuments,
    PartyDocumentUploadForm,
    PartyEnglishTranslationDocumentUploadForm,
    PartyCompanyLetterheadDocumentUploadForm,
)
from exporter.applications.helpers.check_your_answers import convert_party, is_application_export_type_permanent
from exporter.applications.services import (
    copy_party,
    delete_party_document_by_id,
    get_application,
    post_party,
    post_party_document,
    validate_party,
    delete_party,
    get_party,
    update_party,
    delete_party_document_by_id,
)
from exporter.applications.views.parties.base import AddParty, SetParty, DeleteParty, CopyParties, CopyAndSetParty
from exporter.core.constants import OPEN, SetPartyFormSteps, PartyDocumentType
from exporter.core.helpers import (
    NoSaveStorage,
    is_end_user_document_available,
    is_document_in_english,
    is_document_on_letterhead,
    str_to_bool,
)
from lite_content.lite_exporter_frontend.applications import EndUserForm, EndUserPage
from lite_forms.generators import error_page

from core.auth.views import LoginRequiredMixin

log = logging.getLogger(__name__)


class EndUser(LoginRequiredMixin, TemplateView):
    def get(self, request, **kwargs):
        application_id = str(kwargs["pk"])
        application = get_application(request, application_id)
        if application["end_user"]:
            kwargs = {"pk": application_id, "obj_pk": application["end_user"]["id"]}
            return redirect(reverse("applications:end_user_summary", kwargs=kwargs))
        else:
            return redirect(reverse("applications:add_end_user", kwargs={"pk": application_id}))


class AddEndUser(LoginRequiredMixin, AddParty):
    def __init__(self):
        super().__init__(new_url="applications:set_end_user", copy_url="applications:end_users_copy")

    @property
    def back_url(self):
        return reverse("applications:task_list", kwargs={"pk": self.kwargs["pk"]}) + "#end_user"


class SetEndUser(LoginRequiredMixin, SetParty):
    def __init__(self, copy_existing=False):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_user",
            strings=EndUserForm,
            copy_existing=copy_existing,
            post_action=post_party,
            validate_action=validate_party,
        )

    def get_success_url(self):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.object_pk})
        else:
            return reverse(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
            )


class RemoveEndUser(LoginRequiredMixin, DeleteParty):
    def __init__(self):
        super().__init__(
            url="applications:add_end_user",
            action=delete_party,
            error=EndUserPage.DELETE_ERROR,
        )


class CopyEndUsers(LoginRequiredMixin, CopyParties):
    def __init__(self):
        super().__init__(new_party_type="end_user")


class CopyEndUser(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_users_copy",
            strings=EndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )

    def get_success_url(self):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.object_pk})
        else:
            return reverse(
                self.url, kwargs={"pk": self.object_pk, "obj_pk": self.get_validated_data()[self.party_type]["id"]}
            )


class EditEndUser(LoginRequiredMixin, CopyAndSetParty):
    def __init__(self):
        super().__init__(
            url="applications:end_user_attach_document",
            party_type="end_user",
            form=new_party_form_group,
            back_url="applications:end_user",
            strings=EndUserForm,
            validate_action=validate_party,
            post_action=post_party,
        )


class AddEndUserView(LoginRequiredMixin, FormView):
    form_class = PartyReuseForm
    template_name = "core/form.html"

    def form_valid(self, form):
        reuse_party = str_to_bool(form.cleaned_data.get("reuse_party"))
        if reuse_party:
            success_url = reverse("applications:end_users_copy", kwargs=self.kwargs)
        else:
            success_url = reverse("applications:set_end_user", kwargs=self.kwargs)

        return HttpResponseRedirect(success_url)


def _post_party_document(request, application_id, party_id, document_type, document):
    data = {
        "type": document_type,
        "name": getattr(document, "original_name", document.name),
        "s3_key": document.name,
        "size": int(document.size // 1024) if document.size else 0,  # in kilobytes
    }

    response, status_code = post_party_document(request, application_id, party_id, data)
    assert status_code == HTTPStatus.CREATED


class SetPartyView(LoginRequiredMixin, SessionWizardView):
    template_name = "core/form-wizard.html"

    file_storage = NoSaveStorage()

    form_list = [
        (SetPartyFormSteps.PARTY_SUB_TYPE, PartySubTypeSelectForm),
        (SetPartyFormSteps.PARTY_NAME, PartyNameForm),
        (SetPartyFormSteps.PARTY_WEBSITE, PartyWebsiteForm),
        (SetPartyFormSteps.PARTY_ADDRESS, PartyAddressForm),
        (SetPartyFormSteps.PARTY_SIGNATORY_NAME, PartySignatoryNameForm),
        (SetPartyFormSteps.PARTY_DOCUMENTS, PartyDocuments),
        (SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD, PartyDocumentUploadForm),
        (SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD, PartyEnglishTranslationDocumentUploadForm),
        (SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD, PartyCompanyLetterheadDocumentUploadForm),
    ]

    condition_dict = {
        SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(wizard),
        SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD: lambda wizard: is_end_user_document_available(wizard)
        and not is_document_in_english(wizard),
        SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(
            wizard
        )
        and is_document_on_letterhead(wizard),
    }

    @cached_property
    def application(self):
        return get_application(self.request, self.kwargs["pk"])

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if cleaned_data is None:
            return {}
        return cleaned_data

    def get_context_data(self, form, **kwargs):
        context = super().get_context_data(form, **kwargs)
        context["title"] = form.title
        context["hide_step_count"] = True
        context["back_link_text"] = "Back"
        return context

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        if step == SetPartyFormSteps.PARTY_ADDRESS:
            kwargs["request"] = self.request
        if step in (
            SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD,
            SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD,
            SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD,
        ):
            kwargs["edit"] = False

        return kwargs

    def get_success_url(self, party_id):
        raise NotImplementedError("Subclasses must implement get_success_url()")

    def done(self, form_list, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        all_data["type"] = self.party_type
        party_document = all_data.pop("party_document", None)
        party_eng_translation_document = all_data.pop("party_eng_translation_document", None)
        party_letterhead_document = all_data.pop("party_letterhead_document", None)

        response, status_code = post_party(self.request, self.kwargs["pk"], dict(all_data))

        if status_code != HTTPStatus.CREATED:
            log.error(
                "Error creating party - response was: %s - %s",
                status_code,
                response,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error creating party")

        party_id = response[self.party_type]["id"]

        if party_document:
            data = {
                "type": PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT,
                "name": getattr(party_document, "original_name", party_document.name),
                "s3_key": party_document.name,
                "size": int(party_document.size // 1024) if party_document.size else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        if party_eng_translation_document:
            data = {
                "type": PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT,
                "name": getattr(party_eng_translation_document, "original_name", party_eng_translation_document.name),
                "s3_key": party_eng_translation_document.name,
                "size": int(party_eng_translation_document.size // 1024)
                if party_eng_translation_document.size
                else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        if party_letterhead_document:
            data = {
                "type": PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT,
                "name": getattr(party_letterhead_document, "original_name", party_letterhead_document.name),
                "s3_key": party_letterhead_document.name,
                "size": int(party_letterhead_document.size // 1024)
                if party_letterhead_document.size
                else 0,  # in kilobytes
            }

            response, status_code = post_party_document(self.request, str(self.kwargs["pk"]), party_id, data)
            assert status_code == HTTPStatus.CREATED

        return redirect(self.get_success_url(party_id))


class SetEndUserView(SetPartyView):
    party_type = "end_user"

    def get_success_url(self, party_id):
        return reverse("applications:end_user_summary", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})


class CopyEndUserView(SetEndUserView):
    def get_form_initial(self, step):
        initial = copy_party(request=self.request, pk=str(self.kwargs["pk"]), party_pk=str(self.kwargs["obj_pk"]))
        return initial

    def get_success_url(self, party_id):
        if self.application.sub_type == OPEN:
            return reverse("applications:end_user", kwargs={"pk": self.kwargs["pk"]})

        return reverse("applications:end_user_summary", kwargs={"pk": self.kwargs["pk"], "obj_pk": party_id})


class PartyContextMixin:
    template_name = "core/form.html"

    @property
    def application_id(self):
        return str(self.kwargs["pk"])

    @property
    def party_id(self):
        return str(self.kwargs["obj_pk"])

    @property
    def party(self):
        party = get_party(self.request, self.kwargs["pk"], self.kwargs["obj_pk"])
        party_type = list(party.keys())[0]
        return party[party_type]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return {**context, "party": self.party}


class PartySummaryView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    template_name = "applications/party-summary.html"

    def get_success_url(self):
        return "#"


class RemoveEndUserView(LoginRequiredMixin, PartyContextMixin, TemplateView):
    party_type = "end_user"

    def get(self, request, *args, **kwargs):
        status_code = delete_party(self.request, kwargs["pk"], kwargs["obj_pk"])
        if status_code != HTTPStatus.OK:
            return error_page(request, "Error deleting party")

        return redirect(reverse("applications:task_list", kwargs={"pk": kwargs["pk"]}))


class PartyEditMixin(LoginRequiredMixin, PartyContextMixin, FormView):
    def form_valid(self, form):
        update_party(self.request, self.application_id, self.party_id, form.cleaned_data)
        return super().form_valid(form)

    def get_success_url(self):
        return reverse("applications:end_user_summary", kwargs=self.kwargs)


class PartySubTypeEditView(PartyEditMixin):
    form_class = PartySubTypeSelectForm

    def get_initial(self):
        return {"sub_type": self.party["sub_type"]["key"], "sub_type_other": self.party["sub_type_other"]}


class PartyNameEditView(PartyEditMixin):
    form_class = PartyNameForm

    def get_initial(self):
        return {"name": self.party["name"]}


class PartyWebsiteEditView(PartyEditMixin):
    form_class = PartyWebsiteForm

    def get_initial(self):
        return {"website": self.party["website"]}


class PartyAddressEditView(PartyEditMixin):
    form_class = PartyAddressForm

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs["request"] = self.request
        return kwargs

    def get_initial(self):
        return {"address": self.party["address"], "country": self.party["country"]["id"]}


class PartySignatoryEditView(PartyEditMixin):
    form_class = PartySignatoryNameForm

    def get_initial(self):
        return {"signatory_name_euu": self.party["signatory_name_euu"]}


class PartyUndertakingDocumentEditView(LoginRequiredMixin, PartyContextMixin, SessionWizardView):
    template_name = "core/form-wizard.html"
    file_storage = NoSaveStorage()

    form_list = [
        (SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD, PartyDocumentUploadForm),
        (SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD, PartyEnglishTranslationDocumentUploadForm),
        (SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD, PartyCompanyLetterheadDocumentUploadForm),
    ]

    condition_dict = {
        SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD: lambda wizard: is_end_user_document_available(wizard)
        and not is_document_in_english(wizard),
        SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD: lambda wizard: is_end_user_document_available(
            wizard
        )
        and is_document_on_letterhead(wizard),
    }

    def get_form_kwargs(self, step=None):
        kwargs = super().get_form_kwargs(step)

        # get existing document status for the end-user
        self.existing_documents = {document["type"]: document["id"] for document in self.party["documents"]}
        self.english_translation_exists = bool(
            {PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT}.intersection(self.existing_documents.keys())
        )
        self.company_letterhead_document_exists = bool(
            {PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT}.intersection(self.existing_documents.keys())
        )
        if step == SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD:
            kwargs["edit"] = True

        if step == SetPartyFormSteps.PARTY_ENGLISH_TRANSLATION_UPLOAD:
            kwargs["edit"] = self.english_translation_exists

        if step == SetPartyFormSteps.PARTY_COMPANY_LETTERHEAD_DOCUMENT_UPLOAD:
            kwargs["edit"] = self.company_letterhead_document_exists

        return kwargs

    def get_form_initial(self, step):
        if step != SetPartyFormSteps.PARTY_DOCUMENT_UPLOAD:
            return {"end_user_document_available": True}

        document = [
            doc for doc in self.party["documents"] if doc["type"] == PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT
        ]
        if not document:
            raise ValueError("End-user undertaking document not yet uploaded, editing not allowed")

        document = document[0]
        return {
            "end_user_document_available": True,
            "description": document["description"],
            "document_in_english": self.party["document_in_english"],
            "document_on_letterhead": self.party["document_on_letterhead"],
        }

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["hide_step_count"] = True
        # The back_link_url is used for the first form in the sequence. For subsequent forms,
        # the wizard automatically generates the back link to the previous form.
        context["back_link_url"] = reverse("applications:end_user_summary", kwargs=self.kwargs)
        context["back_link_text"] = "Back"
        return context

    def get_cleaned_data_for_step(self, step):
        cleaned_data = super().get_cleaned_data_for_step(step)
        if step == SetPartyFormSteps.PARTY_DOCUMENTS:
            cleaned_data = {"end_user_document_available": True}

        if cleaned_data is None:
            return {}
        return cleaned_data

    def done(self, form_list, **kwargs):
        all_data = {k: v for form in form_list for k, v in form.cleaned_data.items()}
        print(all_data)

        # get updated user choices
        party_document = all_data.pop("party_document", None)
        document_in_english = str_to_bool(all_data.pop("document_in_english", None))
        document_on_letterhead = str_to_bool(all_data.pop("document_on_letterhead", None))
        party_eng_translation_document = all_data.pop("party_eng_translation_document", None)
        party_letterhead_document = all_data.pop("party_letterhead_document", None)

        data = {
            "document_in_english": document_in_english,
            "document_on_letterhead": document_on_letterhead,
        }

        response, status_code = update_party(self.request, self.application_id, self.party_id, data)
        if status_code != HTTPStatus.OK:
            log.error(
                "Error updating party - response was: %s - %s",
                status_code,
                response,
                exc_info=True,
            )
            return error_page(self.request, "Unexpected error updating party")

        # if True then user is uploading new undertaking document
        if party_document:
            _post_party_document(
                self.request,
                self.application_id,
                self.party_id,
                PartyDocumentType.END_USER_UNDERTAKING_DOCUMENT,
                party_document,
            )

        # if True then user choice hasn't changed and uploaded a new translation document
        if party_eng_translation_document:
            _post_party_document(
                self.request,
                self.application_id,
                self.party_id,
                PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT,
                party_eng_translation_document,
            )
        elif document_in_english and self.english_translation_exists:
            # delete existing document
            delete_party_document_by_id(
                self.request,
                self.application_id,
                self.party_id,
                self.existing_documents[PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT],
            )

        if party_letterhead_document:
            _post_party_document(
                self.request,
                self.application_id,
                self.party_id,
                PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT,
                party_letterhead_document,
            )
        elif document_on_letterhead is False and self.company_letterhead_document_exists:
            delete_party_document_by_id(
                self.request,
                self.application_id,
                self.party_id,
                self.existing_documents[PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT],
            )

        return redirect(reverse("applications:end_user_summary", kwargs=self.kwargs))


class PartyDocumentEditView(LoginRequiredMixin, PartyContextMixin, FormView):
    def get_form(self):
        form_kwargs = self.get_form_kwargs()
        if self.kwargs.get("document_type") == "english_translation":
            return PartyEnglishTranslationDocumentUploadForm(edit=True, **form_kwargs)
        elif self.kwargs.get("document_type") == "company_letterhead":
            return PartyCompanyLetterheadDocumentUploadForm(edit=True, **form_kwargs)
        else:
            raise ValueError("Invalid document type encountered")

    def form_valid(self, form):
        if self.kwargs.get("document_type") == "english_translation":
            document = form.cleaned_data["party_eng_translation_document"]
            party_document_type = PartyDocumentType.END_USER_ENGLISH_TRANSLATION_DOCUMENT
        elif self.kwargs.get("document_type") == "company_letterhead":
            document = form.cleaned_data["party_letterhead_document"]
            party_document_type = PartyDocumentType.END_USER_COMPANY_LETTERHEAD_DOCUMENT
        else:
            raise ValueError("Invalid document type encountered")

        data = {
            "type": party_document_type,
            "name": getattr(document, "original_name", document.name),
            "s3_key": document.name,
            "size": int(document.size // 1024) if document.size else 0,  # in kilobytes
        }

        response, status_code = post_party_document(self.request, self.application_id, self.party_id, data)
        assert status_code == HTTPStatus.CREATED
        return super().form_valid(form)

    def get_success_url(self):
        document_type = self.kwargs.pop("document_type")
        return reverse("applications:end_user_summary", kwargs=self.kwargs)
