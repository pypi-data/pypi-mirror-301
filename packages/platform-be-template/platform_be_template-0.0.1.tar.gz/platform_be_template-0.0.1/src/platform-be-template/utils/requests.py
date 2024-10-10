from datetime import datetime, date
from typing import Literal, Union, Optional

import httpx
from httpx import Response


class APIExceptionFromOtherServer(Exception):
    status_code: int
    detail: str

    def __init__(self, status_code: int = 500, detail: Union[str, None] = None):
        self.status_code = status_code
        if not detail:
            self.detail = 'Error from other server'
        else:
            self.detail = detail


DEFAULT_API_HEADER = {
    'content-type': 'application/json'
}


def _request_other_server(
        method: Literal['GET', 'POST', 'OPTION', 'DELETE', 'PATCH'], url: str,
        params: Optional[dict[str, Union[str, int, float, None, datetime, date]]] = None,
        data: Optional[dict[str, Union[str, int, float, None, datetime, date]]] = None,
        api_user_key: Optional[str] = None,
        headers: dict[str, str] = None,
        timeout: int = 10
) -> Response:
    _headers = dict(DEFAULT_API_HEADER)

    if headers:
        _headers.update(headers)
    if api_user_key:
        _headers.update({
            'x-authorization-sso': api_user_key
        })

    request = getattr(httpx, method)

    server_response: Response = request(
        url=url,
        params=params,
        json=data,
        timeout=timeout
    )
    return server_response


def get_json_response_from_other_server(
        method: Literal['GET', 'POST', 'OPTION', 'DELETE', 'PATCH'], url: str,
        params: Optional[dict[str, Union[str, int, float, None, datetime, date]]] = None,
        data: Optional[dict[str, Union[str, int, float, None, datetime, date]]] = None,
        api_user_key: Optional[str] = None,
        headers: dict[str, str] = None,
        timeout: int = 10
):
    """
    :param method: HTTP method of this request.
    :param url: request url.
    :param params: Optional. query params for this request.
    :param data: Optional. data that will be placed in request body.
    :param api_user_key: Optional. The user key if needed to be authenticated.
    :param headers: Optional. header data.
    :param timeout: Optional. default value is 10 sec.
    :return: server response as json if status code is 200. Else, will raise `APIExceptionFromOtherServer`.
    """
    server_response: Response = _request_other_server(
        method, url, params, data, api_user_key, headers, timeout
    )

    if server_response.status_code == 200:
        return server_response.json()

    else:
        _text_response = server_response.json().get('detail', None)
        raise APIExceptionFromOtherServer(
            status_code=server_response.status_code,
            detail=_text_response
        )
