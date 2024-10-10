"""
Type annotations for mediastore-data service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_mediastore_data.client import MediaStoreDataClient

    session = get_session()
    async with session.create_client("mediastore-data") as client:
        client: MediaStoreDataClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListItemsPaginator
from .type_defs import (
    DeleteObjectRequestRequestTypeDef,
    DescribeObjectRequestRequestTypeDef,
    DescribeObjectResponseTypeDef,
    GetObjectRequestRequestTypeDef,
    GetObjectResponseTypeDef,
    ListItemsRequestRequestTypeDef,
    ListItemsResponseTypeDef,
    PutObjectRequestRequestTypeDef,
    PutObjectResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("MediaStoreDataClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    ClientError: Type[BotocoreClientError]
    ContainerNotFoundException: Type[BotocoreClientError]
    InternalServerError: Type[BotocoreClientError]
    ObjectNotFoundException: Type[BotocoreClientError]
    RequestedRangeNotSatisfiableException: Type[BotocoreClientError]


class MediaStoreDataClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        MediaStoreDataClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.exceptions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.can_paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.close)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#close)
        """

    async def delete_object(
        self, **kwargs: Unpack[DeleteObjectRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an object at the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.delete_object)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#delete_object)
        """

    async def describe_object(
        self, **kwargs: Unpack[DescribeObjectRequestRequestTypeDef]
    ) -> DescribeObjectResponseTypeDef:
        """
        Gets the headers for an object at the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.describe_object)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#describe_object)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.generate_presigned_url)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#generate_presigned_url)
        """

    async def get_object(
        self, **kwargs: Unpack[GetObjectRequestRequestTypeDef]
    ) -> GetObjectResponseTypeDef:
        """
        Downloads the object at the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.get_object)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#get_object)
        """

    async def list_items(
        self, **kwargs: Unpack[ListItemsRequestRequestTypeDef]
    ) -> ListItemsResponseTypeDef:
        """
        Provides a list of metadata entries about folders and objects in the specified
        folder.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.list_items)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#list_items)
        """

    async def put_object(
        self, **kwargs: Unpack[PutObjectRequestRequestTypeDef]
    ) -> PutObjectResponseTypeDef:
        """
        Uploads an object to the specified path.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.put_object)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#put_object)
        """

    def get_paginator(self, operation_name: Literal["list_items"]) -> ListItemsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/#get_paginator)
        """

    async def __aenter__(self) -> "MediaStoreDataClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/mediastore-data.html#MediaStoreData.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_mediastore_data/client/)
        """
