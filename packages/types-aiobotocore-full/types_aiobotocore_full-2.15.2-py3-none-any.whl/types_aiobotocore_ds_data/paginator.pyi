"""
Type annotations for ds-data service client paginators.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_ds_data.client import DirectoryServiceDataClient
    from types_aiobotocore_ds_data.paginator import (
        ListGroupMembersPaginator,
        ListGroupsPaginator,
        ListGroupsForMemberPaginator,
        ListUsersPaginator,
        SearchGroupsPaginator,
        SearchUsersPaginator,
    )

    session = get_session()
    with session.create_client("ds-data") as client:
        client: DirectoryServiceDataClient

        list_group_members_paginator: ListGroupMembersPaginator = client.get_paginator("list_group_members")
        list_groups_paginator: ListGroupsPaginator = client.get_paginator("list_groups")
        list_groups_for_member_paginator: ListGroupsForMemberPaginator = client.get_paginator("list_groups_for_member")
        list_users_paginator: ListUsersPaginator = client.get_paginator("list_users")
        search_groups_paginator: SearchGroupsPaginator = client.get_paginator("search_groups")
        search_users_paginator: SearchUsersPaginator = client.get_paginator("search_users")
    ```
"""

import sys
from typing import AsyncIterator, Generic, Iterator, TypeVar

from aiobotocore.paginate import AioPaginator
from botocore.paginate import PageIterator

from .type_defs import (
    ListGroupMembersRequestListGroupMembersPaginateTypeDef,
    ListGroupMembersResultTypeDef,
    ListGroupsForMemberRequestListGroupsForMemberPaginateTypeDef,
    ListGroupsForMemberResultTypeDef,
    ListGroupsRequestListGroupsPaginateTypeDef,
    ListGroupsResultTypeDef,
    ListUsersRequestListUsersPaginateTypeDef,
    ListUsersResultTypeDef,
    SearchGroupsRequestSearchGroupsPaginateTypeDef,
    SearchGroupsResultTypeDef,
    SearchUsersRequestSearchUsersPaginateTypeDef,
    SearchUsersResultTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack

__all__ = (
    "ListGroupMembersPaginator",
    "ListGroupsPaginator",
    "ListGroupsForMemberPaginator",
    "ListUsersPaginator",
    "SearchGroupsPaginator",
    "SearchUsersPaginator",
)

_ItemTypeDef = TypeVar("_ItemTypeDef")

class _PageIterator(Generic[_ItemTypeDef], PageIterator):
    def __iter__(self) -> Iterator[_ItemTypeDef]:
        """
        Proxy method to specify iterator item type.
        """

class ListGroupMembersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListGroupMembers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupmemberspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupMembersRequestListGroupMembersPaginateTypeDef]
    ) -> AsyncIterator[ListGroupMembersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListGroupMembers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupmemberspaginator)
        """

class ListGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsRequestListGroupsPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupspaginator)
        """

class ListGroupsForMemberPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListGroupsForMember)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupsformemberpaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListGroupsForMemberRequestListGroupsForMemberPaginateTypeDef]
    ) -> AsyncIterator[ListGroupsForMemberResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListGroupsForMember.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listgroupsformemberpaginator)
        """

class ListUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[ListUsersRequestListUsersPaginateTypeDef]
    ) -> AsyncIterator[ListUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.ListUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#listuserspaginator)
        """

class SearchGroupsPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.SearchGroups)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchgroupspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchGroupsRequestSearchGroupsPaginateTypeDef]
    ) -> AsyncIterator[SearchGroupsResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.SearchGroups.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchgroupspaginator)
        """

class SearchUsersPaginator(AioPaginator):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.SearchUsers)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchuserspaginator)
    """
    def paginate(
        self, **kwargs: Unpack[SearchUsersRequestSearchUsersPaginateTypeDef]
    ) -> AsyncIterator[SearchUsersResultTypeDef]:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/ds-data.html#DirectoryServiceData.Paginator.SearchUsers.paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_ds_data/paginators/#searchuserspaginator)
        """
