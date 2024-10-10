"""
Type annotations for lambda service client waiters.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_lambda.client import LambdaClient
    from types_aiobotocore_lambda.waiter import (
        FunctionActiveWaiter,
        FunctionActiveV2Waiter,
        FunctionExistsWaiter,
        FunctionUpdatedWaiter,
        FunctionUpdatedV2Waiter,
        PublishedVersionActiveWaiter,
    )

    session = get_session()
    async with session.create_client("lambda") as client:
        client: LambdaClient

        function_active_waiter: FunctionActiveWaiter = client.get_waiter("function_active")
        function_active_v2_waiter: FunctionActiveV2Waiter = client.get_waiter("function_active_v2")
        function_exists_waiter: FunctionExistsWaiter = client.get_waiter("function_exists")
        function_updated_waiter: FunctionUpdatedWaiter = client.get_waiter("function_updated")
        function_updated_v2_waiter: FunctionUpdatedV2Waiter = client.get_waiter("function_updated_v2")
        published_version_active_waiter: PublishedVersionActiveWaiter = client.get_waiter("published_version_active")
    ```
"""

import sys

from aiobotocore.waiter import AIOWaiter

from .type_defs import (
    GetFunctionConfigurationRequestFunctionActiveWaitTypeDef,
    GetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef,
    GetFunctionConfigurationRequestPublishedVersionActiveWaitTypeDef,
    GetFunctionRequestFunctionActiveV2WaitTypeDef,
    GetFunctionRequestFunctionExistsWaitTypeDef,
    GetFunctionRequestFunctionUpdatedV2WaitTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "FunctionActiveWaiter",
    "FunctionActiveV2Waiter",
    "FunctionExistsWaiter",
    "FunctionUpdatedWaiter",
    "FunctionUpdatedV2Waiter",
    "PublishedVersionActiveWaiter",
)


class FunctionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[GetFunctionConfigurationRequestFunctionActiveWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivewaiter)
        """


class FunctionActiveV2Waiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionActiveV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivev2waiter)
    """

    async def wait(self, **kwargs: Unpack[GetFunctionRequestFunctionActiveV2WaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionActiveV2.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionactivev2waiter)
        """


class FunctionExistsWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionExists)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionexistswaiter)
    """

    async def wait(self, **kwargs: Unpack[GetFunctionRequestFunctionExistsWaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionExists.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionexistswaiter)
        """


class FunctionUpdatedWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionUpdated)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedwaiter)
    """

    async def wait(
        self, **kwargs: Unpack[GetFunctionConfigurationRequestFunctionUpdatedWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionUpdated.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedwaiter)
        """


class FunctionUpdatedV2Waiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionUpdatedV2)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedv2waiter)
    """

    async def wait(self, **kwargs: Unpack[GetFunctionRequestFunctionUpdatedV2WaitTypeDef]) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.FunctionUpdatedV2.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#functionupdatedv2waiter)
        """


class PublishedVersionActiveWaiter(AIOWaiter):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.PublishedVersionActive)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#publishedversionactivewaiter)
    """

    async def wait(
        self, **kwargs: Unpack[GetFunctionConfigurationRequestPublishedVersionActiveWaitTypeDef]
    ) -> None:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/lambda.html#Lambda.Waiter.PublishedVersionActive.wait)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_lambda/waiters/#publishedversionactivewaiter)
        """
