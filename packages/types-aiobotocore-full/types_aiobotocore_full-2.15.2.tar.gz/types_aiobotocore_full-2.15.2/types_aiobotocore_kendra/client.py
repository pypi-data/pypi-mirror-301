"""
Type annotations for kendra service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_kendra.client import KendraClient

    session = get_session()
    async with session.create_client("kendra") as client:
        client: KendraClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .type_defs import (
    AssociateEntitiesToExperienceRequestRequestTypeDef,
    AssociateEntitiesToExperienceResponseTypeDef,
    AssociatePersonasToEntitiesRequestRequestTypeDef,
    AssociatePersonasToEntitiesResponseTypeDef,
    BatchDeleteDocumentRequestRequestTypeDef,
    BatchDeleteDocumentResponseTypeDef,
    BatchDeleteFeaturedResultsSetRequestRequestTypeDef,
    BatchDeleteFeaturedResultsSetResponseTypeDef,
    BatchGetDocumentStatusRequestRequestTypeDef,
    BatchGetDocumentStatusResponseTypeDef,
    BatchPutDocumentRequestRequestTypeDef,
    BatchPutDocumentResponseTypeDef,
    ClearQuerySuggestionsRequestRequestTypeDef,
    CreateAccessControlConfigurationRequestRequestTypeDef,
    CreateAccessControlConfigurationResponseTypeDef,
    CreateDataSourceRequestRequestTypeDef,
    CreateDataSourceResponseTypeDef,
    CreateExperienceRequestRequestTypeDef,
    CreateExperienceResponseTypeDef,
    CreateFaqRequestRequestTypeDef,
    CreateFaqResponseTypeDef,
    CreateFeaturedResultsSetRequestRequestTypeDef,
    CreateFeaturedResultsSetResponseTypeDef,
    CreateIndexRequestRequestTypeDef,
    CreateIndexResponseTypeDef,
    CreateQuerySuggestionsBlockListRequestRequestTypeDef,
    CreateQuerySuggestionsBlockListResponseTypeDef,
    CreateThesaurusRequestRequestTypeDef,
    CreateThesaurusResponseTypeDef,
    DeleteAccessControlConfigurationRequestRequestTypeDef,
    DeleteDataSourceRequestRequestTypeDef,
    DeleteExperienceRequestRequestTypeDef,
    DeleteFaqRequestRequestTypeDef,
    DeleteIndexRequestRequestTypeDef,
    DeletePrincipalMappingRequestRequestTypeDef,
    DeleteQuerySuggestionsBlockListRequestRequestTypeDef,
    DeleteThesaurusRequestRequestTypeDef,
    DescribeAccessControlConfigurationRequestRequestTypeDef,
    DescribeAccessControlConfigurationResponseTypeDef,
    DescribeDataSourceRequestRequestTypeDef,
    DescribeDataSourceResponseTypeDef,
    DescribeExperienceRequestRequestTypeDef,
    DescribeExperienceResponseTypeDef,
    DescribeFaqRequestRequestTypeDef,
    DescribeFaqResponseTypeDef,
    DescribeFeaturedResultsSetRequestRequestTypeDef,
    DescribeFeaturedResultsSetResponseTypeDef,
    DescribeIndexRequestRequestTypeDef,
    DescribeIndexResponseTypeDef,
    DescribePrincipalMappingRequestRequestTypeDef,
    DescribePrincipalMappingResponseTypeDef,
    DescribeQuerySuggestionsBlockListRequestRequestTypeDef,
    DescribeQuerySuggestionsBlockListResponseTypeDef,
    DescribeQuerySuggestionsConfigRequestRequestTypeDef,
    DescribeQuerySuggestionsConfigResponseTypeDef,
    DescribeThesaurusRequestRequestTypeDef,
    DescribeThesaurusResponseTypeDef,
    DisassociateEntitiesFromExperienceRequestRequestTypeDef,
    DisassociateEntitiesFromExperienceResponseTypeDef,
    DisassociatePersonasFromEntitiesRequestRequestTypeDef,
    DisassociatePersonasFromEntitiesResponseTypeDef,
    EmptyResponseMetadataTypeDef,
    GetQuerySuggestionsRequestRequestTypeDef,
    GetQuerySuggestionsResponseTypeDef,
    GetSnapshotsRequestRequestTypeDef,
    GetSnapshotsResponseTypeDef,
    ListAccessControlConfigurationsRequestRequestTypeDef,
    ListAccessControlConfigurationsResponseTypeDef,
    ListDataSourcesRequestRequestTypeDef,
    ListDataSourcesResponseTypeDef,
    ListDataSourceSyncJobsRequestRequestTypeDef,
    ListDataSourceSyncJobsResponseTypeDef,
    ListEntityPersonasRequestRequestTypeDef,
    ListEntityPersonasResponseTypeDef,
    ListExperienceEntitiesRequestRequestTypeDef,
    ListExperienceEntitiesResponseTypeDef,
    ListExperiencesRequestRequestTypeDef,
    ListExperiencesResponseTypeDef,
    ListFaqsRequestRequestTypeDef,
    ListFaqsResponseTypeDef,
    ListFeaturedResultsSetsRequestRequestTypeDef,
    ListFeaturedResultsSetsResponseTypeDef,
    ListGroupsOlderThanOrderingIdRequestRequestTypeDef,
    ListGroupsOlderThanOrderingIdResponseTypeDef,
    ListIndicesRequestRequestTypeDef,
    ListIndicesResponseTypeDef,
    ListQuerySuggestionsBlockListsRequestRequestTypeDef,
    ListQuerySuggestionsBlockListsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    ListThesauriRequestRequestTypeDef,
    ListThesauriResponseTypeDef,
    PutPrincipalMappingRequestRequestTypeDef,
    QueryRequestRequestTypeDef,
    QueryResultTypeDef,
    RetrieveRequestRequestTypeDef,
    RetrieveResultTypeDef,
    StartDataSourceSyncJobRequestRequestTypeDef,
    StartDataSourceSyncJobResponseTypeDef,
    StopDataSourceSyncJobRequestRequestTypeDef,
    SubmitFeedbackRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateAccessControlConfigurationRequestRequestTypeDef,
    UpdateDataSourceRequestRequestTypeDef,
    UpdateExperienceRequestRequestTypeDef,
    UpdateFeaturedResultsSetRequestRequestTypeDef,
    UpdateFeaturedResultsSetResponseTypeDef,
    UpdateIndexRequestRequestTypeDef,
    UpdateQuerySuggestionsBlockListRequestRequestTypeDef,
    UpdateQuerySuggestionsConfigRequestRequestTypeDef,
    UpdateThesaurusRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = ("KendraClient",)


class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str


class Exceptions:
    AccessDeniedException: Type[BotocoreClientError]
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    FeaturedResultsConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    InvalidRequestException: Type[BotocoreClientError]
    ResourceAlreadyExistException: Type[BotocoreClientError]
    ResourceInUseException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ResourceUnavailableException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]


class KendraClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        KendraClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.exceptions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#exceptions)
        """

    async def associate_entities_to_experience(
        self, **kwargs: Unpack[AssociateEntitiesToExperienceRequestRequestTypeDef]
    ) -> AssociateEntitiesToExperienceResponseTypeDef:
        """
        Grants users or groups in your IAM Identity Center identity source access to
        your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.associate_entities_to_experience)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#associate_entities_to_experience)
        """

    async def associate_personas_to_entities(
        self, **kwargs: Unpack[AssociatePersonasToEntitiesRequestRequestTypeDef]
    ) -> AssociatePersonasToEntitiesResponseTypeDef:
        """
        Defines the specific permissions of users or groups in your IAM Identity Center
        identity source with access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.associate_personas_to_entities)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#associate_personas_to_entities)
        """

    async def batch_delete_document(
        self, **kwargs: Unpack[BatchDeleteDocumentRequestRequestTypeDef]
    ) -> BatchDeleteDocumentResponseTypeDef:
        """
        Removes one or more documents from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_delete_document)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_delete_document)
        """

    async def batch_delete_featured_results_set(
        self, **kwargs: Unpack[BatchDeleteFeaturedResultsSetRequestRequestTypeDef]
    ) -> BatchDeleteFeaturedResultsSetResponseTypeDef:
        """
        Removes one or more sets of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_delete_featured_results_set)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_delete_featured_results_set)
        """

    async def batch_get_document_status(
        self, **kwargs: Unpack[BatchGetDocumentStatusRequestRequestTypeDef]
    ) -> BatchGetDocumentStatusResponseTypeDef:
        """
        Returns the indexing status for one or more documents submitted with the
        [BatchPutDocument](https://docs.aws.amazon.com/kendra/latest/dg/API_BatchPutDocument.html)
        API.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_get_document_status)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_get_document_status)
        """

    async def batch_put_document(
        self, **kwargs: Unpack[BatchPutDocumentRequestRequestTypeDef]
    ) -> BatchPutDocumentResponseTypeDef:
        """
        Adds one or more documents to an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.batch_put_document)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#batch_put_document)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.can_paginate)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#can_paginate)
        """

    async def clear_query_suggestions(
        self, **kwargs: Unpack[ClearQuerySuggestionsRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Clears existing query suggestions from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.clear_query_suggestions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#clear_query_suggestions)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.close)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#close)
        """

    async def create_access_control_configuration(
        self, **kwargs: Unpack[CreateAccessControlConfigurationRequestRequestTypeDef]
    ) -> CreateAccessControlConfigurationResponseTypeDef:
        """
        Creates an access configuration for your documents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_access_control_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_access_control_configuration)
        """

    async def create_data_source(
        self, **kwargs: Unpack[CreateDataSourceRequestRequestTypeDef]
    ) -> CreateDataSourceResponseTypeDef:
        """
        Creates a data source connector that you want to use with an Amazon Kendra
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_data_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_data_source)
        """

    async def create_experience(
        self, **kwargs: Unpack[CreateExperienceRequestRequestTypeDef]
    ) -> CreateExperienceResponseTypeDef:
        """
        Creates an Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_experience)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_experience)
        """

    async def create_faq(
        self, **kwargs: Unpack[CreateFaqRequestRequestTypeDef]
    ) -> CreateFaqResponseTypeDef:
        """
        Creates a set of frequently ask questions (FAQs) using a specified FAQ file
        stored in an Amazon S3
        bucket.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_faq)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_faq)
        """

    async def create_featured_results_set(
        self, **kwargs: Unpack[CreateFeaturedResultsSetRequestRequestTypeDef]
    ) -> CreateFeaturedResultsSetResponseTypeDef:
        """
        Creates a set of featured results to display at the top of the search results
        page.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_featured_results_set)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_featured_results_set)
        """

    async def create_index(
        self, **kwargs: Unpack[CreateIndexRequestRequestTypeDef]
    ) -> CreateIndexResponseTypeDef:
        """
        Creates an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_index)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_index)
        """

    async def create_query_suggestions_block_list(
        self, **kwargs: Unpack[CreateQuerySuggestionsBlockListRequestRequestTypeDef]
    ) -> CreateQuerySuggestionsBlockListResponseTypeDef:
        """
        Creates a block list to exlcude certain queries from suggestions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_query_suggestions_block_list)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_query_suggestions_block_list)
        """

    async def create_thesaurus(
        self, **kwargs: Unpack[CreateThesaurusRequestRequestTypeDef]
    ) -> CreateThesaurusResponseTypeDef:
        """
        Creates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.create_thesaurus)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#create_thesaurus)
        """

    async def delete_access_control_configuration(
        self, **kwargs: Unpack[DeleteAccessControlConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes an access control configuration that you created for your documents in
        an
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_access_control_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_access_control_configuration)
        """

    async def delete_data_source(
        self, **kwargs: Unpack[DeleteDataSourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_data_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_data_source)
        """

    async def delete_experience(
        self, **kwargs: Unpack[DeleteExperienceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_experience)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_experience)
        """

    async def delete_faq(
        self, **kwargs: Unpack[DeleteFaqRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Removes an FAQ from an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_faq)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_faq)
        """

    async def delete_index(
        self, **kwargs: Unpack[DeleteIndexRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_index)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_index)
        """

    async def delete_principal_mapping(
        self, **kwargs: Unpack[DeletePrincipalMappingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a group so that all users and sub groups that belong to the group can
        no longer access documents only available to that
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_principal_mapping)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_principal_mapping)
        """

    async def delete_query_suggestions_block_list(
        self, **kwargs: Unpack[DeleteQuerySuggestionsBlockListRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_query_suggestions_block_list)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_query_suggestions_block_list)
        """

    async def delete_thesaurus(
        self, **kwargs: Unpack[DeleteThesaurusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Deletes an Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.delete_thesaurus)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#delete_thesaurus)
        """

    async def describe_access_control_configuration(
        self, **kwargs: Unpack[DescribeAccessControlConfigurationRequestRequestTypeDef]
    ) -> DescribeAccessControlConfigurationResponseTypeDef:
        """
        Gets information about an access control configuration that you created for
        your documents in an
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_access_control_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_access_control_configuration)
        """

    async def describe_data_source(
        self, **kwargs: Unpack[DescribeDataSourceRequestRequestTypeDef]
    ) -> DescribeDataSourceResponseTypeDef:
        """
        Gets information about an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_data_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_data_source)
        """

    async def describe_experience(
        self, **kwargs: Unpack[DescribeExperienceRequestRequestTypeDef]
    ) -> DescribeExperienceResponseTypeDef:
        """
        Gets information about your Amazon Kendra experience such as a search
        application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_experience)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_experience)
        """

    async def describe_faq(
        self, **kwargs: Unpack[DescribeFaqRequestRequestTypeDef]
    ) -> DescribeFaqResponseTypeDef:
        """
        Gets information about an FAQ list.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_faq)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_faq)
        """

    async def describe_featured_results_set(
        self, **kwargs: Unpack[DescribeFeaturedResultsSetRequestRequestTypeDef]
    ) -> DescribeFeaturedResultsSetResponseTypeDef:
        """
        Gets information about a set of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_featured_results_set)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_featured_results_set)
        """

    async def describe_index(
        self, **kwargs: Unpack[DescribeIndexRequestRequestTypeDef]
    ) -> DescribeIndexResponseTypeDef:
        """
        Gets information about an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_index)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_index)
        """

    async def describe_principal_mapping(
        self, **kwargs: Unpack[DescribePrincipalMappingRequestRequestTypeDef]
    ) -> DescribePrincipalMappingResponseTypeDef:
        """
        Describes the processing of `PUT` and `DELETE` actions for mapping users to
        their
        groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_principal_mapping)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_principal_mapping)
        """

    async def describe_query_suggestions_block_list(
        self, **kwargs: Unpack[DescribeQuerySuggestionsBlockListRequestRequestTypeDef]
    ) -> DescribeQuerySuggestionsBlockListResponseTypeDef:
        """
        Gets information about a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_query_suggestions_block_list)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_query_suggestions_block_list)
        """

    async def describe_query_suggestions_config(
        self, **kwargs: Unpack[DescribeQuerySuggestionsConfigRequestRequestTypeDef]
    ) -> DescribeQuerySuggestionsConfigResponseTypeDef:
        """
        Gets information on the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_query_suggestions_config)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_query_suggestions_config)
        """

    async def describe_thesaurus(
        self, **kwargs: Unpack[DescribeThesaurusRequestRequestTypeDef]
    ) -> DescribeThesaurusResponseTypeDef:
        """
        Gets information about an Amazon Kendra thesaurus.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.describe_thesaurus)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#describe_thesaurus)
        """

    async def disassociate_entities_from_experience(
        self, **kwargs: Unpack[DisassociateEntitiesFromExperienceRequestRequestTypeDef]
    ) -> DisassociateEntitiesFromExperienceResponseTypeDef:
        """
        Prevents users or groups in your IAM Identity Center identity source from
        accessing your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.disassociate_entities_from_experience)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#disassociate_entities_from_experience)
        """

    async def disassociate_personas_from_entities(
        self, **kwargs: Unpack[DisassociatePersonasFromEntitiesRequestRequestTypeDef]
    ) -> DisassociatePersonasFromEntitiesResponseTypeDef:
        """
        Removes the specific permissions of users or groups in your IAM Identity Center
        identity source with access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.disassociate_personas_from_entities)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#disassociate_personas_from_entities)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.generate_presigned_url)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#generate_presigned_url)
        """

    async def get_query_suggestions(
        self, **kwargs: Unpack[GetQuerySuggestionsRequestRequestTypeDef]
    ) -> GetQuerySuggestionsResponseTypeDef:
        """
        Fetches the queries that are suggested to your users.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.get_query_suggestions)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#get_query_suggestions)
        """

    async def get_snapshots(
        self, **kwargs: Unpack[GetSnapshotsRequestRequestTypeDef]
    ) -> GetSnapshotsResponseTypeDef:
        """
        Retrieves search metrics data.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.get_snapshots)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#get_snapshots)
        """

    async def list_access_control_configurations(
        self, **kwargs: Unpack[ListAccessControlConfigurationsRequestRequestTypeDef]
    ) -> ListAccessControlConfigurationsResponseTypeDef:
        """
        Lists one or more access control configurations for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_access_control_configurations)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_access_control_configurations)
        """

    async def list_data_source_sync_jobs(
        self, **kwargs: Unpack[ListDataSourceSyncJobsRequestRequestTypeDef]
    ) -> ListDataSourceSyncJobsResponseTypeDef:
        """
        Gets statistics about synchronizing a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_data_source_sync_jobs)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_data_source_sync_jobs)
        """

    async def list_data_sources(
        self, **kwargs: Unpack[ListDataSourcesRequestRequestTypeDef]
    ) -> ListDataSourcesResponseTypeDef:
        """
        Lists the data source connectors that you have created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_data_sources)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_data_sources)
        """

    async def list_entity_personas(
        self, **kwargs: Unpack[ListEntityPersonasRequestRequestTypeDef]
    ) -> ListEntityPersonasResponseTypeDef:
        """
        Lists specific permissions of users and groups with access to your Amazon
        Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_entity_personas)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_entity_personas)
        """

    async def list_experience_entities(
        self, **kwargs: Unpack[ListExperienceEntitiesRequestRequestTypeDef]
    ) -> ListExperienceEntitiesResponseTypeDef:
        """
        Lists users or groups in your IAM Identity Center identity source that are
        granted access to your Amazon Kendra
        experience.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_experience_entities)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_experience_entities)
        """

    async def list_experiences(
        self, **kwargs: Unpack[ListExperiencesRequestRequestTypeDef]
    ) -> ListExperiencesResponseTypeDef:
        """
        Lists one or more Amazon Kendra experiences.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_experiences)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_experiences)
        """

    async def list_faqs(
        self, **kwargs: Unpack[ListFaqsRequestRequestTypeDef]
    ) -> ListFaqsResponseTypeDef:
        """
        Gets a list of FAQ lists associated with an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_faqs)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_faqs)
        """

    async def list_featured_results_sets(
        self, **kwargs: Unpack[ListFeaturedResultsSetsRequestRequestTypeDef]
    ) -> ListFeaturedResultsSetsResponseTypeDef:
        """
        Lists all your sets of featured results for a given index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_featured_results_sets)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_featured_results_sets)
        """

    async def list_groups_older_than_ordering_id(
        self, **kwargs: Unpack[ListGroupsOlderThanOrderingIdRequestRequestTypeDef]
    ) -> ListGroupsOlderThanOrderingIdResponseTypeDef:
        """
        Provides a list of groups that are mapped to users before a given ordering or
        timestamp
        identifier.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_groups_older_than_ordering_id)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_groups_older_than_ordering_id)
        """

    async def list_indices(
        self, **kwargs: Unpack[ListIndicesRequestRequestTypeDef]
    ) -> ListIndicesResponseTypeDef:
        """
        Lists the Amazon Kendra indexes that you created.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_indices)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_indices)
        """

    async def list_query_suggestions_block_lists(
        self, **kwargs: Unpack[ListQuerySuggestionsBlockListsRequestRequestTypeDef]
    ) -> ListQuerySuggestionsBlockListsResponseTypeDef:
        """
        Lists the block lists used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_query_suggestions_block_lists)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_query_suggestions_block_lists)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Gets a list of tags associated with a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_tags_for_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_tags_for_resource)
        """

    async def list_thesauri(
        self, **kwargs: Unpack[ListThesauriRequestRequestTypeDef]
    ) -> ListThesauriResponseTypeDef:
        """
        Lists the thesauri for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.list_thesauri)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#list_thesauri)
        """

    async def put_principal_mapping(
        self, **kwargs: Unpack[PutPrincipalMappingRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Maps users to their groups so that you only need to provide the user ID when
        you issue the
        query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.put_principal_mapping)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#put_principal_mapping)
        """

    async def query(self, **kwargs: Unpack[QueryRequestRequestTypeDef]) -> QueryResultTypeDef:
        """
        Searches an index given an input query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.query)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#query)
        """

    async def retrieve(
        self, **kwargs: Unpack[RetrieveRequestRequestTypeDef]
    ) -> RetrieveResultTypeDef:
        """
        Retrieves relevant passages or text excerpts given an input query.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.retrieve)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#retrieve)
        """

    async def start_data_source_sync_job(
        self, **kwargs: Unpack[StartDataSourceSyncJobRequestRequestTypeDef]
    ) -> StartDataSourceSyncJobResponseTypeDef:
        """
        Starts a synchronization job for a data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.start_data_source_sync_job)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#start_data_source_sync_job)
        """

    async def stop_data_source_sync_job(
        self, **kwargs: Unpack[StopDataSourceSyncJobRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Stops a synchronization job that is currently running.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.stop_data_source_sync_job)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#stop_data_source_sync_job)
        """

    async def submit_feedback(
        self, **kwargs: Unpack[SubmitFeedbackRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Enables you to provide feedback to Amazon Kendra to improve the performance of
        your
        index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.submit_feedback)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#submit_feedback)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds the specified tag to the specified index, FAQ, or data source resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.tag_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a tag from an index, FAQ, or a data source.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.untag_resource)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#untag_resource)
        """

    async def update_access_control_configuration(
        self, **kwargs: Unpack[UpdateAccessControlConfigurationRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates an access control configuration for your documents in an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_access_control_configuration)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_access_control_configuration)
        """

    async def update_data_source(
        self, **kwargs: Unpack[UpdateDataSourceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon Kendra data source connector.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_data_source)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_data_source)
        """

    async def update_experience(
        self, **kwargs: Unpack[UpdateExperienceRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates your Amazon Kendra experience such as a search application.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_experience)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_experience)
        """

    async def update_featured_results_set(
        self, **kwargs: Unpack[UpdateFeaturedResultsSetRequestRequestTypeDef]
    ) -> UpdateFeaturedResultsSetResponseTypeDef:
        """
        Updates a set of featured results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_featured_results_set)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_featured_results_set)
        """

    async def update_index(
        self, **kwargs: Unpack[UpdateIndexRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates an Amazon Kendra index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_index)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_index)
        """

    async def update_query_suggestions_block_list(
        self, **kwargs: Unpack[UpdateQuerySuggestionsBlockListRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a block list used for query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_query_suggestions_block_list)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_query_suggestions_block_list)
        """

    async def update_query_suggestions_config(
        self, **kwargs: Unpack[UpdateQuerySuggestionsConfigRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates the settings of query suggestions for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_query_suggestions_config)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_query_suggestions_config)
        """

    async def update_thesaurus(
        self, **kwargs: Unpack[UpdateThesaurusRequestRequestTypeDef]
    ) -> EmptyResponseMetadataTypeDef:
        """
        Updates a thesaurus for an index.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client.update_thesaurus)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/#update_thesaurus)
        """

    async def __aenter__(self) -> "KendraClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/kendra.html#Kendra.Client)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_kendra/client/)
        """
