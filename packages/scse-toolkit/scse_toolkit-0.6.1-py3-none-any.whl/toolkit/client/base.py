import functools
import logging
from json.decoder import JSONDecodeError
from typing import TYPE_CHECKING, Callable

import httpx

from toolkit import utils
from toolkit.exceptions import ServerError, ServiceException

if TYPE_CHECKING:
    from .auth import Auth

logger = logging.getLogger(__name__)


class ServiceClient(object):
    url: str
    auth: "Auth | None"
    http_client: httpx.Client

    def __init__(
        self,
        url: str,
        auth: "Auth | None" = None,
        timeout: int = 10,
        cache_ttl: int = 60 * 15,
    ) -> None:
        self.url = url
        self.auth = auth
        self.ttl_cache = utils.ttl_cache(cache_ttl)

        logger.debug(f"Making new http service client for url={url} auth={auth}.")
        self.http_client = httpx.Client(
            base_url=self.url,
            timeout=timeout,
            http2=True,
            auth=auth,
        )

    def raise_code_or_unknown(self, name: str | None, res: httpx.Response):
        try:
            raise ServiceException.from_status_code(res.status_code)
        except ValueError:
            raise ServerError(http_error_name=name, http_status_code=res.status_code)

    def raise_dict_or_unknown(self, dict_: dict, res: httpx.Response):
        try:
            raise ServiceException.from_dict(dict_)
        except ValueError:
            self.raise_code_or_unknown(dict_.get("name"), res)

    def raise_service_exception(self, res: httpx.Response):
        if res.is_error:
            try:
                json = res.json()
            except (ValueError, JSONDecodeError):
                self.raise_code_or_unknown(res.text, res)

            self.raise_dict_or_unknown(json, res)

    def jti_cache(self, func: Callable):
        """Caches a functions results for each unique jwt id using `utils.ttl_cache`"""

        @self.ttl_cache
        def jti_func(*args, jti=None, **kwargs):
            del jti
            return func(*args, **kwargs)

        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> bool:
            jti = None
            if self.auth is not None:
                if self.auth.access_token is not None:
                    jti = self.auth.access_token.jti
            return jti_func(*args, jti=jti, **kwargs)

        return wrapper
