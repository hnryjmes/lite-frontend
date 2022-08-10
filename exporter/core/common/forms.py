from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.choices import Choice
from crispy_forms_gds.layout import HTML, Layout, Submit
from django import forms


class TextChoice(Choice):
    def __init__(self, choice, **kwargs):
        super().__init__(choice.value, choice.label, **kwargs)


def coerce_str_to_bool(val):
    return val == "True"


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                self.helper.attrs = {"enctype": "multipart/form-data"}
                break

        if not hasattr(self.Layout, "SUBTITLE"):
            headings = (HTML.h1(self.Layout.TITLE),)
        else:
            headings = (
                HTML(f'<h1 class="govuk-heading-xl govuk-!-margin-bottom-0">{self.Layout.TITLE}</h1>'),
                HTML(f'<p class="govuk-hint">{self.Layout.SUBTITLE}</p>'),
            )

        self.helper.layout = Layout(*headings, *self.get_layout_fields(), *self.get_layout_actions())

    def get_layout_fields(self):
        raise NotImplementedError(f"Implement `get_layout_fields` on {self.__class__.__name__}")

    def get_layout_actions(self):
        return [
            Submit("submit", getattr(self.Layout, "SUBMIT_BUTTON", "Continue")),
        ]
