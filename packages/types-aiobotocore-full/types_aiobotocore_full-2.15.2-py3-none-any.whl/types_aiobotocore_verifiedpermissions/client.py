"""
Type annotations for verifiedpermissions service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_verifiedpermissions.client import VerifiedPermissionsClient

    session = get_session()
    async with session.create_client("verifiedpermissions") as client:
        client: VerifiedPermissionsClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import (
    ListIdentitySourcesPaginator,
    ListPoliciesPaginator,
    ListPolicyStoresPaginator,
    ListPolicyTemplatesPaginator,
)
from .type_defs import (
    BatchIsAuthorizedInputRequestTypeDef,
    BatchIsAuthorizedOutputTypeDef,
    BatchIsAuthorizedWithTokenInputRequestTypeDef,
    BatchIsAuthorizedWithTokenOutputTypeDef,
    CreateIdentitySourceInputRequestTypeDef,
    CreateIdentitySourceOutputTypeDef,
    CreatePolicyInputRequestTypeDef,
    CreatePolicyOutputTypeDef,
    CreatePolicyStoreInputRequestTypeDef,
    CreatePolicyStoreOutputTypeDef,
    CreatePolicyTemplateInputRequestTypeDef,
    CreatePolicyTemplateOutputTypeDef,
    DeleteIdentitySourceInputRequestTypeDef,
    DeletePolicyInputRequestTypeDef,
    DeletePolicyStoreInputRequestTypeDef,
    DeletePolicyTemplateInputRequestTypeDef,
    GetIdentitySourceInputRequestTypeDef,
    GetIdentitySourceOutputTypeDef,
    GetPolicyInputRequestTypeDef,
    GetPolicyOutputTypeDef,
    GetPolicyStoreInputRequestTypeDef,
    GetPolicyStoreOutputTypeDef,
    GetPolicyTemplateInputRequestTypeDef,
    GetPolicyTemplateOutputTypeDef,
    GetSchemaInputRequestTypeDef,
    GetSchemaOutputTypeDef,
    IsAuthorizedInputRequestTypeDef,
    IsAuthorizedOutputTypeDef,
    IsAuthorizedWithTokenInputRequestTypeDef,
    IsAuthorizedWithTokenOutputTypeDef,
    ListIdentitySourcesInputRequestTypeDef,
    ListIdentitySourcesOutputTypeDef,
    ListPoliciesInputRequestTypeDef,
    ListPoliciesOutputTypeDef,
    ListPolicyStoresInputRequestTypeDef,
    ListPolicyStoresOutputTypeDef,
    ListPolicyTemplatesInputRequestTypeDef,
    ListPolicyTemplatesOutputTypeDef,
    PutSchemaInputRequestTypeDef,
    PutSchemaOutputTypeDef,
    UpdateIdentitySourceInputRequestTypeDef,
    UpdateIdentitySourceOutputTypeDef,
    UpdatePolicyInputRequestTypeDef,
    UpdatePolicyOutputTypeDef,
    UpdatePolicyStoreInputRequestTypeDef,
    UpdatePolicyStoreOutputTypeDef,
    UpdatePolicyTemplateInputRequestTypeDef,
    UpdatePolicyTemplateOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack


__all__ = ("VerifiedPermissionsClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class VerifiedPermissionsClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        VerifiedPermissionsClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.exceptions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#exceptions)
        """

    async def batch_is_authorized(
        self, **kwargs: Unpack[BatchIsAuthorizedInputRequestTypeDef]
    ) -> BatchIsAuthorizedOutputTypeDef:
        """
        Makes a series of decisions about multiple authorization requests for one
        principal or
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.batch_is_authorized)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#batch_is_authorized)
        """

    async def batch_is_authorized_with_token(
        self, **kwargs: Unpack[BatchIsAuthorizedWithTokenInputRequestTypeDef]
    ) -> BatchIsAuthorizedWithTokenOutputTypeDef:
        """
        Makes a series of decisions about multiple authorization requests for one token.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.batch_is_authorized_with_token)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#batch_is_authorized_with_token)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.can_paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.close)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#close)
        """

    async def create_identity_source(
        self, **kwargs: Unpack[CreateIdentitySourceInputRequestTypeDef]
    ) -> CreateIdentitySourceOutputTypeDef:
        """
        Adds an identity source to a policy store-an Amazon Cognito user pool or OpenID
        Connect (OIDC) identity provider
        (IdP).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.create_identity_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#create_identity_source)
        """

    async def create_policy(
        self, **kwargs: Unpack[CreatePolicyInputRequestTypeDef]
    ) -> CreatePolicyOutputTypeDef:
        """
        Creates a Cedar policy and saves it in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.create_policy)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#create_policy)
        """

    async def create_policy_store(
        self, **kwargs: Unpack[CreatePolicyStoreInputRequestTypeDef]
    ) -> CreatePolicyStoreOutputTypeDef:
        """
        Creates a policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.create_policy_store)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#create_policy_store)
        """

    async def create_policy_template(
        self, **kwargs: Unpack[CreatePolicyTemplateInputRequestTypeDef]
    ) -> CreatePolicyTemplateOutputTypeDef:
        """
        Creates a policy template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.create_policy_template)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#create_policy_template)
        """

    async def delete_identity_source(
        self, **kwargs: Unpack[DeleteIdentitySourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an identity source that references an identity provider (IdP) such as
        Amazon
        Cognito.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.delete_identity_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#delete_identity_source)
        """

    async def delete_policy(
        self, **kwargs: Unpack[DeletePolicyInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy from the policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.delete_policy)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#delete_policy)
        """

    async def delete_policy_store(
        self, **kwargs: Unpack[DeletePolicyStoreInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.delete_policy_store)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#delete_policy_store)
        """

    async def delete_policy_template(
        self, **kwargs: Unpack[DeletePolicyTemplateInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified policy template from the policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.delete_policy_template)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#delete_policy_template)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.generate_presigned_url)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#generate_presigned_url)
        """

    async def get_identity_source(
        self, **kwargs: Unpack[GetIdentitySourceInputRequestTypeDef]
    ) -> GetIdentitySourceOutputTypeDef:
        """
        Retrieves the details about the specified identity source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_identity_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_identity_source)
        """

    async def get_policy(
        self, **kwargs: Unpack[GetPolicyInputRequestTypeDef]
    ) -> GetPolicyOutputTypeDef:
        """
        Retrieves information about the specified policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_policy)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_policy)
        """

    async def get_policy_store(
        self, **kwargs: Unpack[GetPolicyStoreInputRequestTypeDef]
    ) -> GetPolicyStoreOutputTypeDef:
        """
        Retrieves details about a policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_policy_store)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_policy_store)
        """

    async def get_policy_template(
        self, **kwargs: Unpack[GetPolicyTemplateInputRequestTypeDef]
    ) -> GetPolicyTemplateOutputTypeDef:
        """
        Retrieve the details for the specified policy template in the specified policy
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_policy_template)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_policy_template)
        """

    async def get_schema(
        self, **kwargs: Unpack[GetSchemaInputRequestTypeDef]
    ) -> GetSchemaOutputTypeDef:
        """
        Retrieve the details for the specified schema in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_schema)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_schema)
        """

    async def is_authorized(
        self, **kwargs: Unpack[IsAuthorizedInputRequestTypeDef]
    ) -> IsAuthorizedOutputTypeDef:
        """
        Makes an authorization decision about a service request described in the
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.is_authorized)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#is_authorized)
        """

    async def is_authorized_with_token(
        self, **kwargs: Unpack[IsAuthorizedWithTokenInputRequestTypeDef]
    ) -> IsAuthorizedWithTokenOutputTypeDef:
        """
        Makes an authorization decision about a service request described in the
        parameters.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.is_authorized_with_token)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#is_authorized_with_token)
        """

    async def list_identity_sources(
        self, **kwargs: Unpack[ListIdentitySourcesInputRequestTypeDef]
    ) -> ListIdentitySourcesOutputTypeDef:
        """
        Returns a paginated list of all of the identity sources defined in the
        specified policy
        store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.list_identity_sources)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#list_identity_sources)
        """

    async def list_policies(
        self, **kwargs: Unpack[ListPoliciesInputRequestTypeDef]
    ) -> ListPoliciesOutputTypeDef:
        """
        Returns a paginated list of all policies stored in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.list_policies)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#list_policies)
        """

    async def list_policy_stores(
        self, **kwargs: Unpack[ListPolicyStoresInputRequestTypeDef]
    ) -> ListPolicyStoresOutputTypeDef:
        """
        Returns a paginated list of all policy stores in the calling Amazon Web
        Services
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.list_policy_stores)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#list_policy_stores)
        """

    async def list_policy_templates(
        self, **kwargs: Unpack[ListPolicyTemplatesInputRequestTypeDef]
    ) -> ListPolicyTemplatesOutputTypeDef:
        """
        Returns a paginated list of all policy templates in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.list_policy_templates)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#list_policy_templates)
        """

    async def put_schema(
        self, **kwargs: Unpack[PutSchemaInputRequestTypeDef]
    ) -> PutSchemaOutputTypeDef:
        """
        Creates or updates the policy schema in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.put_schema)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#put_schema)
        """

    async def update_identity_source(
        self, **kwargs: Unpack[UpdateIdentitySourceInputRequestTypeDef]
    ) -> UpdateIdentitySourceOutputTypeDef:
        """
        Updates the specified identity source to use a new identity provider (IdP), or
        to change the mapping of identities from the IdP to a different principal
        entity
        type.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.update_identity_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#update_identity_source)
        """

    async def update_policy(
        self, **kwargs: Unpack[UpdatePolicyInputRequestTypeDef]
    ) -> UpdatePolicyOutputTypeDef:
        """
        Modifies a Cedar static policy in the specified policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.update_policy)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#update_policy)
        """

    async def update_policy_store(
        self, **kwargs: Unpack[UpdatePolicyStoreInputRequestTypeDef]
    ) -> UpdatePolicyStoreOutputTypeDef:
        """
        Modifies the validation setting for a policy store.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.update_policy_store)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#update_policy_store)
        """

    async def update_policy_template(
        self, **kwargs: Unpack[UpdatePolicyTemplateInputRequestTypeDef]
    ) -> UpdatePolicyTemplateOutputTypeDef:
        """
        Updates the specified policy template.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.update_policy_template)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#update_policy_template)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_identity_sources"]
    ) -> ListIdentitySourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_paginator)
        """

    @overload
    def get_paginator(self, operation_name: Literal["list_policies"]) -> ListPoliciesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_stores"]
    ) -> ListPolicyStoresPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["list_policy_templates"]
    ) -> ListPolicyTemplatesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client.get_paginator)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/#get_paginator)
        """

    async def __aenter__(self) -> "VerifiedPermissionsClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/verifiedpermissions.html#VerifiedPermissions.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_verifiedpermissions/client/)
        """
