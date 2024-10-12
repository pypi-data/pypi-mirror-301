"""Stream type classes for tap-brevo."""

from __future__ import annotations
from typing import Optional
from importlib import resources
from singer_sdk import typing as th  # JSON Schema typing helpers
from tap_brevo.client import brevoStream
from singer_sdk.helpers.types import Context
from datetime import datetime, timezone
import typing as t
from singer_sdk.pagination import BaseOffsetPaginator
from singer_sdk.helpers.jsonpath import extract_jsonpath

# TODO: Delete this is if not using json files for schema definition
SCHEMAS_DIR = resources.files(__package__) / "schemas"
# TODO: - Override `UsersStream` and `GroupsStream` with your own stream definition.
#       - Copy-paste as many times as needed to create multiple stream types.


class ListsStream(brevoStream):
    """Define custom stream."""

    name = "lists"
    path = "/contacts/lists"
    primary_keys = ["id"]
    replication_key = None
    records_jsonpath = "$.lists[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("totalBlacklisted", th.IntegerType),
        th.Property("totalSubscribers", th.IntegerType),
        th.Property("uniqueSubscribers", th.IntegerType),
        th.Property("folderId", th.IntegerType),
    ).to_dict()
    
    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a paginator for offset-based pagination."""
        return BaseOffsetPaginator(start_value=0, page_size=50)

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        return params
    
    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        # Basic params: limit and sort
        params = { "limit": 50, "offset": 0, "sort": "asc" }

        # Pagination logic
        if next_page_token:
            params["offset"] = next_page_token

        return params
    
    def parse_response(self, response: t.Any) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

        # Get current offset and total records
        current_offset = response.json().get("offset", 0)
        total_records = response.json().get("total", 0)

        # Set next page token (offset) if more records exist
        if current_offset + 50 < total_records:
            self._page_token = current_offset + 50
        else:
            self._page_token = None


class CampaignsStream(brevoStream):
    """Define custom stream."""

    name = "campaigns"
    path = "/emailCampaigns"
    primary_keys = ["id"]
    replication_key = "createdAt"
    records_jsonpath = "$.campaigns[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("subject", th.StringType),
        th.Property("type", th.StringType),
        th.Property("status", th.StringType),
        th.Property("scheduledAt", th.StringType),
        th.Property("testSent", th.BooleanType),
        th.Property("header", th.StringType),
        th.Property("footer", th.StringType),
        th.Property(
            "sender",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("replyTo", th.StringType),
        th.Property("toField", th.StringType),
        th.Property("shareLink", th.StringType),
        th.Property("tag", th.StringType),
        th.Property("createdAt", th.StringType),
        th.Property("modifiedAt", th.StringType),
        th.Property("inlineImageActivation", th.BooleanType),
        th.Property("mirrorActive", th.BooleanType),
        th.Property("recurring", th.BooleanType),
        th.Property(
            "recipients",
            th.ObjectType(additional_properties=True),
        ),
        th.Property("statistics", th.ObjectType(additional_properties=True)),
    ).to_dict()

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a paginator for offset-based pagination."""
        return BaseOffsetPaginator(start_value=0, page_size=100)

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        return params

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        # Basic params: limit and sort
        params = { "limit": 100, "offset": 0, "sort": "asc", "excludeHtmlContent": True }

        # Pagination logic
        if next_page_token:
            params["offset"] = next_page_token

        # Use timezone-aware current time in UTC
        end_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Start with the config start_date or use replication key
        start_date = self.config.get("start_date")

        if self.replication_key and self.get_starting_replication_key_value(context):
            start_date = self.get_starting_replication_key_value(context)

        # If we have a start_date, apply both startDate and endDate
        if start_date:
            params["startDate"] = start_date
            params["endDate"] = end_date  # endDate is required when startDate is used

        return params
    
    def parse_response(self, response: t.Any) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

        # Get current offset and total records
        current_offset = response.json().get("offset", 0)
        total_records = response.json().get("total", 0)

        # Set next page token (offset) if more records exist
        if current_offset + 100 < total_records:
            self._page_token = current_offset + 100
        else:
            self._page_token = None


class SMSCampaignsStream(brevoStream):
    """Define custom stream."""

    name = "sms_campaigns"
    path = "/smsCampaigns"
    primary_keys = ["id"]
    replication_key = "createdAt"
    records_jsonpath = "$.campaigns[*]"
    schema = th.PropertiesList(
        th.Property("id", th.IntegerType),
        th.Property("name", th.StringType),
        th.Property("status", th.StringType),
        th.Property("content", th.StringType),
        th.Property("scheduledAt", th.StringType),
        th.Property("testSent", th.BooleanType),
        th.Property("sender", th.StringType),
        th.Property("createdAt", th.StringType),
        th.Property("modifiedAt", th.StringType),
        th.Property("recipients", th.ObjectType()),
        th.Property("statistics", th.ObjectType()),
    ).to_dict()

    def get_new_paginator(self) -> BaseOffsetPaginator:
        """Create a paginator for offset-based pagination."""
        return BaseOffsetPaginator(start_value=0, page_size=1000)

    def get_url_params(self, context, next_page_token):
        params = super().get_url_params(context, next_page_token)
        return params

    def get_url_params(
        self,
        context: Context | None,
        next_page_token: t.Any | None,
    ) -> dict[str, t.Any]:
        """Return a dictionary of values to be used in URL parameterization."""
        # Basic params: limit and sort
        params = {"limit": 1000, "offset": 0, "sort": "asc" }

        # Pagination logic
        if next_page_token:
            params["offset"] = next_page_token

        # Use timezone-aware current time in UTC
        end_date = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")

        # Start with the config start_date or use replication key
        start_date = self.config.get("start_date")

        if self.replication_key and self.get_starting_replication_key_value(context):
            start_date = self.get_starting_replication_key_value(context)

        # If we have a start_date, apply both startDate and endDate
        if start_date:
            params["startDate"] = start_date
            params["endDate"] = end_date  # endDate is required when startDate is used

        return params

    def parse_response(self, response: t.Any) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        yield from extract_jsonpath(self.records_jsonpath, input=response.json())

        # Get current offset and total records
        current_offset = response.json().get("offset", 0)
        total_records = response.json().get("total", 0)

        # Set next page token (offset) if more records exist
        if current_offset + 1000 < total_records:
            self._page_token = current_offset + 1000
        else:
            self._page_token = None
