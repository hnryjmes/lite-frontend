import rules

from caseworker.core.rules import is_user_allocated
from caseworker.advice import services


def can_fcdo_make_recommendation(user, case, queue_alias):
    if queue_alias not in (
        services.FCDO_CASES_TO_REVIEW_QUEUE,
        services.FCDO_CPACC_CASES_TO_REVIEW_QUEUE,
    ):
        return False
    return len(services.unadvised_countries(user, case)) > 0


def can_mod_make_recommendation(user, case, queue_alias):
    return queue_alias in services.MOD_CONSOLIDATE_QUEUES


def can_ncsc_make_recommendation(user, case, queue_alias):
    return queue_alias == services.NCSC_CASES_TO_REVIEW


def can_beis_make_recommendation(user, case, queue_alias):
    if queue_alias not in (
        services.BEIS_CHEMICAL_CASES_TO_REVIEW,
        services.BEIS_NUCLEAR_CASES_TO_REVIEW,
    ):
        return False

    if queue_alias == services.BEIS_NUCLEAR_CASES_TO_REVIEW:
        return len(services.unassessed_trigger_list_goods(case)) == 0

    return True


@rules.predicate
def can_user_make_recommendation(request, case):
    try:
        queue = request.queue
        user = request.lite_user
    except AttributeError:
        return False
    team = user["team"]["alias"]
    queue_alias = queue["alias"]
    existing_advice = services.get_my_advice(case.advice, user["id"])

    # Existing advice, so this must be edited
    if existing_advice:
        return False

    if team == services.FCDO_TEAM:
        return can_fcdo_make_recommendation(user, case, queue_alias)
    if team in services.MOD_CONSOLIDATE_TEAMS:
        return can_mod_make_recommendation(user, case, queue_alias)
    if team in services.BEIS_TEAMS:
        return can_beis_make_recommendation(user, case, queue_alias)
    if team == services.NCSC_TEAM:
        return can_ncsc_make_recommendation(user, case, queue_alias)

    return False


rules.add_rule("can_user_make_recommendation", is_user_allocated & can_user_make_recommendation)
rules.add_rule("can_user_allocate_and_approve", can_user_make_recommendation)
