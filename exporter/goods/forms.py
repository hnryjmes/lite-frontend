from crispy_forms_gds.fields import DateInputField
from crispy_forms_gds.helper import FormHelper
from crispy_forms_gds.layout import Field, Fieldset, HTML, Layout, Submit
from django import forms
from django.conf import settings
from django.template.loader import render_to_string
from django.urls import reverse, reverse_lazy
from django.utils import timezone

from exporter.core.helpers import str_to_bool
from exporter.core.constants import PRODUCT_CATEGORY_FIREARM
from core.builtins.custom_tags import linkify
from exporter.core.services import get_control_list_entries
from exporter.core.services import get_pv_gradings
from exporter.goods.helpers import good_summary, get_category_display_string
from lite_content.lite_exporter_frontend.generic import PERMISSION_FINDER_LINK
from lite_content.lite_exporter_frontend import generic
from lite_content.lite_exporter_frontend.goods import (
    CreateGoodForm,
    GoodsQueryForm,
    EditGoodForm,
    DocumentAvailabilityForm,
    DocumentSensitivityForm,
    AttachDocumentForm,
    GoodsList,
    GoodGradingForm,
)
from lite_forms.common import control_list_entries_question
from lite_forms.components import (
    Form,
    HTMLBlock,
    TextArea,
    RadioButtons,
    Option,
    BackLink,
    Custom,
    FileUpload,
    TextInput,
    HiddenField,
    Button,
    DateInput,
    Label,
    Select,
    Group,
    Breadcrumbs,
    FormGroup,
    Heading,
    Checkboxes,
    GroupWithLabel,
)
from lite_forms.helpers import conditional
from lite_forms.styles import ButtonStyle, HeadingStyle


def product_category_form(request):
    return Form(
        title=CreateGoodForm.ProductCategory.TITLE,
        questions=[
            RadioButtons(
                title="",
                name="item_category",
                options=[
                    Option(key="group1_platform", value=CreateGoodForm.ProductCategory.GROUP1_PLATFORM),
                    Option(key="group1_device", value=CreateGoodForm.ProductCategory.GROUP1_DEVICE),
                    Option(key="group1_components", value=CreateGoodForm.ProductCategory.GROUP1_COMPONENTS),
                    Option(key="group1_materials", value=CreateGoodForm.ProductCategory.GROUP1_MATERIALS),
                    Option(key=PRODUCT_CATEGORY_FIREARM, value=CreateGoodForm.ProductCategory.GROUP2_FIREARMS),
                    Option(key="group3_software", value=CreateGoodForm.ProductCategory.GROUP3_SOFTWARE),
                    Option(key="group3_technology", value=CreateGoodForm.ProductCategory.GROUP3_TECHNOLOGY),
                ],
            )
        ],
    )


def software_technology_details_form(request, category_type):
    category_text = get_category_display_string(category_type)

    return Form(
        title=CreateGoodForm.TechnologySoftware.TITLE + category_text,
        questions=[
            HiddenField("is_software_or_technology_step", True),
            TextArea(title="", description="", name="software_or_technology_details", optional=False,),
        ],
    )


def product_military_use_form(request):
    return Form(
        title=CreateGoodForm.MilitaryUse.TITLE,
        questions=[
            HiddenField("is_military_use_step", True),
            RadioButtons(
                title="",
                name="is_military_use",
                options=[
                    Option(key="yes_designed", value=CreateGoodForm.MilitaryUse.YES_DESIGNED),
                    Option(
                        key="yes_modified",
                        value=CreateGoodForm.MilitaryUse.YES_MODIFIED,
                        components=[
                            TextArea(
                                title=CreateGoodForm.MilitaryUse.MODIFIED_MILITARY_USE_DETAILS,
                                description="",
                                name="modified_military_use_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key="no", value=CreateGoodForm.MilitaryUse.NO),
                ],
            ),
        ],
    )


def product_component_form(request):
    return Form(
        title=CreateGoodForm.ProductComponent.TITLE,
        questions=[
            HiddenField("is_component_step", True),
            RadioButtons(
                title="",
                name="is_component",
                options=[
                    Option(
                        key="yes_designed",
                        value=CreateGoodForm.ProductComponent.YES_DESIGNED,
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductComponent.DESIGNED_DETAILS,
                                description="",
                                name="designed_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(
                        key="yes_modified",
                        value=CreateGoodForm.ProductComponent.YES_MODIFIED,
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductComponent.MODIFIED_DETAILS,
                                description="",
                                name="modified_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(
                        key="yes_general",
                        value=CreateGoodForm.ProductComponent.YES_GENERAL_PURPOSE,
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductComponent.GENERAL_DETAILS,
                                description="",
                                name="general_details",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key="no", value=CreateGoodForm.ProductComponent.NO),
                ],
            ),
        ],
    )


def product_uses_information_security(request):
    return Form(
        title=CreateGoodForm.ProductInformationSecurity.TITLE,
        questions=[
            HiddenField("is_information_security_step", True),
            RadioButtons(
                title="",
                name="uses_information_security",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=CreateGoodForm.ProductInformationSecurity.INFORMATION_SECURITY_DETAILS,
                                description="",
                                name="information_security_details",
                                optional=True,
                            ),
                        ],
                    ),
                    Option(key=False, value=CreateGoodForm.ProductInformationSecurity.NO),
                ],
            ),
        ],
    )


