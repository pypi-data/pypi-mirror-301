from __future__ import annotations

import typing as t
import requests
from singer_sdk import typing as th  # JSON Schema typing helpers
from tap_shopify.client import shopifyStream
from datetime import datetime, timezone, timedelta


class OrdersStream(shopifyStream):
    """Orders stream."""

    name = "orders"
    primary_keys: t.ClassVar[list[str]] = ["id"]
    replication_key = "createdAt"
    schema = th.PropertiesList(
        th.Property("id", th.StringType),
        th.Property("name", th.StringType),
        th.Property("createdAt", th.DateTimeType),
        th.Property("referrerUrl", th.StringType),
        th.Property("landingPageUrl", th.StringType),
        th.Property("landingPageDisplayText", th.StringType),
        th.Property("totalRefunded", th.StringType),
        th.Property(
            "totalTipReceived", th.ObjectType(th.Property("amount", th.StringType))
        ),
        th.Property("discountCodes", th.ArrayType(th.StringType), required=False),
        th.Property(
            "channel", th.ObjectType(th.Property("name", th.StringType)), required=False
        ),
        th.Property(
            "currentTotalPriceSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "totalTaxSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "totalDiscountsSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "totalShippingPriceSet",
            th.ObjectType(
                th.Property(
                    "shopMoney", th.ObjectType(th.Property("amount", th.StringType))
                )
            ),
        ),
        th.Property(
            "shippingAddress",
            th.ObjectType(
                th.Property("address1", th.StringType),
                th.Property("address2", th.StringType),
                th.Property("city", th.StringType),
                th.Property("country", th.StringType),
                th.Property("province", th.StringType),
                th.Property("zip", th.StringType),
            ),
        ),
        th.Property(
            "customer",
            th.ObjectType(
                th.Property("displayName", th.StringType),
                th.Property("email", th.StringType),
                th.Property("phone", th.StringType),
            ),
        ),
        th.Property(
            "taxLines",
            th.ArrayType(
                th.ObjectType(th.Property("rate", th.NumberType, required=False))
            ),
            required=False,
        ),
    ).to_dict()

    def query(self, next_page_token=None) -> str:
        """Return the GraphQL query to be executed."""

        replication_key_value = self.get_starting_replication_key_value(context={})
        last_replication_value = replication_key_value or self.config.get("start_date")
        after_cursor = f', after: "{next_page_token}"' if next_page_token else ""

        # Get the current time as a datetime object
        current_time = datetime.now(timezone.utc)

        # Calculate the next day
        next_day = current_time.date() + timedelta(days=1)

        # Combine next day with the minimum time (00:00:00) and set UTC timezone
        next_day_start = datetime.combine(next_day, datetime.min.time()).replace(tzinfo=timezone.utc)

        # Format next_day_start as a string in the desired format
        end_day = next_day_start.strftime("%Y-%m-%dT%H:%M:%SZ")

        self.logger.info(f"end_day: {end_day}")

        return f"""
        query {{
            orders(first: 250, query: "created_at:>={last_replication_value} created_at:<={end_day}", sortKey: CREATED_AT, reverse: false {after_cursor}) {{
                pageInfo {{
                    hasNextPage
                    endCursor
                }}
                edges {{
                    node {{
                        id
                        name
                        createdAt
                        referrerUrl
                        landingPageUrl
                        landingPageDisplayText
                        channel {{
                            name
                        }}
                        totalRefunded
                        discountCodes
                        totalTipReceived {{
                            amount
                        }}
                        currentTotalPriceSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        totalTaxSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        totalDiscountsSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        totalShippingPriceSet {{
                            shopMoney {{
                                amount
                            }}
                        }}
                        shippingAddress {{
                            address1
                            address2
                            city
                            country
                            province
                            zip
                        }}
                        customer {{
                            displayName
                            email
                            phone
                        }}
                        taxLines {{
                            rate
                        }}
                    }}
                }}
            }}
        }}
        """

    def get_next_page_token(self, response, previous_token=None):
        """Extracts the pagination token for the next page."""
        page_info = (
            response.json().get("data", {}).get("orders", {}).get("pageInfo", {})
        )
        return page_info.get("endCursor") if page_info.get("hasNextPage") else None

    def request_records(self, context: dict):
        """Handles requesting and iterating through paginated records."""
        next_page_token = None
        while True:
            query = self.query(next_page_token)
            headers = self.http_headers
            response = requests.post(
                self.url_base, json={"query": query}, headers=headers
            )

            if response.status_code != 200:
                raise RuntimeError(f"GraphQL query failed: {response.text}")

            for record in self.parse_response(response):
                yield record

            next_page_token = self.get_next_page_token(response)
            if not next_page_token:
                break
