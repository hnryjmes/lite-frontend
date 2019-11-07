from sys import exit
from os import path, environ

from ...seed_data.seed_data import SeedData


def _get_env():
    base_dir = path.dirname(path.dirname(path.dirname(path.abspath(__file__))))
    env_file = path.join(base_dir, '.env')

    if path.exists(env_file):
        with open(env_file) as f:
            for line in f:
                key_value_pair = line.split('=')
                if len(key_value_pair) == 2:
                    environ[key_value_pair[0].strip()] = key_value_pair[1].strip()

    return environ


def _get_exporter_info(env):
    exporter_user_email = env['TEST_EXPORTER_SSO_EMAIL']
    exporter_user_password = env['TEST_EXPORTER_SSO_PASSWORD']
    exporter_user__name = env['TEST_EXPORTER_SSO_NAME']
    exporter_user_first_name, exporter_user_last_name = exporter_user__name.split(' ')

    return {
        'email': exporter_user_email,
        'password': exporter_user_password,
        'first_name': exporter_user_first_name,
        'last_name': exporter_user_last_name
    }


def _get_internal_info(env):
    gov_user_email = env['TEST_SSO_EMAIL']
    gov_user_password = env['TEST_SSO_PASSWORD']
    gov_user_name = env['TEST_SSO_NAME']
    gov_user_first_name, gov_user_last_name = gov_user_name.split(' ')

    return {
        'email': gov_user_email,
        'name': gov_user_name,
        'first_name': gov_user_first_name,
        'last_name': gov_user_last_name,
        'password': gov_user_password
    }


def _get_seed_data_config():
    env = _get_env()
    api_url = env['LITE_API_URL']

    return {
        'api_url': api_url,
        'exporter': _get_exporter_info(env),
        'gov': _get_internal_info(env)
    }


def _get_amount_to_seed(argv):
    if len(argv) > 1:
        try:
            amount_to_seed = int(argv[1])

            if amount_to_seed <= 0:
                raise ValueError

            return amount_to_seed
        except ValueError:
            print('You must supply a positive integer.')
            exit(1)

    return 1


def seed(argv, action):
    amount_to_seed = _get_amount_to_seed(argv)
    seed_data = SeedData(_get_seed_data_config())

    for _ in range(amount_to_seed):
        action(seed_data)
