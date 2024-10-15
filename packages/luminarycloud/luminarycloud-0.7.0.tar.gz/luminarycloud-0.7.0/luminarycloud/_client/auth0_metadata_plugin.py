# Copyright 2023 Luminary Cloud, Inc. All Rights Reserved.

import grpc

from .._auth import Auth0Client


class Auth0MetadataPlugin(grpc.AuthMetadataPlugin):
    """
    Adds fresh Bearer tokens as auth headers for each outgoing RPC.

    The __call__ function is invoked for every outgoing call. If the
    token has expired or doesn't exist, the Auth0 client tries to
    acquire a new one.
    """

    def __init__(self, auth0_client: Auth0Client):
        super(Auth0MetadataPlugin, self).__init__()
        self.auth0_client = auth0_client

    def __call__(
        self,
        context: grpc.AuthMetadataContext,
        # Takes the list of headers to add as tuples
        callback: grpc.AuthMetadataPluginCallback,
    ) -> None:
        try:
            access_token = self.auth0_client.fetch_access_token()
        except Exception as err:
            callback(None, err)
        else:
            metadata = [
                ("authorization", "Bearer " + access_token),
            ]
            callback(metadata, None)
