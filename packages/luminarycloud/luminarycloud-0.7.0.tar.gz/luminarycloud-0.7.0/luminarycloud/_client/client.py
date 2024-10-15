# Copyright 2023-2024 Luminary Cloud, Inc. All Rights Reserved.

import logging
import re
from contextvars import ContextVar
from collections.abc import Iterable
from typing import Any, Optional, cast

import grpc

from .._auth import Auth0Client
from .._proto.api.v0.luminarycloud.geometry.geometry_pb2_grpc import GeometryServiceStub
from .._proto.api.v0.luminarycloud.mesh.mesh_pb2_grpc import MeshServiceStub
from .._proto.api.v0.luminarycloud.project.project_pb2_grpc import ProjectServiceStub
from .._proto.api.v0.luminarycloud.simulation.simulation_pb2_grpc import (
    SimulationServiceStub,
)
from .._proto.api.v0.luminarycloud.simulation_template.simulation_template_pb2_grpc import (
    SimulationTemplateServiceStub,
)
from .._proto.api.v0.luminarycloud.solution.solution_pb2_grpc import SolutionServiceStub
from .._proto.api.v0.luminarycloud.upload.upload_pb2_grpc import UploadServiceStub
from .auth0_metadata_plugin import Auth0MetadataPlugin
from .config import LC_DOMAIN
from .logging_interceptor import LoggingInterceptor
from .retry_interceptor import RetryInterceptor
from .tracing import add_instrumentation

logger = logging.getLogger(__name__)


class Client(
    ProjectServiceStub,
    MeshServiceStub,
    SimulationServiceStub,
    SimulationTemplateServiceStub,
    GeometryServiceStub,
    SolutionServiceStub,
    UploadServiceStub,
):
    """
    Creates a Luminary API client.

    The returned client automatically obtains access tokens for the Luminary API and
    sends them with each RPC call. See auth/auth.py for details.

    Supports "with" syntax to set as the default client for all API calls inside the
    "with" block. Exiting the block restores the previous default client.

    Parameters
    ----------
    target : str
        The URL of the API server.
    localhost : bool
        True if the API server is running locally.
    grpc_channel_options : Optional[Iterable[tuple[str, str]]]
        A list of gRPC channel args. The full list is available here:
        https://github.com/grpc/grpc/blob/v1.46.x/include/grpc/impl/codegen/grpc_types.h
    **kwargs : dict, optional
        Additional arguments are passed to Auth0Client. See auth/auth.py.

    Examples
    --------
    Using the "with" syntax to set the default client within a scope:

    >>> import luminarycloud as lc
    >>> with lc.Client(access_token="blahblahblah"):
    >>>     project = lc.list_projects()[0]
    >>>     sims = project.list_simulations()
    """

    def __init__(
        self,
        target: str = LC_DOMAIN,
        localhost: bool = False,
        grpc_channel_options: Optional[Iterable[tuple[str, str]]] = None,
        channel_credentials: Optional[grpc.ChannelCredentials] = None,
        **kwargs: Any,
    ):
        self._target = target
        self._apiserver_domain = target.split(":", maxsplit=1)[0]
        self._auth0_client = Auth0Client(**kwargs)
        self._channel = self._create_channel(localhost, grpc_channel_options, channel_credentials)
        self._context_tokens = []
        ProjectServiceStub.__init__(self, self._channel)
        MeshServiceStub.__init__(self, self._channel)
        SimulationServiceStub.__init__(self, self._channel)
        GeometryServiceStub.__init__(self, self._channel)
        UploadServiceStub.__init__(self, self._channel)
        SolutionServiceStub.__init__(self, self._channel)
        SimulationTemplateServiceStub.__init__(self, self._channel)

    @property
    def channel(self) -> grpc.ChannelCredentials:
        return self._channel

    @property
    def apiserver_domain(self) -> str:
        return self._apiserver_domain

    @property
    def primary_domain(self) -> Optional[str]:
        return _get_primary_domain_for_apiserver_domain(self._apiserver_domain)

    @property
    def internal(self) -> bool:
        return _is_internal_domain_for_lc_apiserver(self._apiserver_domain)

    def get_token(self) -> str:
        return self._auth0_client.fetch_access_token()

    def __enter__(self) -> "Client":
        self._context_tokens.append(_DEFAULT_CLIENT.set(self))
        return self

    def __exit__(self, *exc: Any) -> None:
        _DEFAULT_CLIENT.reset(self._context_tokens.pop())

    def _create_channel(
        self,
        localhost: bool = False,
        grpc_channel_options: Optional[Iterable[tuple[str, str]]] = None,
        channel_credentials: Optional[grpc.ChannelCredentials] = None,
    ) -> grpc.ChannelCredentials:
        if channel_credentials is None:
            if localhost:
                logger.debug("Using local channel credentials.")
                channel_credentials = grpc.local_channel_credentials()
            else:
                logger.debug("Using SSL channel credentials.")
                channel_credentials = grpc.ssl_channel_credentials()
        metadata_plugin = Auth0MetadataPlugin(self._auth0_client)
        auth0_credentials = grpc.metadata_call_credentials(metadata_plugin)
        options = grpc_channel_options and list(grpc_channel_options)
        channel = grpc.secure_channel(
            self._target,
            grpc.composite_channel_credentials(
                cast(grpc.ChannelCredentials, channel_credentials),
                auth0_credentials,
            ),
            options=options,
        )
        intercepted_channel = grpc.intercept_channel(
            channel,
            LoggingInterceptor(),
            RetryInterceptor(),
        )
        return add_instrumentation(
            intercepted_channel, self._target, self.primary_domain, self._auth0_client
        )


def _is_internal_domain_for_lc_apiserver(domain_name: str) -> bool:
    """Returns true iff the domain is an internal (non-prod) apiserver domain."""
    return re.match(r"apis[\.-].+\.luminarycloud\.com", domain_name) is not None


def _get_primary_domain_for_apiserver_domain(apiserver_domain: str) -> Optional[str]:
    """
    Get the frontend (primary) domain given an apiserver domain
    apis.luminarycloud.com -> app.luminarycloud.com
    apis-foo.int.luminarycloud.com -> foo.int.luminarycloud.com
    """
    if apiserver_domain == "apis.luminarycloud.com":  # prod
        return "app.luminarycloud.com"
    if apiserver_domain == "apis-itar.luminarycloud.com":  # itar-prod
        return "app-itar.luminarycloud.com"
    elif _is_internal_domain_for_lc_apiserver(apiserver_domain):
        return re.sub(r"^apis[-\.]{1}", "", apiserver_domain)
    return None


_DEFAULT_CLIENT = ContextVar("luminarycloud_client", default=Client())
