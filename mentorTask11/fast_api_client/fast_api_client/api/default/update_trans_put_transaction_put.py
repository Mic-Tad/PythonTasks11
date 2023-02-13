from http import HTTPStatus
from typing import Any, Dict, Optional, Union, cast

import httpx

from ... import errors
from ...client import Client
from ...models.http_validation_error import HTTPValidationError
from ...types import UNSET, Response, Unset


def _get_kwargs(
    *,
    client: Client,
    transaction_id: Union[Unset, None, Any] = UNSET,
    transaction_status: Union[Unset, None, Any] = UNSET,
    amount: Union[Unset, None, Any] = UNSET,
    recipient_id: Union[Unset, None, Any] = UNSET,
    currency: Union[Unset, None, Any] = UNSET,
) -> Dict[str, Any]:
    url = "{}/put/transaction".format(client.base_url)

    headers: Dict[str, str] = client.get_headers()
    cookies: Dict[str, Any] = client.get_cookies()

    params: Dict[str, Any] = {}
    params["transaction_id"] = transaction_id

    params["transaction_status"] = transaction_status

    params["amount"] = amount

    params["recipient_id"] = recipient_id

    params["currency"] = currency

    params = {k: v for k, v in params.items() if v is not UNSET and v is not None}

    return {
        "method": "put",
        "url": url,
        "headers": headers,
        "cookies": cookies,
        "timeout": client.get_timeout(),
        "params": params,
    }


def _parse_response(*, client: Client, response: httpx.Response) -> Optional[Union[Any, HTTPValidationError]]:
    if response.status_code == HTTPStatus.OK:
        response_200 = cast(Any, response.json())
        return response_200
    if response.status_code == HTTPStatus.UNPROCESSABLE_ENTITY:
        response_422 = HTTPValidationError.from_dict(response.json())

        return response_422
    if client.raise_on_unexpected_status:
        raise errors.UnexpectedStatus(f"Unexpected status code: {response.status_code}")
    else:
        return None


def _build_response(*, client: Client, response: httpx.Response) -> Response[Union[Any, HTTPValidationError]]:
    return Response(
        status_code=HTTPStatus(response.status_code),
        content=response.content,
        headers=response.headers,
        parsed=_parse_response(client=client, response=response),
    )


def sync_detailed(
    *,
    client: Client,
    transaction_id: Union[Unset, None, Any] = UNSET,
    transaction_status: Union[Unset, None, Any] = UNSET,
    amount: Union[Unset, None, Any] = UNSET,
    recipient_id: Union[Unset, None, Any] = UNSET,
    currency: Union[Unset, None, Any] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Update Trans

    Args:
        transaction_id (Union[Unset, None, Any]):
        transaction_status (Union[Unset, None, Any]):
        amount (Union[Unset, None, Any]):
        recipient_id (Union[Unset, None, Any]):
        currency (Union[Unset, None, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
        transaction_status=transaction_status,
        amount=amount,
        recipient_id=recipient_id,
        currency=currency,
    )

    response = httpx.request(
        verify=client.verify_ssl,
        **kwargs,
    )

    return _build_response(client=client, response=response)


def sync(
    *,
    client: Client,
    transaction_id: Union[Unset, None, Any] = UNSET,
    transaction_status: Union[Unset, None, Any] = UNSET,
    amount: Union[Unset, None, Any] = UNSET,
    recipient_id: Union[Unset, None, Any] = UNSET,
    currency: Union[Unset, None, Any] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Update Trans

    Args:
        transaction_id (Union[Unset, None, Any]):
        transaction_status (Union[Unset, None, Any]):
        amount (Union[Unset, None, Any]):
        recipient_id (Union[Unset, None, Any]):
        currency (Union[Unset, None, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return sync_detailed(
        client=client,
        transaction_id=transaction_id,
        transaction_status=transaction_status,
        amount=amount,
        recipient_id=recipient_id,
        currency=currency,
    )


async def asyncio_detailed(
    *,
    client: Client,
    transaction_id: Union[Unset, None, Any] = UNSET,
    transaction_status: Union[Unset, None, Any] = UNSET,
    amount: Union[Unset, None, Any] = UNSET,
    recipient_id: Union[Unset, None, Any] = UNSET,
    currency: Union[Unset, None, Any] = UNSET,
) -> Response[Union[Any, HTTPValidationError]]:
    """Update Trans

    Args:
        transaction_id (Union[Unset, None, Any]):
        transaction_status (Union[Unset, None, Any]):
        amount (Union[Unset, None, Any]):
        recipient_id (Union[Unset, None, Any]):
        currency (Union[Unset, None, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    kwargs = _get_kwargs(
        client=client,
        transaction_id=transaction_id,
        transaction_status=transaction_status,
        amount=amount,
        recipient_id=recipient_id,
        currency=currency,
    )

    async with httpx.AsyncClient(verify=client.verify_ssl) as _client:
        response = await _client.request(**kwargs)

    return _build_response(client=client, response=response)


async def asyncio(
    *,
    client: Client,
    transaction_id: Union[Unset, None, Any] = UNSET,
    transaction_status: Union[Unset, None, Any] = UNSET,
    amount: Union[Unset, None, Any] = UNSET,
    recipient_id: Union[Unset, None, Any] = UNSET,
    currency: Union[Unset, None, Any] = UNSET,
) -> Optional[Union[Any, HTTPValidationError]]:
    """Update Trans

    Args:
        transaction_id (Union[Unset, None, Any]):
        transaction_status (Union[Unset, None, Any]):
        amount (Union[Unset, None, Any]):
        recipient_id (Union[Unset, None, Any]):
        currency (Union[Unset, None, Any]):

    Raises:
        errors.UnexpectedStatus: If the server returns an undocumented status code and Client.raise_on_unexpected_status is True.
        httpx.TimeoutException: If the request takes longer than Client.timeout.

    Returns:
        Response[Union[Any, HTTPValidationError]]
    """

    return (
        await asyncio_detailed(
            client=client,
            transaction_id=transaction_id,
            transaction_status=transaction_status,
            amount=amount,
            recipient_id=recipient_id,
            currency=currency,
        )
    ).parsed
