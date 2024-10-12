"""GraphQL client handling, including shopifyStream base class."""

from __future__ import annotations

import typing as t

import requests  # noqa: TCH002
from singer_sdk.streams import GraphQLStream

from tap_shopify.auth import shopifyAuthenticator

if t.TYPE_CHECKING:
    from singer_sdk.helpers.types import Context


class shopifyStream(GraphQLStream):
    """shopify stream class."""

    @property
    def url_base(self) -> str:
        """Return the API URL root, configurable via tap settings."""
        # TODO: hardcode a value here, or retrieve it from self.config
        return "https://{store}.myshopify.com/admin/api/2024-10/graphql.json".format(
            store=self.config["store"]
        )

    @property
    def authenticator(self) -> shopifyAuthenticator:
        """Return a new authenticator object.

        Returns:
            An authenticator instance.
        """
        return shopifyAuthenticator.create_for_stream(self)

    @property
    def http_headers(self) -> dict:
        """Return the http headers needed.

        Returns:
            A dictionary of HTTP headers.
        """

        headers = {
            "Content-Type": "application/json",
            "X-Shopify-Access-Token": str(self.config["access_token"]),
        }

        if "user_agent" in self.config:
            headers["User-Agent"] = self.config.get("user_agent")

        return headers

    def parse_response(self, response: requests.Response) -> t.Iterable[dict]:
        """Parse the response and return an iterator of result records."""
        resp_json = response.json()

        orders = resp_json.get("data", {}).get("orders", {}).get("edges", [])

        if not orders:
            self.logger.warning("No orders found in the response.")
            return

        for order in orders:
            yield order.get(
                "node", {}
            )  # Yield only the 'node' object, which contains the order details

    def post_process(
        self,
        row: dict,
        context: Context | None = None,  # noqa: ARG002
    ) -> dict | None:
        """As needed, append or transform raw data to match expected structure.

        Args:
            row: An individual record from the stream.
            context: The stream context.

        Returns:
            The updated record dictionary, or ``None`` to skip the record.
        """
        # TODO: Delete this method if not needed.
        return row
