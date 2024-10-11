"""shopify Authentication."""

from __future__ import annotations

from singer_sdk.authenticators import APIKeyAuthenticator, SingletonMeta


# The SingletonMeta metaclass makes your streams reuse the same authenticator instance.
# If this behaviour interferes with your use-case, you can remove the metaclass.
class shopifyAuthenticator(APIKeyAuthenticator, metaclass=SingletonMeta):
    """Authenticator class for shopify."""

    @classmethod
    def create_for_stream(cls, stream) -> shopifyAuthenticator:  # noqa: ANN001
        """Instantiate an authenticator for a specific Singer stream.

        Args:
            stream: The Singer stream instance.

        Returns:
            A new authenticator.
        """
        return cls(
            stream=stream,
            key="X-Shopify-Access-Token",
            value=stream.config["access_token"],
            location="header",
        )
