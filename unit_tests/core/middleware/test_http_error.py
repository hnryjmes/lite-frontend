from requests import HTTPError
from requests.models import Response

from core.middleware import HttpErrorHandlerMiddleware


def test_http_error_handler_non_http_error_exception(rf, mocker, caplog):
    get_response = mocker.MagicMock()
    http_error_handler = HttpErrorHandlerMiddleware(get_response)

    request = rf.get("/")
    not_http_error = Exception()
    assert http_error_handler.process_exception(request, not_http_error) is None
    assert not caplog.records


def test_http_error_handler_with_http_error(rf, mocker, caplog):
    get_response = mocker.MagicMock()
    http_error_handler = HttpErrorHandlerMiddleware(get_response)

    response = Response()
    response.status_code = 400
    response._content = b'{"error": "this is an error"}'

    http_error = HTTPError(response=response)
    request = rf.get("/")
    assert http_error_handler.process_exception(request, http_error) is None
    assert ("INFO", '{"error": "this is an error"}') in [(r.levelname, r.msg) for r in caplog.records]
