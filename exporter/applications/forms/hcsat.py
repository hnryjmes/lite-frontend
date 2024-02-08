from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Layout, Submit, HTML
from django.urls import reverse_lazy
from django import forms


class HCSATminiform(forms.Form):
    SAT_CHOICES = [
        ("VERY_DISSATISFIED", "1"),
        ("DISSATISFIED", "2"),
        ("NEUTRAL", "3"),
        ("SATISFIED", "4"),
        ("VERY_SATISFIED", "5"),
    ]

    recommendation = forms.ChoiceField(
        choices=SAT_CHOICES,
        widget=forms.RadioSelect,
        help_text="",
        label="",
        error_messages={"required": "Star rating is required"},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("recommendation"),
            Submit("submit", "Submit feedback"),
        )


class HCSATApplicationForm(HCSATminiform):

    EXPERIENCED_ISSUE = [
        ("NO_ISSUE", "I did not experience any issue"),
        ("UNCLEAR", "The process of submitting my application form was unclear"),
        ("NAVIGATION", "I found it difficult to navigate the service"),
        ("FEATURE", "The service lacks a feature I need"),
        ("SLOW", "The service was slow"),
        ("OTHER", "Other"),
    ]

    other_detail = forms.CharField(
        label="Please specify below",
        widget=forms.Textarea,
        required=False,
    )

    experienced_issue = forms.MultipleChoiceField(
        choices=EXPERIENCED_ISSUE,
        widget=forms.CheckboxSelectMultiple,
        label="Did you experience any of the following issues?",
        help_text="Tick all that apply",
        required=False,
    )

    HELPFUL_GUIDANCE = [
        ("STRONGLY_DISAGREE", "Strongly disagree"),
        ("DISAGREE", "Disagree"),
        ("NEUTRAL", "Neither agree nor disagree"),
        ("AGREE", "Agree"),
        ("STRONGLY_AGREE", "Strongly agree"),
    ]
    helpful_guidance = forms.ChoiceField(
        choices=HELPFUL_GUIDANCE,
        widget=forms.RadioSelect,
        label="To what extent do you agree that the guidance available during the application process was helpful?",
        required=False,
    )

    USER_ACCOUNT_PROCESS = [
        ("VERY_DIFFICULT", "Very difficult"),
        ("DIFFICULT", "Difficult"),
        ("NEUTRAL", "Neither easy nor difficult"),
        ("EASY", "Easy"),
        ("VERY_EASY", "Very easy"),
    ]
    user_account_process = forms.ChoiceField(
        choices=USER_ACCOUNT_PROCESS,
        widget=forms.RadioSelect,
        label="How would you describe the process of creating a user account on this service?",
        required=False,
    )

    service_improvements_feedback = forms.CharField(
        label="How could we improve this service?",
        widget=forms.Textarea,
        help_text="Do not include any personal information, like your name or email address",
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields[
            "recommendation"
        ].help_text = "Overall, how would you rate your experience with the 'apply for a standard individual export licence (SIEL)' service today?"
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Field("recommendation"),
            Field("experienced_issue"),
            Field("other_detail"),
            Field("helpful_guidance"),
            Field("user_account_process"),
            Field("service_improvements_feedback"),
            Submit("submit", "Submit feedback"),
            HTML(f'<a href="{reverse_lazy("core:home")}" class="govuk-button govuk-button--secondary">Cancel</a>'),
        )
