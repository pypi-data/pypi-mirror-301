"""
Type annotations for iotsecuretunneling service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_iotsecuretunneling.client import IoTSecureTunnelingClient

    session = get_session()
    async with session.create_client("iotsecuretunneling") as client:
        client: IoTSecureTunnelingClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    CloseTunnelRequestRequestTypeDef,
    DescribeTunnelRequestRequestTypeDef,
    DescribeTunnelResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListTunnelsRequestRequestTypeDef,
    ListTunnelsResponseTypeDef,
    OpenTunnelRequestRequestTypeDef,
    OpenTunnelResponseTypeDef,
    RotateTunnelAccessTokenRequestRequestTypeDef,
    RotateTunnelAccessTokenResponseTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = ("IoTSecureTunnelingClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]

class IoTSecureTunnelingClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        IoTSecureTunnelingClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.exceptions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.can_paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.close)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#close)
        """

    async def close_tunnel(
        self, **kwargs: Unpack[CloseTunnelRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Closes a tunnel identified by the unique tunnel id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.close_tunnel)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#close_tunnel)
        """

    async def describe_tunnel(
        self, **kwargs: Unpack[DescribeTunnelRequestRequestTypeDef]
    ) -> DescribeTunnelResponseTypeDef:
        """
        Gets information about a tunnel identified by the unique tunnel id.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.describe_tunnel)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#describe_tunnel)
        """

    async def generate_presigned_url(
        self,
        ClientMethod: str,
        Params: Mapping[str, Any] = ...,
        ExpiresIn: int = 3600,
        HttpMethod: str = ...,
    ) -> str:
        """
        Generate a presigned url given a client, its method, and arguments.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.generate_presigned_url)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#generate_presigned_url)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Lists the tags for the specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.list_tags_for_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#list_tags_for_resource)
        """

    async def list_tunnels(
        self, **kwargs: Unpack[ListTunnelsRequestRequestTypeDef]
    ) -> ListTunnelsResponseTypeDef:
        """
        List all tunnels for an Amazon Web Services account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.list_tunnels)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#list_tunnels)
        """

    async def open_tunnel(
        self, **kwargs: Unpack[OpenTunnelRequestRequestTypeDef]
    ) -> OpenTunnelResponseTypeDef:
        """
        Creates a new tunnel, and returns two client access tokens for clients to use
        to connect to the IoT Secure Tunneling proxy
        server.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.open_tunnel)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#open_tunnel)
        """

    async def rotate_tunnel_access_token(
        self, **kwargs: Unpack[RotateTunnelAccessTokenRequestRequestTypeDef]
    ) -> RotateTunnelAccessTokenResponseTypeDef:
        """
        Revokes the current client access token (CAT) and returns new CAT for clients
        to use when reconnecting to secure tunneling to access the same
        tunnel.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.rotate_tunnel_access_token)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#rotate_tunnel_access_token)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        A resource tag.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.tag_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client.untag_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/#untag_resource)
        """

    async def __aenter__(self) -> "IoTSecureTunnelingClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/iotsecuretunneling.html#IoTSecureTunneling.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_iotsecuretunneling/client/)
        """
