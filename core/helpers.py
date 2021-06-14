from urllib.parse import urlencode


def dummy_quote(string, safe="", encoding=None, errors=None):
    return string


def convert_dict_to_query_params(dictionary):
    return urlencode(dictionary, doseq=True, quote_via=dummy_quote)


def convert_parameters_to_query_params(dictionary):
    if "request" in dictionary:
        del dictionary["request"]
    return "?" + convert_dict_to_query_params({key: value for key, value in dictionary.items() if value is not None})


def convert_value_to_query_param(key: str, value):
    if value is None:
        return ""
    return urlencode({key: value}, doseq=True, quote_via=dummy_quote)


def format_date(data, date_field):
    year = data.get(date_field + "year", "")
    month = data.get(date_field + "month", "")
    day = data.get(date_field + "day", "")
    if not year or not month or not day:
        return None
    if len(month) == 1:
        month = "0" + month
    if len(day) == 1:
        day = "0" + day
    return f"{year}-{month}-{day}"
