from typing import Any

from .base import BaseEndpoint as BaseEndpoint

log: Any

class RequestTokenEndpoint(BaseEndpoint):
    def create_request_token(self, request, credentials): ...
    def create_request_token_response(
        self, uri, http_method: str = ..., body: Any | None = ..., headers: Any | None = ..., credentials: Any | None = ...
    ): ...
    def validate_request_token_request(self, request): ...