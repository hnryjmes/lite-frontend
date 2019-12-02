class PartyForm:
    class Options:
        GOVERNMENT = "A Government Organisation"
        COMMERCIAL = "A Commercial Organisation"
        INDIVIDUAL = "An Individual"
        OTHER = "Other"


class EndUserForm:
    TITLE = "Who is the end user of your goods?"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Enter the final recipient's name"
    WEBSITE_FORM_TITLE = "Enter the final recipient's web address (URL)"


class UltimateEndUserForm:
    TITLE = "Who is the ultimate end user of your goods?"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Enter the final recipient's name"
    WEBSITE_FORM_TITLE = "Enter the final recipient's web address (URL)"


class ConsigneeForm:
    TITLE = "Who will be the consignee of your goods?"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Enter the final recipient's name"
    WEBSITE_FORM_TITLE = "Enter the final recipient's web address (URL)"


class ThirdPartyForm:
    class Options:
        AGENT = "Agent or broker"
        ADDITIONAL_END_USER = "Additional end user"
        INTERMEDIATE_CONSIGNEE = "Intermediate consignee"
        SUBMITTER = "Authorised submitter"
        CONSULTANT = "Consultant"
        CONTACT = "Contact"
        EXPORTER = "Exporter"
    TITLE = "What type of third party would you like to add?"
    BUTTON = "Continue"
    NAME_FORM_TITLE = "Enter the final recipient's name"
    WEBSITE_FORM_TITLE = "Enter the final recipient's web address (URL)"