def add_goods_questions(control_list_entries, application_pk=None):

    is_good_controlled_description = (
        f"Products that aren't on the {PERMISSION_FINDER_LINK} may be affected by [military end use controls]"
        "(https://www.gov.uk/guidance/export-controls-military-goods-software-and-technology), "
        "[current trade sanctions and embargoes]"
        "(https://www.gov.uk/guidance/current-arms-embargoes-and-other-restrictions) or "
        "[weapons of mass destruction controls](https://www.gov.uk/guidance/supplementary-wmd-end-use-controls). "
        "If the product isn't subject to any controls, you'll get a no licence required (NLR) document from ECJU."
    )

    is_pv_graded_description = (
        "For example, UK OFFICIAL or NATO UNCLASSIFIED. The security grading of the product doesn't affect "
        "if an export licence is needed."
    )

    is_good_controlled_options = [
        Option(
            key=True,
            value="Yes",
            components=[
                control_list_entries_question(
                    control_list_entries=control_list_entries,
                    title="Control list entries",
                    description="Type to get suggestions. For example, ML1a.",
                ),
            ],
        ),
        Option(key=False, value="No"),
    ]

    is_pv_graded_options = [
        Option(key="yes", value="Yes"),
        Option(key="no", value="No, it doesn't need one"),
    ]

    return Form(
        title=conditional(application_pk, "Add a product to your application", "Add a product to your product list"),
        questions=[
            TextInput(
                title="Name",
                description=("Give your product a name so it is easier to find in your product list"),
                name="name",
            ),
            TextArea(title="Description", name="description", extras={"max_length": 280}, rows=5, optional=True,),
            TextInput(title="Part number", name="part_number", optional=True),
            RadioButtons(
                title="Is the product on the control list?",
                description=is_good_controlled_description,
                name="is_good_controlled",
                options=is_good_controlled_options,
            ),
            RadioButtons(
                title="Does the product have a security grading?",
                description=is_pv_graded_description,
                name="is_pv_graded",
                options=is_pv_graded_options,
            ),
        ],
        back_link=conditional(
            application_pk,
            BackLink("Back", reverse_lazy("applications:goods", kwargs={"pk": application_pk})),
            Breadcrumbs(
                [
                    BackLink(generic.SERVICE_NAME, reverse_lazy("core:home")),
                    BackLink(GoodsList.TITLE, reverse_lazy("goods:goods")),
                    BackLink(GoodsList.CREATE_GOOD),
                ]
            ),
        ),
        default_button_name="Continue",
    )


