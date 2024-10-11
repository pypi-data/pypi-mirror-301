"""This module contains the RestAdapter class, which is used to make requests to the Flowery API."""""
from asyncio import sleep as asleep
from json import JSONDecodeError

import aiohttp

from pyflowery.exceptions import (
    ClientError,
    InternalServerError,
    RetryLimitExceeded,
    TooManyRequests,
)
from pyflowery.models import FloweryAPIConfig, Result


class RestAdapter:
    """Constructor for RestAdapter

    Args:
        config (FloweryAPIConfig): Configuration object for the FloweryAPI class

    Raises:
        ValueError: Raised when the keyword arguments passed to the class constructor conflict.
    """
    def __init__(self, config = FloweryAPIConfig):
        self._url = "https://api.flowery.pw/v1"
        self.config = config

    async def _do(self, http_method: str, endpoint: str, params: dict = None, timeout: float = 60):
        """Internal method to make a request to the Flowery API. You shouldn't use this directly.

        Args:
            http_method (str): The [HTTP method](https://developer.mozilla.org/en-US/docs/Web/HTTP/Methods) to use
            endpoint (str): The endpoint to make the request to.
            params (dict): Python dictionary of query parameters to send with the request.
            timeout (float): Number of seconds to wait for the request to complete.

        Raises:
            TooManyRequests: Raised when the Flowery API returns a 429 status code
            ClientError: Raised when the Flowery API returns a 4xx status code
            InternalServerError: Raised when the Flowery API returns a 5xx status code
            RetryLimitExceeded: Raised when the retry limit defined in the `FloweryAPIConfig` class (default 3) is exceeded

        Returns:
            Result: A Result object containing the status code, message, and data from the request.
        """
        full_url = self._url + endpoint
        headers = {
            'User-Agent': self.config.prepended_user_agent(),
        }
        sanitized_params = {k: str(v) if isinstance(v, bool) else v for k, v in params.items()} if params else None
        retry_counter = 0

        async with aiohttp.ClientSession() as session:
            while retry_counter < self.config.retry_limit:
                self.config.logger.debug("Making %s request to %s with headers %s and params %s", http_method, full_url, headers, sanitized_params)
                async with session.request(method=http_method, url=full_url, params=sanitized_params, headers=headers, timeout=timeout) as response:
                    try:
                        data = await response.json()
                    except (JSONDecodeError, aiohttp.ContentTypeError):
                        data = await response.read()

                    result = Result(
                        success=response.status,
                        status_code=response.status,
                        message=response.reason,
                        data=data,
                    )
                    self.config.logger.debug("Received response: %s %s", response.status, response.reason)
                    try:
                        if result.status_code == 429:
                            raise TooManyRequests(f"{result.message} - {result.data}")
                        if 400 <= result.status_code < 500:
                            raise ClientError(f"{result.status_code} - {result.message} - {result.data}")
                        if 500 <= result.status_code < 600:
                            raise InternalServerError(f"{result.status_code} - {result.message} - {result.data}")
                    except (TooManyRequests, InternalServerError) as e:
                        if retry_counter < self.config.retry_limit:
                            interval = self.config.interval * retry_counter
                            self.config.logger.error("%s - retrying in %s seconds", e, interval, exc_info=True)
                            retry_counter += 1
                            await asleep(interval)
                            continue
                        raise RetryLimitExceeded(message=f"Request failed more than {self.config.retry_limit} times, not retrying") from e
                    return result

    async def get(self, endpoint: str, params: dict = None, timeout: float = 60) -> Result:
        """Make a GET request to the Flowery API. You should almost never have to use this directly.

        Args:
            endpoint (str): The endpoint to make the request to.
            params (dict): Python dictionary of query parameters to send with the request.
            timeout (float): Number of seconds to wait for the request to complete.

        Raises:
            TooManyRequests: Raised when the Flowery API returns a 429 status code
            ClientError: Raised when the Flowery API returns a 4xx status code
            InternalServerError: Raised when the Flowery API returns a 5xx status code
            RetryLimitExceeded: Raised when the retry limit defined in the `FloweryAPIConfig` class (default 3) is exceeded

        Returns:
            Result: A Result object containing the status code, message, and data from the request.
        """
        return await self._do(http_method='GET', endpoint=endpoint, params=params, timeout=timeout)
