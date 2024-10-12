from __future__ import annotations
import typing as t
from singer_sdk.authenticators import APIKeyAuthenticator
from singer_sdk.helpers.jsonpath import extract_jsonpath
from singer_sdk.pagination import BaseOffsetPaginator
from singer_sdk.streams import RESTStream
from singer_sdk.helpers.types import Context
from datetime import datetime, timezone


class brevoStream(RESTStream):
    """brevo stream class."""

    records_jsonpath = "$[*]"
    next_page_token_jsonpath = None  # Not using jsonpath for offset pagination

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return "https://api.sendinblue.com/v3"

    @property
    def authenticator(self) -> APIKeyAuthenticator:
        return APIKeyAuthenticator.create_for_stream(
            self,
            key="api-key",
            value=self.config.get("api_key", ""),
            location="header",
        )
