# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.
import logging
import re
from typing import Optional, Any

import requests
from grpc import Channel
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.grpc import client_interceptor, intercept_channel
from opentelemetry.sdk.resources import SERVICE_NAME, SERVICE_VERSION, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    SpanExportResult,
)

from .. import __version__
from .._auth import Auth0Client

logger = logging.getLogger(__name__)

# By default, OpenTelemetry Python uses W3C Trace Context and W3C Baggage for propagation:
# https://opentelemetry.io/docs/instrumentation/python/manual/#change-the-default-propagation-format

_resource = Resource(
    attributes={
        SERVICE_NAME: "python/sdk",
        SERVICE_VERSION: __version__,
    }
)


# This is a hack to get opentelemetry to skip SSL verification when exporting traces.
# We do it this way because opentelemetry overrides the `verify` option in their code when they make
# the POST request.
class InsecureSession(requests.Session):
    def post(self, *args: Any, **kwargs: Any) -> Any:
        kwargs["verify"] = False
        return super(InsecureSession, self).post(*args, **kwargs)


# We're creating our own SpanExporter here so that we can dynamically update the
# auth headers with the latest credentials across token refreshes.
class Auth0SpanExporter(OTLPSpanExporter):
    def __init__(
        self,
        auth0_client: Auth0Client,
        endpoint: str,
        verify_ssl: bool = True,
    ):
        session = None
        if not verify_ssl:
            session = InsecureSession()
        OTLPSpanExporter.__init__(self, endpoint=endpoint, session=session)
        self.auth0_client = auth0_client

    def export(self, spans: Any) -> SpanExportResult:
        token = self.auth0_client.fetch_access_token()
        headers = {
            "authorization": "Bearer " + token,
        }
        self._session.headers.update(headers)
        return OTLPSpanExporter.export(self, spans)


def _get_collector_endpoint(primary_domain: str) -> str:
    """Get the opentelemetry collector endpoint given the primary domain."""
    return f"https://{primary_domain}/v1/traces"


def _add_instrumentation(
    channel: Channel,
    endpoint: str,
    auth0_client: Auth0Client,
    verify_ssl: bool = True,
) -> Channel:
    provider = TracerProvider(resource=_resource)
    processor = BatchSpanProcessor(
        Auth0SpanExporter(
            endpoint=endpoint,
            auth0_client=auth0_client,
            verify_ssl=verify_ssl,
        )
    )
    provider.add_span_processor(processor)
    return intercept_channel(
        channel,
        client_interceptor(tracer_provider=provider),
    )


def add_instrumentation(
    channel: Channel,
    apiserver_domain: str,
    primary_domain: Optional[str],
    auth0_client: Auth0Client,
) -> Channel:
    if primary_domain is None or "itar" in primary_domain:
        logger.debug("Tracing is disabled for this gRPC client.")
        return channel

    endpoint = _get_collector_endpoint(primary_domain)

    # skip SSL verification for internal domains
    verify_ssl = ".int." not in apiserver_domain
    if not verify_ssl:
        logger.debug("SSL verification will be skipped when exporting traces.")

    logger.debug("Adding tracing instrumentation to gRPC client.")
    return _add_instrumentation(
        channel,
        endpoint,
        auth0_client,
        verify_ssl,
    )
