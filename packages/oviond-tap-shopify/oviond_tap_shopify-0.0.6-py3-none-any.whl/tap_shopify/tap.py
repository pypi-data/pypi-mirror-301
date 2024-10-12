"""shopify tap class."""

from __future__ import annotations

from singer_sdk import Tap
from singer_sdk import typing as th  # JSON schema typing helpers

# TODO: Import your custom stream types here:
from tap_shopify import streams


class Tapshopify(Tap):
    """shopify tap class."""

    name = "tap-shopify"

    # TODO: Update this section with the actual config values you expect:
    config_jsonschema = th.PropertiesList(
        th.Property(
            "access_token",
            th.StringType,
            required=True,
            secret=True,  # Flag config as protected.
            description="The token to authenticate against the API service",
        ),
        th.Property(
            "store",
            th.StringType,
            required=True,
            description=(
                "Shopify store id, use the prefix of your admin url "
                + "e.g. https://[your store].myshopify.com/admin"
            ),
        ),
        th.Property(
            "start_date",
            th.DateTimeType,
            description="The earliest record date to sync",
        ),
        th.Property(
            "admin_url",
            th.StringType,
            description=(
                "The Admin url for your Shopify store " + "(overrides 'store' property)"
            ),
        ),
        th.Property(
            "is_plus_account",
            th.BooleanType,
            description=("Enabled Shopify plus account endpoints."),
        ),
    ).to_dict()

    def discover_streams(self) -> list[streams.shopifyStream]:
        """Return a list of discovered streams.

        Returns:
            A list of discovered streams.
        """
        return [
            streams.OrdersStream(self),
        ]


if __name__ == "__main__":
    Tapshopify.cli()
