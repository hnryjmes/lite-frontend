from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import HTML, Layout, Submit


from django import forms
from .validators import validate_vat, validate_eori, validate_phone, validate_website


class BaseForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        for field in self.fields.values():
            if isinstance(field, forms.FileField):
                self.helper.attrs = {"enctype": "multipart/form-data"}
                break

        self.helper.layout = Layout(HTML.h1(self.Layout.TITLE), *self.get_layout_fields(), *self.get_layout_actions())

    def get_layout_fields(self):
        raise NotImplementedError(f"Implement `get_layout_fields` on {self.__class__.__name__}")

    def get_layout_actions(self):
        return [
            Submit("submit", getattr(self.Layout, "SUBMIT_BUTTON", "Continue")),
        ]


class RegistrationTypeForm(BaseForm):
    class Layout:
        TITLE = "Commercial organisation or private individual"

    type = forms.ChoiceField(
        choices=(
            ("commercial", "Commercial organisation"),
            ("individual", "Private individual"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select the type of organisation you're registering for",
        },
    )

    def get_layout_fields(self):
        return ("type",)


class RegistrationUKBasedForm(BaseForm):
    class Layout:
        TITLE = "Where is your organisation based?"

    location = forms.ChoiceField(
        choices=(
            ("united_kingdom", "In the United Kingdom"),
            ("abroad", "Outside of the United Kingdom"),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={
            "required": "Select a location",
        },
    )

    def get_layout_fields(self):
        return ("location",)


class RegisterIndividualDetailsForm(BaseForm):
    class Layout:
        TITLE = "Register a private individual"

    name = forms.CharField(
        label="First and last name",
        error_messages={
            "required": "Enter a name",
        },
    )

    eori_number = forms.CharField(
        label="European Union registration and identification number (EORI)",
        error_messages={
            "required": "Enter a EORI number",
        },
        validators=[validate_eori],
    )

    vat_number = forms.CharField(
        required=False, label="UK VAT number This field is (optional)", validators=[validate_vat]
    )

    def get_layout_fields(self):
        return ("name", "eori_number", "vat_number")


class RegisterAddressDetailsForm(BaseForm):
    class Layout:
        TITLE = "Where in the United Kingdom are you based?"

    def __init__(self, is_uk_based, *args, **kwargs):
        self.is_uk_based = is_uk_based
        self.Layout.TITLE = "Where in the United Kingdom are you based?" if self.is_uk_based else "Where are you based?"

        super().__init__(*args, **kwargs)

    name = forms.CharField(
        label="Name of headquarters",
        error_messages={
            "required": "Enter a name for your site",
        },
    )
    address = forms.CharField(
        widget=forms.Textarea(attrs={"rows": "5"}),
        label="Address",
        error_messages={
            "required": "Enter an address",
        },
    )

    address_line_1 = forms.CharField(
        label="Building and street",
        error_messages={
            "required": "Enter a real building and street name",
        },
    )
    address_line_2 = forms.CharField(
        label="",
        required=False,
    )

    city = forms.CharField(
        label="Town or city",
        error_messages={
            "required": "Enter a real city",
        },
    )
    region = forms.CharField(
        label="County or state",
        error_messages={
            "required": "Enter a real region",
        },
    )

    postcode = forms.CharField(
        label="Postcode",
        error_messages={
            "required": "Enter a real postcode",
        },
    )

    phone_number = forms.CharField(
        label="Phone number",
        error_messages={
            "required": "Enter a phone number",
        },
        validators=[validate_phone],
    )

    website = forms.CharField(label="Website", required=False, validators=[validate_website])

    country = forms.CharField(
        label="Country",
        error_messages={
            "required": "Enter a country",
        },
    )

    def clean(self):
        errors_to_remove = (
            {"address", "country"}
            if self.is_uk_based
            else {"address_line_1", "address_line_2", "city", "region", "postcode"}
        )

        for field in errors_to_remove:
            if self.errors.get(field):
                del self.errors[field]
        return

    def get_layout_fields(self):
        if self.is_uk_based:
            return (
                "name",
                "address_line_1",
                "address_line_2",
                "city",
                "region",
                "postcode",
                "phone_number",
                "website",
            )
        else:
            return ("name", "address", "phone_number", "website", "country")
