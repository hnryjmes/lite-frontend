from django import forms
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Layout, Submit

from core.forms.widgets import GridmultipleSelect


class TAUAssessmentForm(forms.Form):
    """
    This is replacing caseworker.cases.forms.review_goods.ExportControlCharacteristicsForm.

    TODO: Delete ExportControlCharacteristicsForm after this goes live.
    """

    MESSAGE_NO_CLC_MUTEX = "This is mutually exclusive with control list entries"
    MESSAGE_NO_CLC_REQUIRED = "Select a control list entry or select 'This product does not have a control list entry'"

    control_list_entries = forms.MultipleChoiceField(
        label="What is the correct control list entry for this product?",
        help_text="Type to get suggestions. For example ML1a.",
        choices=[],  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
    )

    does_not_have_control_list_entries = forms.BooleanField(
        label="This product does not have a control list entry",
        required=False,
    )

    report_summary = forms.CharField(
        label="Select an annual report summary",
        help_text="Type to get suggestions. For example, components for body armour.",
        # setting id for javascript to use
        widget=forms.TextInput(attrs={"id": "report_summary"}),
    )

    comment = forms.CharField(
        label="Comment (optional)",
        required=False,
        widget=forms.Textarea,
    )

    def __init__(self, goods, control_list_entries_choices, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["control_list_entries"].choices = control_list_entries_choices
        self.fields["goods"] = forms.MultipleChoiceField(
            choices=goods.items(),
            widget=GridmultipleSelect(),
            label="Select the products that you want to assess",
            error_messages={"required": "Select the products that you want to assess"},
        )
        self.helper = FormHelper()
        self.helper.layout = Layout(
            "goods",
            "control_list_entries",
            "does_not_have_control_list_entries",
            "report_summary",
            "comment",
            Submit("submit", "Submit"),
        )

    def clean(self):
        cleaned_data = super().clean()
        has_none = cleaned_data["does_not_have_control_list_entries"]
        has_some = bool(cleaned_data["control_list_entries"])
        if has_none and has_some:
            raise forms.ValidationError({"does_not_have_control_list_entries": self.MESSAGE_NO_CLC_MUTEX})
        elif not has_none and not has_some:
            raise forms.ValidationError({"does_not_have_control_list_entries": self.MESSAGE_NO_CLC_REQUIRED})
        return cleaned_data