def edit_grading_form(request, good_id):
    return Form(
        title=CreateGoodForm.IsGraded.TITLE,
        description="",
        questions=[
            RadioButtons(
                name="is_pv_graded",
                options=[
                    Option(key="yes", value=CreateGoodForm.IsGraded.YES, components=pv_details_form(request).questions),
                    Option(key="no", value=CreateGoodForm.IsGraded.NO),
                ],
            )
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def pv_details_form(request):
    return Form(
        title=GoodGradingForm.TITLE,
        description=GoodGradingForm.DESCRIPTION,
        questions=[
            Heading("PV grading", HeadingStyle.M),
            Group(
                id="pv-gradings-group",
                components=[
                    TextInput(title=GoodGradingForm.PREFIX, name="prefix", optional=True),
                    Select(
                        options=get_pv_gradings(request, convert_to_options=True),
                        title=GoodGradingForm.GRADING,
                        name="grading",
                        optional=True,
                    ),
                    TextInput(title=GoodGradingForm.SUFFIX, name="suffix", optional=True),
                ],
                classes=["app-pv-grading-inputs"],
            ),
            TextInput(title=GoodGradingForm.OTHER_GRADING, name="custom_grading", optional=True),
            TextInput(title=GoodGradingForm.ISSUING_AUTHORITY, name="issuing_authority"),
            TextInput(title=GoodGradingForm.REFERENCE, name="reference"),
            DateInput(
                title=GoodGradingForm.DATE_OF_ISSUE, prefix="date_of_issue", name="date_of_issue", optional=False
            ),
        ],
        default_button_name=GoodGradingForm.BUTTON,
    )


def add_good_form_group(
    request,
    application: dict = None,
    is_pv_graded: bool = None,
    is_software_technology: bool = None,
    is_firearm: bool = None,
    is_firearm_ammunition_or_component: bool = None,
    is_firearms_accessory: bool = None,
    is_firearms_software_or_tech: bool = None,
    show_serial_numbers_form: bool = False,
    draft_pk: str = None,
    base_form_back_link: str = None,
    is_rfd: bool = False,
):
    application = application or {}

    control_list_entries = get_control_list_entries(request, convert_to_options=True)
    is_category_firearms = (
        request.POST.get("item_category") == PRODUCT_CATEGORY_FIREARM
        or settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS
    )

    show_attach_rfd = str_to_bool(request.POST.get("is_registered_firearm_dealer"))
    is_preexisting = str_to_bool(request.GET.get("preexisting", False))
    # when adding to product list then always show RFD question if not yet have a valid RFD certificate
    # when adding to application then show RFD question if has expired RFD and not show if they do not have one yet
    if is_preexisting:
        show_rfd_question = is_firearm_ammunition_or_component and has_expired_rfd_certificate(application)
    else:
        show_rfd_question = is_firearm_ammunition_or_component and not has_valid_rfd_certificate(application)

    return FormGroup(
        [
            conditional(not settings.FEATURE_FLAG_ONLY_ALLOW_FIREARMS_PRODUCTS, product_category_form(request)),
            conditional(is_category_firearms, group_two_product_type_form(back_link=base_form_back_link),),
            conditional(
                is_firearm_ammunition_or_component and draft_pk, firearms_number_of_items(request.POST.get("type"))
            ),
            conditional(is_firearm_ammunition_or_component and draft_pk, identification_markings_form()),
            conditional(
                is_firearm_ammunition_or_component and draft_pk and show_serial_numbers_form,
                firearms_capture_serial_numbers(request.POST.get("number_of_items", 0)),
            ),
            conditional(not is_category_firearms, product_military_use_form(request)),
            conditional(not is_category_firearms, product_uses_information_security(request)),
            add_goods_questions(control_list_entries, draft_pk),
            conditional(is_pv_graded, pv_details_form(request)),
            # only ask if adding to a draft application
            conditional(is_firearm and bool(draft_pk), firearm_year_of_manufacture_details_form()),
            conditional(is_firearm, firearm_replica_form(request.POST.get("type"))),
            conditional(is_firearm_ammunition_or_component, firearm_calibre_details_form()),
            conditional(show_rfd_question, is_registered_firearm_dealer_field(base_form_back_link)),
            conditional(show_attach_rfd, attach_firearm_dealer_certificate_form(base_form_back_link)),
            conditional(is_firearm_ammunition_or_component and bool(draft_pk), firearms_act_confirmation_form(is_rfd)),
            conditional(
                is_firearms_software_or_tech, software_technology_details_form(request, request.POST.get("type"))
            ),
            conditional(is_firearms_accessory or is_firearms_software_or_tech, product_military_use_form(request)),
            conditional(is_firearms_accessory, product_component_form(request)),
            conditional(
                is_firearms_accessory or is_firearms_software_or_tech, product_uses_information_security(request)
            ),
        ]
    )


def edit_good_detail_form(request, good_id):
    return Form(
        title=EditGoodForm.TITLE,
        description=EditGoodForm.DESCRIPTION,
        questions=[
            TextInput(
                title="Name",
                description=("Give your product a name so it is easier to find in your product list"),
                name="name",
            ),
            TextArea(
                title=EditGoodForm.Description.TITLE,
                name="description",
                rows=5,
                optional=True,
                extras={"max_length": 280},
            ),
            TextInput(title=EditGoodForm.PartNumber.TITLE, name="part_number", optional=True),
            RadioButtons(
                title=EditGoodForm.IsControlled.TITLE,
                description=EditGoodForm.IsControlled.DESCRIPTION,
                name="is_good_controlled",
                options=[
                    Option(
                        key=True,
                        value=EditGoodForm.IsControlled.YES,
                        components=[
                            control_list_entries_question(
                                control_list_entries=get_control_list_entries(request, convert_to_options=True),
                                title=EditGoodForm.ControlListEntry.TITLE,
                                description=EditGoodForm.ControlListEntry.DESCRIPTION,
                            ),
                        ],
                    ),
                    Option(key=False, value=EditGoodForm.IsControlled.NO),
                ],
            ),
        ],
        back_link=BackLink(CreateGoodForm.BACK_BUTTON, reverse_lazy("goods:good", kwargs={"pk": good_id})),
    )


def check_document_available_form(back_url):
    return Form(
        title=DocumentAvailabilityForm.TITLE,
        description=DocumentAvailabilityForm.DESCRIPTION,
        questions=[
            RadioButtons(
                name="is_document_available",
                options=[
                    Option(key="yes", value=DocumentSensitivityForm.Options.YES),
                    Option(
                        key="no",
                        value=DocumentSensitivityForm.Options.NO,
                        components=[
                            TextArea(
                                title=DocumentAvailabilityForm.NO_DOCUMENT_TEXTFIELD_DESCRIPTION,
                                description=None,
                                name="no_document_comments",
                                optional=False,
                            ),
                        ],
                    ),
                ],
            ),
        ],
        back_link=BackLink("Back", back_url),
        default_button_name=DocumentAvailabilityForm.SUBMIT_BUTTON,
    )


def document_grading_form(back_url):
    return Form(
        title=DocumentSensitivityForm.TITLE,
        questions=[
            RadioButtons(
                name="is_document_sensitive",
                options=[
                    Option(
                        key="yes",
                        value=DocumentSensitivityForm.Options.YES,
                        components=[Label(text=DocumentSensitivityForm.ECJU_HELPLINE)],
                    ),
                    Option(key="no", value=DocumentSensitivityForm.Options.NO,),
                ],
            ),
        ],
        back_link=BackLink("Back", back_url),
        default_button_name=DocumentSensitivityForm.SUBMIT_BUTTON,
    )


def attach_documents_form(back_link):
    return Form(
        title=AttachDocumentForm.TITLE,
        description=AttachDocumentForm.DESCRIPTION,
        questions=[
            FileUpload(),
            TextArea(
                title=AttachDocumentForm.Description.TITLE,
                optional=True,
                name="description",
                extras={"max_length": 280},
            ),
        ],
        buttons=[Button(AttachDocumentForm.BUTTON, "submit")],
        back_link=back_link,
    )


def raise_a_goods_query(good_id, raise_a_clc: bool, raise_a_pv: bool):
    questions = []

    if raise_a_clc:
        if GoodsQueryForm.CLCQuery.TITLE:
            questions += [
                Heading(GoodsQueryForm.CLCQuery.TITLE, HeadingStyle.M),
            ]
        questions += [
            TextInput(
                title=GoodsQueryForm.CLCQuery.Code.TITLE,
                description=GoodsQueryForm.CLCQuery.Code.DESCRIPTION,
                name="clc_control_code",
                optional=True,
            ),
            TextArea(title=GoodsQueryForm.CLCQuery.Details.TITLE, name="clc_raised_reasons", optional=True,),
        ]

    if raise_a_pv:
        if GoodsQueryForm.PVGrading.TITLE:
            questions += [
                Heading(GoodsQueryForm.PVGrading.TITLE, HeadingStyle.M),
            ]
        questions += [
            TextArea(title=GoodsQueryForm.PVGrading.Details.TITLE, name="pv_grading_raised_reasons", optional=True,),
        ]

    return Form(
        title=GoodsQueryForm.TITLE,
        description=GoodsQueryForm.DESCRIPTION,
        questions=questions,
        back_link=BackLink(GoodsQueryForm.BACK_LINK, reverse("goods:good", kwargs={"pk": good_id})),
        default_button_name="Save",
    )


def delete_good_form(good):
    return Form(
        title=EditGoodForm.DeleteConfirmationForm.TITLE,
        questions=[good_summary(good)],
        buttons=[
            Button(value=EditGoodForm.DeleteConfirmationForm.YES, action="submit", style=ButtonStyle.WARNING),
            Button(
                value=EditGoodForm.DeleteConfirmationForm.NO,
                action="",
                style=ButtonStyle.SECONDARY,
                link=reverse_lazy("goods:good", kwargs={"pk": good["id"]}),
            ),
        ],
    )


def group_two_product_type_form(back_link=None):
    form = Form(
        title=CreateGoodForm.FirearmGood.ProductType.TITLE,
        questions=[
            HiddenField("product_type_step", True),
            RadioButtons(
                title="",
                name="type",
                options=[
                    Option(key="firearms", value=CreateGoodForm.FirearmGood.ProductType.FIREARM),
                    Option(key="ammunition", value=CreateGoodForm.FirearmGood.ProductType.AMMUNITION),
                    Option(
                        key="components_for_firearms",
                        value=CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_FIREARM,
                    ),
                    Option(
                        key="components_for_ammunition",
                        value=CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_AMMUNITION,
                    ),
                    Option(key="firearms_accessory", value=CreateGoodForm.FirearmGood.ProductType.FIREARMS_ACCESSORY),
                    Option(
                        key="software_related_to_firearms",
                        value=CreateGoodForm.FirearmGood.ProductType.SOFTWARE_RELATED_TO_FIREARM,
                    ),
                    Option(
                        key="technology_related_to_firearms",
                        value=CreateGoodForm.FirearmGood.ProductType.TECHNOLOGY_RELATED_TO_FIREARM,
                    ),
                ],
            ),
        ],
        default_button_name=CreateGoodForm.FirearmGood.ProductType.BUTTON_TEXT,
    )

    if back_link:
        form.back_link = BackLink("Back", back_link)

    return form


def firearms_number_of_items(firearm_type):
    return Form(
        title="Number of items",
        questions=[
            HiddenField("type", firearm_type),
            HiddenField("number_of_items_step", True),
            TextInput(name="number_of_items"),
        ],
        default_button_name="Continue",
    )


def firearms_capture_serial_numbers(number_of_items):
    if isinstance(number_of_items, str):
        try:
            number_of_items = int(number_of_items)
        except ValueError:
            number_of_items = 0
    elif number_of_items is None:
        number_of_items = 0

    questions = [
        HiddenField("capture_serial_numbers_step", True),
        HiddenField("number_of_items", number_of_items),
        Label(text=f"Number of items: {number_of_items}"),
    ]

    input_fields = [
        Group(
            id="serial_number_input_field_group",
            components=[Label(text=f"{i+1}"), TextInput(name=f"serial_number_input_{i}")],
            classes=["lite-input-with-label"],
        )
        for i in range(number_of_items)
    ]

    questions.append(GroupWithLabel(id="serial_numbers", components=input_fields))

    return Form(
        title="Enter the serial numbers for this product",
        description="Enter one serial number in every row",
        questions=questions,
        default_button_name="Save and continue",
    )


def firearm_year_of_manufacture_details_form(good_id=None):
    return Form(
        title="What is the year of manufacture of the firearm?",
        default_button_name="Continue",
        questions=list(
            filter(
                bool,
                [
                    HiddenField("good_id", good_id) if good_id else None,
                    HiddenField("firearm_year_of_manufacture_step", True),
                    TextInput(description="", name="year_of_manufacture", optional=False,),
                ],
            )
        ),
    )


def firearm_replica_form(firearm_type):
    return Form(
        title=CreateGoodForm.FirearmGood.FirearmsReplica.TITLE,
        default_button_name="Save and continue",
        questions=[
            HiddenField("type", firearm_type),
            HiddenField("is_replica_step", True),
            RadioButtons(
                title="",
                name="is_replica",
                options=[
                    Option(
                        key=True,
                        value="Yes",
                        components=[
                            TextArea(
                                title=CreateGoodForm.FirearmGood.FirearmsReplica.DESCRIPTION,
                                description="",
                                name="replica_description",
                                optional=False,
                            ),
                        ],
                    ),
                    Option(key=False, value="No",),
                ],
            ),
        ],
    )


def firearm_calibre_details_form():
    return Form(
        title="What is the calibre of the product?",
        default_button_name="Save and continue",
        questions=[
            HiddenField("firearm_calibre_step", True),
            TextInput(title="", description="", name="calibre", optional=False,),
        ],
    )


def format_list_item(link, name, description):
    return "<br>" + "<li>" + linkify(link, name=name,) + f"&nbsp;&nbsp;{description}" + "</li>"


def firearms_act_confirmation_form(is_rfd):

    if is_rfd:
        # RFD certificate covers sections 1 and 2 hence only ask for section 5
        section1_list_item = ""
        section2_list_item = ""
        title = "Is the product covered by section 5 of the Firearms Act 1968?"
        sections_title = "What does section 5 cover?"
        section_options = []
    else:
        title = CreateGoodForm.FirearmGood.FirearmsActCertificate.TITLE
        sections_title = "What do these sections cover?"
        section1_list_item = format_list_item(
            CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE_LINK,
            CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE,
            "  is a broad category covering most types of firearm and ammunition, including rifles and high powered air weapons.",
        )
        section2_list_item = format_list_item(
            CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO_LINK,
            CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO,
            "  covers most types of shotgun.",
        )
        section_options = [
            RadioButtons(
                title="Select section",
                name="firearms_act_section",
                options=[
                    Option(key="firearms_act_section1", value="Section 1"),
                    Option(key="firearms_act_section2", value="Section 2"),
                    Option(key="firearms_act_section5", value="Section 5"),
                ],
            )
        ]

    return Form(
        title=title,
        default_button_name="Save and continue",
        questions=[
            HiddenField("section_certificate_step", True),
            HTMLBlock(
                "<br>"
                + "<details class='govuk-details' data-module='govuk-details'>"
                + "<summary class='govuk-details__summary'>"
                + f"    <span class='govuk-details__summary-text'>{sections_title}</span>"
                + "</summary>"
                + "<div class='govuk-details__text govuk-!-padding-top-0'>"
                + " <ol class='govuk-list'>"
                + section1_list_item
                + section2_list_item
                + format_list_item(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                    "  covers weapons and ammunition that are generally prohibited.",
                )
                + "</ol>"
                + "</div>"
                + "</details>"
                "<br>"
            ),
            RadioButtons(
                title="",
                name="is_covered_by_firearm_act_section_one_two_or_five",
                options=[
                    Option(
                        key="Yes",
                        value=CreateGoodForm.FirearmGood.FirearmsActCertificate.YES,
                        components=section_options,
                    ),
                    Option(key="No", value=CreateGoodForm.FirearmGood.FirearmsActCertificate.NO),
                    Option(key="Unsure", value=CreateGoodForm.FirearmGood.FirearmsActCertificate.DONT_KNOW),
                ],
            ),
        ],
        javascript_imports={"/javascripts/add-good.js"},
    )


def upload_firearms_act_certificate_form(section, filename, back_link):
    return Form(
        title=f"Attach your Firearms Act 1968 {section} certificate",
        description="The file must be smaller than 50MB",
        questions=[
            HiddenField("firearms_certificate_uploaded", False),
            FileUpload(),
            HiddenField("uploaded_file_name", filename),
            TextInput(
                title=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_CERTIFICATE_NUMBER,
                description="",
                name="section_certificate_number",
                optional=False,
            ),
            DateInput(
                title=CreateGoodForm.FirearmGood.FirearmsActCertificate.EXPIRY_DATE,
                description=CreateGoodForm.FirearmGood.FirearmsActCertificate.EXPIRY_DATE_HINT,
                prefix="section_certificate_date_of_expiry",
                name="section_certificate_date_of_expiry",
            ),
            Label(text="Or"),
            Checkboxes(
                name="section_certificate_missing",
                options=[Option(key="True", value=f"I do not have a Firearms Act 1968 {section} certificate",)],
            ),
            TextArea(
                title="Provide a reason why you do not have a certificate",
                name="section_certificate_missing_reason",
                optional=False,
            ),
        ],
        back_link=back_link,
        buttons=[Button("Save and continue", "submit")],
        javascript_imports={"/javascripts/add-good.js"},
    )


def build_firearm_back_link_create(form_url, form_data):
    return Custom(
        data={**form_data, "form_pk": int(form_data["form_pk"]) + 1, "form_url": form_url,},
        template="applications/firearm_upload_back_link.html",
    )


def build_firearm_create_back(back_link):
    return BackLink("Back", back_link)


def identification_markings_form(draft_pk=None, good_id=None):
    questions = [
        HiddenField("identification_markings_step", True),
        RadioButtons(
            title="",
            name="has_identification_markings",
            options=[
                Option(key=True, value=CreateGoodForm.FirearmGood.IdentificationMarkings.YES,),
                Option(
                    key=False,
                    value=CreateGoodForm.FirearmGood.IdentificationMarkings.NO,
                    components=[
                        TextArea(
                            title=CreateGoodForm.FirearmGood.IdentificationMarkings.NO_MARKINGS_DETAILS,
                            description="",
                            name="no_identification_markings_details",
                            optional=False,
                        )
                    ],
                ),
            ],
        ),
        HiddenField("pk", draft_pk) if draft_pk else None,
        HiddenField("good_id", good_id) if good_id else None,
    ]

    return Form(
        title=CreateGoodForm.FirearmGood.IdentificationMarkings.TITLE,
        questions=questions,
        default_button_name=CreateGoodForm.FirearmGood.IdentificationMarkings.BUTTON_TEXT,
    )


def attach_firearm_dealer_certificate_form(back_url):
    return Form(
        title="Attach your registered firearms dealer certificate",
        description="The file must be smaller than 50MB",
        questions=[
            FileUpload(),
            TextInput(name="reference_code", title="Certificate number",),
            DateInput(
                prefix="expiry_date_", name="expiry_date", title="Expiry date", description="For example 12 3 2021"
            ),
        ],
        back_link=BackLink("Back", back_url),
    )


def is_registered_firearm_dealer_field(back_url):
    questions = [
        RadioButtons(
            title="",
            name="is_registered_firearm_dealer",
            options=[Option(key=True, value="Yes"), Option(key=False, value="No"),],
        )
    ]
    return Form(
        title="Are you a registered firearms dealer?",
        questions=questions,
        back_link=BackLink("Back", back_url),
        default_button_name="Save and continue",
    )


def has_expired_rfd_certificate(application):
    document = get_rfd_certificate(application)
    return bool(document) and document["is_expired"]


def has_valid_rfd_certificate(application):
    document = get_rfd_certificate(application)
    return bool(document) and not document["is_expired"]


def get_rfd_certificate(application):
    documents = {item["document_type"]: item for item in application.get("organisation", {}).get("documents", [])}
    return documents.get("rfd-certificate")


def has_valid_section_five_certificate(application):
    documents = {item["document_type"]: item for item in application.get("organisation", {}).get("documents", [])}
    if "section-five-certificate" in documents:
        return not documents["section-five-certificate"]["is_expired"]
    return False


class FormContextMixin:
    def __init__(self, *args, **kwargs):
        self.form_context = kwargs.pop("form_context")
        super().__init__(*args, **kwargs)


class ProductCategoryForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.ProductCategory.TITLE

    item_category = forms.ChoiceField(
        choices=(
            ("group1_platform", CreateGoodForm.ProductCategory.GROUP1_PLATFORM),
            ("group1_device", CreateGoodForm.ProductCategory.GROUP1_DEVICE),
            ("group1_components", CreateGoodForm.ProductCategory.GROUP1_COMPONENTS),
            ("group1_materials", CreateGoodForm.ProductCategory.GROUP1_MATERIALS),
            (PRODUCT_CATEGORY_FIREARM, CreateGoodForm.ProductCategory.GROUP2_FIREARMS),
            ("group3_software", CreateGoodForm.ProductCategory.GROUP3_SOFTWARE),
            ("group3_technology", CreateGoodForm.ProductCategory.GROUP3_TECHNOLOGY),
        ),
        widget=forms.RadioSelect,
        label="",
        error_messages={"required": "Select a product category",},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title), "item_category", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )


class GroupTwoProductTypeForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.FirearmGood.ProductType.TITLE

    type = forms.TypedChoiceField(
        choices=(
            ("firearms", CreateGoodForm.FirearmGood.ProductType.FIREARM),
            ("ammunition", CreateGoodForm.FirearmGood.ProductType.AMMUNITION),
            ("components_for_firearms", CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_FIREARM),
            ("components_for_ammunition", CreateGoodForm.FirearmGood.ProductType.COMPONENTS_FOR_AMMUNITION),
            ("firearms_accessory", CreateGoodForm.FirearmGood.ProductType.FIREARMS_ACCESSORY),
            ("software_related_to_firearms", CreateGoodForm.FirearmGood.ProductType.SOFTWARE_RELATED_TO_FIREARM),
            ("technology_related_to_firearms", CreateGoodForm.FirearmGood.ProductType.TECHNOLOGY_RELATED_TO_FIREARM),
        ),
        error_messages={"required": "Select the type of product",},
        widget=forms.RadioSelect,
        label="",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(HTML.h1(self.title), "type", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["product_type_step"] = True
        return cleaned_data


class FirearmsNumberOfItemsForm(FormContextMixin, forms.Form):
    title = "Number of items"

    number_of_items = forms.IntegerField(
        error_messages={"required": "Enter the number of items",}, widget=forms.TextInput, label=""
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title), "number_of_items", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["number_of_items_step"] = True
        return cleaned_data


class IdentificationMarkingsForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.FirearmGood.IdentificationMarkings.TITLE

    has_identification_markings = forms.ChoiceField(
        choices=(
            (True, CreateGoodForm.FirearmGood.IdentificationMarkings.YES),
            (False, CreateGoodForm.FirearmGood.IdentificationMarkings.NO),
        ),
        error_messages={"required": "Select yes if the product has identification markings",},
        label="",
    )
    no_identification_markings_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=CreateGoodForm.FirearmGood.IdentificationMarkings.NO_MARKINGS_DETAILS,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML(
                render_to_string(
                    "goods/choice-with-details.html",
                    {
                        "form": self,
                        "choice_field_name": "has_identification_markings",
                        "details": {False: "no_identification_markings_details"},
                    },
                )
            ),
            Submit("submit", CreateGoodForm.FirearmGood.IdentificationMarkings.BUTTON_TEXT),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["identification_markings_step"] = True

        if cleaned_data.get("has_identification_markings") == "False":
            if not cleaned_data.get("no_identification_markings_details"):
                self.add_error(
                    "no_identification_markings_details", "Enter a reason why the product has not been marked",
                )

        return cleaned_data


class FirearmsCaptureSerialNumbersForm(FormContextMixin, forms.Form):
    title = "Enter the serial numbers for this product"

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for i in range(self.form_context.number_of_items):
            field_name = f"serial_number_input_{i}"
            self.fields[field_name] = forms.CharField(label=f"Serial number {i + 1}", required=False)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.h4("Enter one serial number in every row"),
            HTML.p(f"Number of items: {self.form_context.number_of_items}"),
            *self.fields,
            Submit("submit", "Save and continue"),
        )

    def clean(self):
        cleaned_data = super().clean()

        if not any(cleaned_data.values()):
            self.add_error(None, "Enter at least one serial number")

        cleaned_data["capture_serial_numbers_step"] = True

        return cleaned_data


class ProductMilitaryUseForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.MilitaryUse.TITLE

    is_military_use = forms.ChoiceField(
        choices=(
            ("yes_designed", CreateGoodForm.MilitaryUse.YES_DESIGNED),
            ("yes_modified", CreateGoodForm.MilitaryUse.YES_MODIFIED),
            ("no", CreateGoodForm.MilitaryUse.NO),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title), "is_military_use", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )


class ProductUsesInformationSecurityForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.ProductInformationSecurity.TITLE

    uses_information_security = forms.ChoiceField(
        choices=((True, "Yes"), (False, CreateGoodForm.ProductInformationSecurity.NO),),
        label="",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    information_security_details = forms.CharField(
        required=False,
        widget=forms.Textarea,
        label=f"{CreateGoodForm.ProductInformationSecurity.INFORMATION_SECURITY_DETAILS} (optional)",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML(
                render_to_string(
                    "goods/choice-with-details.html",
                    {
                        "form": self,
                        "choice_field_name": "uses_information_security",
                        "details": {True: "information_security_details"},
                    },
                )
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )


class AddGoodsQuestionsForm(FormContextMixin, forms.Form):

    name = forms.CharField(
        help_text="Give your product a name so it is easier to find in your product list",
        error_messages={"required": "Enter a product name",},
    )

    description = forms.CharField(
        required=False, label="Description (optional)", widget=forms.Textarea(attrs={"rows": 5, "max_length": 280}),
    )

    part_number = forms.CharField(required=False, label="Part number (optional)")

    is_good_controlled = forms.ChoiceField(
        choices=((True, CreateGoodForm.IsControlled.YES), (False, CreateGoodForm.IsControlled.NO),),
        label=CreateGoodForm.IsControlled.TITLE,
        help_text=CreateGoodForm.IsControlled.DESCRIPTION,
        error_messages={"required": "Select an option",},
    )

    control_list_entries = forms.MultipleChoiceField(
        help_text="Type to get suggestions. For example ML1a.",
        choices=[],  # set in __init__
        required=False,
        # setting id for javascript to use
        widget=forms.SelectMultiple(attrs={"id": "control_list_entries"}),
    )

    is_pv_graded = forms.ChoiceField(
        choices=(("yes", CreateGoodForm.IsGraded.YES), ("no", CreateGoodForm.IsGraded.NO),),
        label=CreateGoodForm.IsGraded.TITLE,
        help_text=CreateGoodForm.IsGraded.DESCRIPTION,
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.form_context.application_pk is not None:
            self.title = CreateGoodForm.TITLE_APPLICATION
        else:
            self.title = CreateGoodForm.TITLE_GOODS_LIST

        self.fields["control_list_entries"].choices = [
            (entry["rating"], entry["rating"]) for entry in self.form_context.clc_list
        ]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "name",
            "description",
            "part_number",
            HTML(
                render_to_string(
                    "goods/choice-with-details.html",
                    {
                        "form": self,
                        "choice_field_name": "is_good_controlled",
                        "details": {True: "control_list_entries"},
                    },
                )
            ),
            "is_pv_graded",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        if not str_to_bool(cleaned_data.get("is_good_controlled")):
            cleaned_data.pop("control_list_entries", None)
        return cleaned_data


class PvDetailsForm(FormContextMixin, forms.Form):
    title = GoodGradingForm.TITLE

    prefix = forms.CharField(required=False, label=f"{GoodGradingForm.PREFIX} (optional)")

    grading = forms.ChoiceField(required=False, label=GoodGradingForm.GRADING,)

    suffix = forms.CharField(required=False, label=f"{GoodGradingForm.SUFFIX} (optional)")

    custom_grading = forms.CharField(required=False, label=f"{GoodGradingForm.OTHER_GRADING} (optional)")

    issuing_authority = forms.CharField(
        label=GoodGradingForm.ISSUING_AUTHORITY, error_messages={"required": "This field may not be blank",},
    )

    reference = forms.CharField(
        label=GoodGradingForm.REFERENCE, error_messages={"required": "This field may not be blank",},
    )

    date_of_issue = DateInputField(label=GoodGradingForm.DATE_OF_ISSUE)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        gradings = [
            (key, display) for grading in get_pv_gradings(self.form_context.request) for key, display in grading.items()
        ]
        gradings.insert(0, ("Select", "Select"))

        self.fields["grading"] = forms.ChoiceField(required=False, label=GoodGradingForm.GRADING, choices=gradings)

        # The date field is styled correctly when the input type is 'number'.
        # This workaround switches the underlying widgets to 'number' type.
        convert_to_number_input(self.fields["date_of_issue"])

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.h3("PV grading"),
            Fieldset(
                Field.text("prefix"), Field.text("grading"), Field.text("suffix"), css_class="app-pv-grading-inputs"
            ),
            "custom_grading",
            "issuing_authority",
            "reference",
            "date_of_issue",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        if cleaned_data["grading"] == "Select" and not cleaned_data["custom_grading"]:
            self.add_error("custom_grading", "Enter the grading if it's not listed in the dropdown list")

        date_of_issue = cleaned_data.get("date_of_issue")

        if date_of_issue:
            cleaned_data["date_of_issue"] = date_of_issue.strftime("%Y-%m-%d")
            cleaned_data["date_of_issueday"] = str(date_of_issue.day)
            cleaned_data["date_of_issuemonth"] = str(date_of_issue.month)
            cleaned_data["date_of_issueyear"] = str(date_of_issue.year)

        return cleaned_data


def convert_to_number_input(date_field):
    date_field.widget.widgets = [forms.NumberInput(attrs=w.attrs) for w in date_field.widget.widgets]


class FirearmsYearOfManufactureDetailsForm(FormContextMixin, forms.Form):
    title = "What is the year of manufacture of the firearm?"

    year_of_manufacture = forms.CharField(label="", error_messages={"required": "Enter the year of manufacture",},)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title), "year_of_manufacture", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["firearm_year_of_manufacture_step"] = True

        try:
            year_of_manufacture = int(cleaned_data["year_of_manufacture"])
        except KeyError:
            return cleaned_data
        except ValueError:
            year_of_manufacture = 0

        if year_of_manufacture <= 0:
            self.add_error("year_of_manufacture", "Year of manufacture must be valid")

        if year_of_manufacture > timezone.now().date().year:
            self.add_error("year_of_manufacture", "Year of manufacture must be in the past")

        return cleaned_data


class FirearmsReplicaForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.FirearmGood.FirearmsReplica.TITLE

    is_replica = forms.ChoiceField(
        choices=((True, "Yes"), (False, "No"),),
        label="",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    replica_description = forms.CharField(
        widget=forms.Textarea, label=CreateGoodForm.FirearmGood.FirearmsReplica.DESCRIPTION, required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML(
                render_to_string(
                    "goods/choice-with-details.html",
                    {"form": self, "choice_field_name": "is_replica", "details": {True: "replica_description"}},
                )
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["is_replica_step"] = True

        if str_to_bool(cleaned_data.get("is_replica")) and not cleaned_data.get("replica_description"):
            self.add_error("replica_description", "Enter a description")

        return cleaned_data


class FirearmsCalibreDetailsForm(FormContextMixin, forms.Form):
    title = "What is the calibre of the product?"

    calibre = forms.CharField(label="", error_messages={"required": "Enter the calibre",},)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(HTML.h1(self.title), "calibre", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),)

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["firearm_calibre_step"] = True
        return cleaned_data


class RegisteredFirearmsDealerForm(FormContextMixin, forms.Form):
    title = "Are you a registered firearms dealer?"

    is_registered_firearm_dealer = forms.ChoiceField(
        choices=((True, "Yes"), (False, "No"),),
        label="",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title), "is_registered_firearm_dealer", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )


class AttachFirearmsDealerCertificateForm(FormContextMixin, forms.Form):
    title = "Attach your registered firearms dealer certificate"

    file = forms.FileField(
        label="",
        help_text="The file must be smaller than 50MB",
        error_messages={"required": "Select certificate file to upload",},
    )

    reference_code = forms.CharField(
        label="Certificate number", error_messages={"required": "Enter the certificate number",},
    )

    expiry_date = DateInputField(label="Expiry date", help_text="For example 12 3 2022",)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # The date field is styled correctly when the input type is 'number'.
        # This workaround switches the underlying widgets to 'number' type.
        convert_to_number_input(self.fields["expiry_date"])

        self.helper = FormHelper()
        self.helper.attrs = {"enctype": "multipart/form-data"}
        self.helper.layout = Layout(
            HTML.h1(self.title),
            "file",
            "reference_code",
            "expiry_date",
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()

        expiry_date = cleaned_data.pop("expiry_date", None)

        if expiry_date:
            if expiry_date < timezone.now().date():
                self.add_error("expiry_date", "Expiry date must be in the future")
            else:
                cleaned_data["expiry_date_day"] = str(expiry_date.day)
                cleaned_data["expiry_date_month"] = str(expiry_date.month)
                cleaned_data["expiry_date_year"] = str(expiry_date.year)

        return cleaned_data


class FirearmsActConfirmationForm(FormContextMixin, forms.Form):

    is_covered_by_firearm_act_section_one_two_or_five = forms.ChoiceField(
        choices=(
            ("Yes", CreateGoodForm.FirearmGood.FirearmsActCertificate.YES),
            ("No", CreateGoodForm.FirearmGood.FirearmsActCertificate.NO),
            ("Unsure", CreateGoodForm.FirearmGood.FirearmsActCertificate.DONT_KNOW),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    firearms_act_section = forms.ChoiceField(
        choices=(
            ("firearms_act_section1", "Section 1"),
            ("firearms_act_section2", "Section 2"),
            ("firearms_act_section5", "Section 5"),
        ),
        label="Select section",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
        required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        if self.form_context.is_rfd:
            self.title = "Is the product covered by section 5 of the Firearms Act 1968?"

            details = [
                "What does section 5 cover?",
                linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                )
                + f"&nbsp;&nbsp;covers weapons and ammunition that are generally prohibited.",
            ]
        else:
            self.title = CreateGoodForm.FirearmGood.FirearmsActCertificate.TITLE

            details = [
                "What do these sections cover?",
                linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_ONE,
                )
                + f"&nbsp;&nbsp;is a broad category covering most types of firearm and ammunition, including rifles and high powered air weapons.<br><br>"
                + linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_TWO,
                )
                + f"&nbsp;&nbsp;covers most types of shotgun.<br><br>"
                + linkify(
                    CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE_LINK,
                    name=CreateGoodForm.FirearmGood.FirearmsActCertificate.SECTION_FIVE,
                )
                + f"&nbsp;&nbsp;covers weapons and ammunition that are generally prohibited.",
            ]

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML.details(*details),
            "is_covered_by_firearm_act_section_one_two_or_five"
            if self.form_context.is_rfd
            else HTML(
                render_to_string(
                    "goods/choice-with-details.html",
                    {
                        "form": self,
                        "choice_field_name": "is_covered_by_firearm_act_section_one_two_or_five",
                        "details": {"Yes": "firearms_act_section"},
                    },
                )
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )

    def clean(self):
        cleaned_data = super().clean()
        cleaned_data["section_certificate_step"] = True

        if (
            not self.form_context.is_rfd
            and cleaned_data.get("is_covered_by_firearm_act_section_one_two_or_five") == "Yes"
            and not cleaned_data.get("firearms_act_section")
        ):
            self.add_error("firearms_act_section", "Select an option")

        return cleaned_data


class SoftwareTechnologyDetailsForm(FormContextMixin, forms.Form):
    software_or_technology_details = forms.CharField(
        label="", widget=forms.Textarea, error_messages={"required": "Enter the purpose of the technology",},
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        category_text = get_category_display_string(self.form_context.category_type)
        self.title = CreateGoodForm.TechnologySoftware.TITLE + category_text

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title), "software_or_technology_details", Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )


class ProductComponentForm(FormContextMixin, forms.Form):
    title = CreateGoodForm.ProductComponent.TITLE

    is_component = forms.ChoiceField(
        choices=(
            ("yes_designed", CreateGoodForm.ProductComponent.YES_DESIGNED),
            ("yes_modified", CreateGoodForm.ProductComponent.YES_MODIFIED),
            ("yes_general", CreateGoodForm.ProductComponent.YES_GENERAL_PURPOSE),
            ("no", CreateGoodForm.ProductComponent.NO),
        ),
        label="",
        widget=forms.RadioSelect,
        error_messages={"required": "Select an option",},
    )

    designed_details = forms.CharField(
        label=CreateGoodForm.ProductComponent.DESIGNED_DETAILS, widget=forms.Textarea, required=False,
    )

    modified_details = forms.CharField(
        label=CreateGoodForm.ProductComponent.MODIFIED_DETAILS, widget=forms.Textarea, required=False,
    )

    general_details = forms.CharField(
        label=CreateGoodForm.ProductComponent.GENERAL_DETAILS, widget=forms.Textarea, required=False,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.layout = Layout(
            HTML.h1(self.title),
            HTML(
                render_to_string(
                    "goods/choice-with-details.html",
                    {
                        "form": self,
                        "choice_field_name": "is_component",
                        "details": {
                            "yes_designed": "designed_details",
                            "yes_modified": "modified_details",
                            "yes_general": "general_details",
                        },
                    },
                )
            ),
            Submit("submit", CreateGoodForm.SUBMIT_BUTTON),
        )
