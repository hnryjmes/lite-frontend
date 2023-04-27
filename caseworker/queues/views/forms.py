from django import forms

from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Field, Fieldset, Submit

from core.forms.utils import coerce_str_to_bool
from caseworker.flags.services import get_flags

SLA_DAYS_RANGE = 99


class AdvancedFiltersFieldset(Fieldset):
    template = "queues/advanced_filters_fieldset.html"


class CasesFiltersForm(forms.Form):

    case_reference = forms.CharField(
        label="Filter by case reference",
        required=False,
    )
    exporter_application_reference = forms.CharField(
        label="Filter by exporter application reference",
        required=False,
    )
    organisation_name = forms.CharField(
        label="Filter by organisation name",
        required=False,
    )
    exporter_site_name = forms.CharField(
        label="Filter by exporter site name",
        required=False,
    )
    exporter_site_address = forms.CharField(
        label="Filter by exporter site address",
        required=False,
    )
    party_name = forms.CharField(
        label="Filter by party name",
        required=False,
    )
    party_address = forms.CharField(
        label="Filter by party address",
        required=False,
    )
    goods_related_description = forms.CharField(
        label="Filter by goods related description",
        required=False,
    )
    country = forms.CharField(
        label="Filter by country",
        required=False,
    )
    control_list_entry = forms.CharField(
        label="Filter by control list entry",
        required=False,
    )
    regime_entry = forms.CharField(
        label="Filter by regime entry",
        required=False,
    )
    submitted_from = DateInputField(
        label="Filter by submitted from date",
        required=False,
    )
    submitted_to = DateInputField(
        label="Filter by submitted to date",
        required=False,
    )
    finalised_from = DateInputField(
        label="Filter by finalised from date",
        required=False,
    )
    finalised_to = DateInputField(
        label="Filter by finalised to date",
        required=False,
    )

    def __init__(self, request, filters_data, *args, **kwargs):
        super().__init__(*args, **kwargs)

        case_type_choices = [("", "Select")] + [
            (choice["key"], choice["value"]) for choice in filters_data["case_types"]
        ]
        case_status_choices = [("", "Select")] + [
            (choice["key"], choice["value"]) for choice in filters_data["statuses"]
        ]
        gov_user_choices = [("", "Select"), ("not_assigned", "Not assigned")] + [
            (choice["id"], choice["full_name"]) for choice in filters_data["gov_users"]
        ]

        advice_type_choices = [("", "Select")] + [
            (choice["key"], choice["value"]) for choice in filters_data["advice_types"]
        ]
        sla_days_choices = [("", "Select")] + [(i, i) for i in range(SLA_DAYS_RANGE)]
        sla_sorted_choices = [("", "Select"), ("ascending", "Ascending"), ("descending", "Descending")]
        nca_choices = [(True, "Filter by Nuclear Cooperation Agreement"), (False, "No")]
        trigger_list_guidelines_choices = [(True, "Yes"), (False, "No")]
        flags_choices = [(flag["id"], flag["name"]) for flag in get_flags(request, disable_pagination=True)]

        self.fields["case_type"] = forms.ChoiceField(
            choices=case_type_choices,
            label="Filter by type",
        )

        self.fields["status"] = forms.ChoiceField(
            choices=case_status_choices,
            label="Filter by status",
        )

        self.fields["case_officer"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Filter by case officer",
        )

        self.fields["assigned_user"] = forms.ChoiceField(
            choices=gov_user_choices,
            label="Filter by assigned user",
        )

        self.fields["team_advice_type"] = forms.ChoiceField(
            label="Filter by team advice type",
            choices=advice_type_choices,
            required=False,
        )

        self.fields["final_advice_type"] = forms.ChoiceField(
            label="Filter by final advice type",
            choices=advice_type_choices,
            required=False,
        )

        self.fields["max_sla_days_remaining"] = forms.ChoiceField(
            label="Filter by max SLA days remaining",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["min_sla_days_remaining"] = forms.ChoiceField(
            label="Filter by min SLA days remaining",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["sla_days_elapsed"] = forms.ChoiceField(
            label="Filter by SLA days elapsed",
            choices=sla_days_choices,
            required=False,
        )

        self.fields["sla_days_elapsed_sort_order"] = forms.ChoiceField(
            label="Filter by sorted by SLA days",
            choices=sla_sorted_choices,
            required=False,
        )
        self.fields["is_nca_applicable"] = forms.TypedChoiceField(
            choices=nca_choices,
            coerce=coerce_str_to_bool,
            label="Filter by Nuclear Cooperation Agreement",
            widget=forms.CheckboxInput(attrs={"class": "govuk-checkboxes--small"}),
            required=False,
        )
        self.fields["is_trigger_list"] = forms.TypedChoiceField(
            choices=trigger_list_guidelines_choices,
            coerce=coerce_str_to_bool,
            label="Filter by Trigger List",
            widget=forms.CheckboxInput(attrs={"class": "govuk-checkboxes--small"}),
            required=False,
        )
        self.fields["flags"] = forms.MultipleChoiceField(
            label="Filter by flags",
            choices=flags_choices,
            required=False,
            # setting id for javascript to use
            widget=forms.SelectMultiple(attrs={"id": "flags"}),
        )

        self.helper = FormHelper()
        self.helper.layout = Layout(
            "case_reference",
            "case_type",
            "status",
            "case_officer",
            "assigned_user",
            AdvancedFiltersFieldset(
                Field.text("exporter_application_reference"),
                Field.text("organisation_name"),
                Field.text("exporter_site_name"),
                Field.text("exporter_site_address"),
                Field.select("team_advice_type"),
                Field.select("final_advice_type"),
                Field.select("max_sla_days_remaining"),
                Field.select("min_sla_days_remaining"),
                Field.select("sla_days_elapsed"),
                Field.select("sla_days_elapsed_sort_order"),
                Field.text("party_name"),
                Field.text("party_address"),
                Field.text("goods_related_description"),
                Field.text("country"),
                Field.text("control_list_entry"),
                Field.text("regime_entry"),
                Field.select("flags"),
                Field("submitted_from"),
                Field("submitted_to"),
                Field("finalised_from"),
                Field("finalised_to"),
                Field("is_nca_applicable"),
                Field("is_trigger_list"),
                legend="Advanced filters",
            ),
        )
