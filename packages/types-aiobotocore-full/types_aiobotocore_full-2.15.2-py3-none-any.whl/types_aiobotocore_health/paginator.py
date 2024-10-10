"""
Type annotations for health service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_health.client import HealthClient
    from types_aiobotocore_health.paginator import (
        DescribeAffectedAccountsForOrganizationPaginator,
        DescribeAffectedEntitiesPaginator,
        DescribeAffectedEntitiesForOrganizationPaginator,
        DescribeEventAggregatesPaginator,
        DescribeEventTypesPaginator,
        DescribeEventsPaginator,
        DescribeEventsForOrganizationPaginator,
    )

    session = get_session()
    with session.create_client("health") as client:
        client: HealthClient

        describe_affected_accounts_for_organization_paginator: DescribeAffectedAccountsForOrganizationPaginator = client.get_paginator("describe_affected_accounts_for_organization")
        describe_affected_entities_paginator: DescribeAffectedEntitiesPaginator = client.get_paginator("describe_affected_entities")
        describe_affected_entities_for_organization_paginator: DescribeAffectedEntitiesForOrganizationPaginator = client.get_paginator("describe_affected_entities_for_organization")
        describe_event_aggregates_paginator: DescribeEventAggregatesPaginator = client.get_paginator("describe_event_aggregates")
        describe_event_types_paginator: DescribeEventTypesPaginator = client.get_paginator("describe_event_types")
        describe_events_paginator: DescribeEventsPaginator = client.get_paginator("describe_events")
        describe_events_for_organization_paginator: DescribeEventsForOrganizationPaginator = client.get_paginator("describe_events_for_organization")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef,
    DescribeAffectedAccountsForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef,
    DescribeAffectedEntitiesForOrganizationResponseTypeDef,
    DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef,
    DescribeAffectedEntitiesResponseTypeDef,
    DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef,
    DescribeEventAggregatesResponseTypeDef,
    DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef,
    DescribeEventsForOrganizationResponseTypeDef,
    DescribeEventsRequestDescribeEventsPaginateTypeDef,
    DescribeEventsResponseTypeDef,
    DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef,
    DescribeEventTypesResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "DescribeAffectedAccountsForOrganizationPaginator",
    "DescribeAffectedEntitiesPaginator",
    "DescribeAffectedEntitiesForOrganizationPaginator",
    "DescribeEventAggregatesPaginator",
    "DescribeEventTypesPaginator",
    "DescribeEventsPaginator",
    "DescribeEventsForOrganizationPaginator",
)


_ItemTypeDef = TypeVar("_ItemTypeDef")


class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """


class DescribeAffectedAccountsForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeAffectedAccountsForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedaccountsfororganizationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAffectedAccountsForOrganizationRequestDescribeAffectedAccountsForOrganizationPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeAffectedAccountsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeAffectedAccountsForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedaccountsfororganizationpaginator)
        """


class DescribeAffectedEntitiesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeAffectedEntities)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiespaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[DescribeAffectedEntitiesRequestDescribeAffectedEntitiesPaginateTypeDef],
    ) -> AsyncIterator[DescribeAffectedEntitiesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeAffectedEntities.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiespaginator)
        """


class DescribeAffectedEntitiesForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeAffectedEntitiesForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiesfororganizationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeAffectedEntitiesForOrganizationRequestDescribeAffectedEntitiesForOrganizationPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeAffectedEntitiesForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeAffectedEntitiesForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeaffectedentitiesfororganizationpaginator)
        """


class DescribeEventAggregatesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEventAggregates)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventaggregatespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEventAggregatesRequestDescribeEventAggregatesPaginateTypeDef]
    ) -> AsyncIterator[DescribeEventAggregatesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEventAggregates.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventaggregatespaginator)
        """


class DescribeEventTypesPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEventTypes)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventtypespaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEventTypesRequestDescribeEventTypesPaginateTypeDef]
    ) -> AsyncIterator[DescribeEventTypesResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEventTypes.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventtypespaginator)
        """


class DescribeEventsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEvents)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventspaginator)
    """

    def paginate(
        self, **kwargs: Unpack[DescribeEventsRequestDescribeEventsPaginateTypeDef]
    ) -> AsyncIterator[DescribeEventsResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEvents.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventspaginator)
        """


class DescribeEventsForOrganizationPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEventsForOrganization)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventsfororganizationpaginator)
    """

    def paginate(
        self,
        **kwargs: Unpack[
            DescribeEventsForOrganizationRequestDescribeEventsForOrganizationPaginateTypeDef
        ],
    ) -> AsyncIterator[DescribeEventsForOrganizationResponseTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/health.html#Health.Paginator.DescribeEventsForOrganization.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_health/paginators/#describeeventsfororganizationpaginator)
        """
