from django.http import HttpRequest
from lite_forms.components import Form, Checkboxes, Filter, BackLink

from core.builtins.custom_tags import get_string
from queues.services import get_queues


def move_case_form(request: HttpRequest, case_url: str):
    return Form(
        get_string("cases.manage.move_case.title"),
        get_string("cases.manage.move_case.description"),
        [Filter(), Checkboxes("queues", get_queues(request, True)),],
        javascript_imports=["/assets/javascripts/filter-checkbox-list.js"],
        back_link=BackLink("Back to Case", case_url),
    )
