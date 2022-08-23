from exporter.applications.views.goods.common import constants


class AddGoodSoftwareSteps:
    NAME = constants.NAME
    PRODUCT_CONTROL_LIST_ENTRY = constants.PRODUCT_CONTROL_LIST_ENTRY
    PART_NUMBER = constants.PART_NUMBER
    PV_GRADING = constants.PV_GRADING
    PV_GRADING_DETAILS = constants.PV_GRADING_DETAILS
    SECURITY_FEATURES = constants.SECURITY_FEATURES
    PRODUCT_DECLARED_AT_CUSTOMS = constants.PRODUCT_DECLARED_AT_CUSTOMS
    PRODUCT_USES_INFORMATION_SECURITY = constants.PRODUCT_USES_INFORMATION_SECURITY
    PRODUCT_DOCUMENT_AVAILABILITY = constants.PRODUCT_DOCUMENT_AVAILABILITY
    PRODUCT_DESIGN_DETAILS = constants.PRODUCT_DESIGN_DETAILS
    PRODUCT_DOCUMENT_SENSITIVITY = constants.PRODUCT_DOCUMENT_SENSITIVITY
    PRODUCT_DOCUMENT_UPLOAD = constants.PRODUCT_DOCUMENT_UPLOAD
    PRODUCT_MILITARY_USE = "PRODUCT_MILITARY_USE"
    PART_NUMBER = constants.PART_NUMBER


class AddGoodSoftwareToApplicationSteps:
    ONWARD_EXPORTED = constants.ONWARD_EXPORTED
    ONWARD_ALTERED_PROCESSED = constants.ONWARD_ALTERED_PROCESSED
    ONWARD_INCORPORATED = constants.ONWARD_INCORPORATED
    QUANTITY_AND_VALUE = constants.QUANTITY_AND_VALUE
