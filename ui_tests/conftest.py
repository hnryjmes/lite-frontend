import os
from collections import OrderedDict

import tests_common.tools.helpers as utils


STEP_THROUGH = False  # Gives a prompt for every step in the terminal
SCENARIO_HISTORY = OrderedDict()


def pytest_bdd_before_step_call(request, feature, scenario, step, step_func, step_func_args):
    """
    Runs before each step
    """

    try:
        SCENARIO_HISTORY[scenario]["steps"].append(step)
    except KeyError:
        SCENARIO_HISTORY[scenario] = {
            "steps": [step],
            "scenario": scenario,
        }

    if STEP_THROUGH:
        print("*******************************************")
        print(f"SCENARIO: {scenario.feature.description}")
        print(f"STEP: .. {step.keyword} {step.name}")
        print("*******************************************")
        import IPython

        IPython.embed(using=False)


def pytest_configure(config):
    if config.option.step_through:
        global STEP_THROUGH  # pylint: disable=global-statement
        STEP_THROUGH = config.option.step_through


def pytest_addoption(parser):
    env = str(os.environ.get("ENVIRONMENT"))
    if env == "None":
        env = "dev"
    parser.addoption("--headless", action="store_true", default=False)
    parser.addoption(
        "--step-through", action="store_true", default=STEP_THROUGH, help="Allow stepping through each scenario step"
    )
    if env == "local":
        parser.addoption(
            "--exporter_url", action="store", default=f"http://localhost:{str(os.environ.get('PORT'))}/", help="url"
        )
        parser.addoption(
            "--internal_url", action="store", default="http://localhost:" + str(os.environ.get("PORT")), help="url"
        )
        lite_api_url = os.environ.get("LOCAL_LITE_API_URL", os.environ.get("LITE_API_URL"),)
        parser.addoption(
            "--lite_api_url", action="store", default=lite_api_url, help="url",
        )
    else:
        parser.addoption(
            "--exporter_url",
            action="store",
            default=f"https://exporter.lite.service.{env}.uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--internal_url",
            action="store",
            default="https://internal.lite.service." + env + ".uktrade.digital/",
            help="url",
        )
        parser.addoption(
            "--lite_api_url", action="store", default=f"https://lite-api-{env}.london.cloudapps.digital/", help="url",
        )
    parser.addoption("--sso_sign_in_url", action="store", default="https://sso.trade.uat.uktrade.io/login/", help="url")


def pytest_exception_interact(node, report):
    if node and report.failed and hasattr(node, "funcargs"):
        driver = node.funcargs.get("driver")
        if driver:
            utils.save_screenshot(driver=driver, name=node.name)
