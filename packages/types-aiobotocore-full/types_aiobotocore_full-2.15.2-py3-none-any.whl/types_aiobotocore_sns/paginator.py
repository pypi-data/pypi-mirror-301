"""
Type annotations for sns service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sns.client import SNSClient
    from types_aiobotocore_sns.paginator import (
        ListEndpointsByPlatformApplicationPaginator,
        ListOriginationNumbersPaginator,
        ListPhoneNumbersOptedOutPaginator,
        ListPlatformApplicationsPaginator,
        ListSMSSandboxPhoneNumbersPaginator,
        ListSubscriptionsPaginator,
        ListSubscriptionsByTopicPaginator,
        ListTopicsPaginator,
    )

    session = get_session()
    with session.create_client("sns") as client:
        client: SNSClient

        list_endpoints_by_platform_application_paginator: ListEndpointsByPlatformApplicationPaginator = client.get_paginator("list_endpoints_by_platform_application")
        list_origination_numbers_paginator: ListOriginationNumbersPaginator = client.get_paginator("list_origination_numbers")
        list_phone_numbers_opted_out_paginator: ListPhoneNumbersOptedOutPaginator = client.get_paginator("list_phone_numbers_opted_out")
        list_platform_applications_paginator: ListPlatformApplicationsPaginator = client.get_paginator("list_platform_applications")
        list_sms_sandbox_phone_numbers_paginator: ListSMSSandboxPhoneNumbersPaginator = client.get_paginator("list_sms_sandbox_phone_numbers")
        list_subscriptions_paginator: ListSubscriptionsPaginator = client.get_paginator("list_subscriptions")
        list_subscriptions_by_topic_paginator: ListSubscriptionsByTopicPaginator = client.get_paginator("list_subscriptions_by_topic")
        list_topics_paginator: ListTopicsPaginator = client.get_paginator("list_topics")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef,
    ListEndpointsByPlatformApplicationResponseTypeDef,
    ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef,
    ListOriginationNumbersResultTypeDef,
    ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef,
    ListPhoneNumbersOptedOutResponseTypeDef,
    ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef,
    ListPlatformApplicationsResponseTypeDef,
    ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef,
    ListSMSSandboxPhoneNumbersResultTypeDef,
    ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef,
    ListSubscriptionsByTopicResponseTypeDef,
    ListSubscriptionsInputListSubscriptionsPaginateTypeDef,
    ListSubscriptionsResponseTypeDef,
    ListTopicsInputListTopicsPaginateTypeDef,
    ListTopicsResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "ListEndpointsByPlatformApplicationPaginator",
    "ListOriginationNumbersPaginator",
    "ListPhoneNumbersOptedOutPaginator",
    "ListPlatformApplicationsPaginator",
    "ListSMSSandboxPhoneNumbersPaginator",
    "ListSubscriptionsPaginator",
    "ListSubscriptionsByTopicPaginator",
    "ListTopicsPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class ListEndpointsByPlatformApplicationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListEndpointsByPlatformApplication)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listendpointsbyplatformapplicationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            ListEndpointsByPlatformApplicationInputListEndpointsByPlatformApplicationPaginateTypeDef
        ],
    ) -> AsyncIterator[ListEndpointsByPlatformApplicationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListEndpointsByPlatformApplication.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listendpointsbyplatformapplicationpaginator)
        """


class ListOriginationNumbersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListOriginationNumbers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listoriginationnumberspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListOriginationNumbersRequestListOriginationNumbersPaginateTypeDef]
    ) -> AsyncIterator[ListOriginationNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListOriginationNumbers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listoriginationnumberspaginator)
        """


class ListPhoneNumbersOptedOutPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListPhoneNumbersOptedOut)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listphonenumbersoptedoutpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPhoneNumbersOptedOutInputListPhoneNumbersOptedOutPaginateTypeDef]
    ) -> AsyncIterator[ListPhoneNumbersOptedOutResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListPhoneNumbersOptedOut.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listphonenumbersoptedoutpaginator)
        """


class ListPlatformApplicationsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListPlatformApplications)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listplatformapplicationspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListPlatformApplicationsInputListPlatformApplicationsPaginateTypeDef]
    ) -> AsyncIterator[ListPlatformApplicationsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListPlatformApplications.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listplatformapplicationspaginator)
        """


class ListSMSSandboxPhoneNumbersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListSMSSandboxPhoneNumbers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsmssandboxphonenumberspaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[ListSMSSandboxPhoneNumbersInputListSMSSandboxPhoneNumbersPaginateTypeDef],
    ) -> AsyncIterator[ListSMSSandboxPhoneNumbersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListSMSSandboxPhoneNumbers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsmssandboxphonenumberspaginator)
        """


class ListSubscriptionsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListSubscriptions)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscriptionsInputListSubscriptionsPaginateTypeDef]
    ) -> AsyncIterator[ListSubscriptionsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListSubscriptions.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionspaginator)
        """


class ListSubscriptionsByTopicPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListSubscriptionsByTopic)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionsbytopicpaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListSubscriptionsByTopicInputListSubscriptionsByTopicPaginateTypeDef]
    ) -> AsyncIterator[ListSubscriptionsByTopicResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListSubscriptionsByTopic.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listsubscriptionsbytopicpaginator)
        """


class ListTopicsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListTopics)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listtopicspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[ListTopicsInputListTopicsPaginateTypeDef]
    ) -> AsyncIterator[ListTopicsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Paginator.ListTopics.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/paginators/#listtopicspaginator)
        """
