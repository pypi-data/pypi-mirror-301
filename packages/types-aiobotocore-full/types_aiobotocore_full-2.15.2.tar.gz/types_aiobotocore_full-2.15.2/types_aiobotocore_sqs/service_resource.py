"""
Type annotations for sqs service ServiceResource

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sqs.service_resource import SQSServiceResource
    import types_aiobotocore_sqs.service_resource as sqs_resources

    session = get_session()
    async with session.resource("sqs") as resource:
        resource: SQSServiceResource

        my_message: sqs_resources.Message = resource.Message(...)
        my_queue: sqs_resources.Queue = resource.Queue(...)
```
"""

import sys
from typing import AsyncIterator, Awaitable, Dict, List, NoReturn, Sequence

from .client import SQSClient
from .literals import MessageSystemAttributeNameType, QueueAttributeNameType
from .type_defs import (
    AddPermissionRequestQueueAddPermissionTypeDef,
    ChangeMessageVisibilityBatchRequestQueueChangeMessageVisibilityBatchTypeDef,
    ChangeMessageVisibilityBatchResultTypeDef,
    ChangeMessageVisibilityRequestMessageChangeVisibilityTypeDef,
    CreateQueueRequestServiceResourceCreateQueueTypeDef,
    DeleteMessageBatchRequestQueueDeleteMessagesTypeDef,
    DeleteMessageBatchResultTypeDef,
    GetQueueUrlRequestServiceResourceGetQueueByNameTypeDef,
    MessageAttributeValueOutputTypeDef,
    ReceiveMessageRequestQueueReceiveMessagesTypeDef,
    RemovePermissionRequestQueueRemovePermissionTypeDef,
    SendMessageBatchRequestQueueSendMessagesTypeDef,
    SendMessageBatchResultTypeDef,
    SendMessageRequestQueueSendMessageTypeDef,
    SendMessageResultTypeDef,
    SetQueueAttributesRequestQueueSetAttributesTypeDef,
)

try:
    from aioboto3.resources.base import AIOBoto3ServiceResource
except ImportError:
    from builtins import object as AIOBoto3ServiceResource
try:
    from aioboto3.resources.collection import AIOResourceCollection
except ImportError:
    from builtins import object as AIOResourceCollection
try:
    from boto3.resources.base import ResourceMeta
except ImportError:
    from builtins import object as ResourceMeta
if sys.version_info >= (3, 12):
    from typing import Unpack
else:
    from typing_extensions import Unpack


__all__ = (
    "SQSServiceResource",
    "Message",
    "Queue",
    "ServiceResourceQueuesCollection",
    "QueueDeadLetterSourceQueuesCollection",
)


class ServiceResourceQueuesCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
    """

    def all(self) -> "ServiceResourceQueuesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

    def filter(  # type: ignore
        self, *, QueueNamePrefix: str = ..., NextToken: str = ..., MaxResults: int = ...
    ) -> "ServiceResourceQueuesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

    def limit(self, count: int) -> "ServiceResourceQueuesCollection":
        """
        Return at most this many Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

    def page_size(self, count: int) -> "ServiceResourceQueuesCollection":
        """
        Fetch at most this many Queues per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

    def pages(self) -> AsyncIterator[List["Queue"]]:
        """
        A generator which yields pages of Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """

    def __aiter__(self) -> AsyncIterator["Queue"]:
        """
        A generator which yields Queues.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.queues)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#serviceresourcequeuescollection)
        """


class QueueDeadLetterSourceQueuesCollection(AIOResourceCollection):
    def all(self) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ..., MaxResults: int = ...
    ) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Return at most this many Queues.
        """

    def page_size(self, count: int) -> "QueueDeadLetterSourceQueuesCollection":
        """
        Fetch at most this many Queues per service request.
        """

    def pages(self) -> AsyncIterator[List["Queue"]]:
        """
        A generator which yields pages of Queues.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Queues.
        """

    def __aiter__(self) -> AsyncIterator["Queue"]:
        """
        A generator which yields Queues.
        """


class Message(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Message)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#message)
    """

    message_id: Awaitable[str]
    md5_of_body: Awaitable[str]
    body: Awaitable[str]
    attributes: Awaitable[Dict[MessageSystemAttributeNameType, str]]
    md5_of_message_attributes: Awaitable[str]
    message_attributes: Awaitable[Dict[str, MessageAttributeValueOutputTypeDef]]
    queue_url: str
    receipt_handle: str
    meta: "SQSResourceMeta"  # type: ignore

    async def Queue(self) -> "_Queue":
        """
        Creates a Queue resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.Queue)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messagequeue-method)
        """

    async def change_visibility(
        self, **kwargs: Unpack[ChangeMessageVisibilityRequestMessageChangeVisibilityTypeDef]
    ) -> None:
        """
        Changes the visibility timeout of a specified message in a queue to a new value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.change_visibility)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messagechange_visibility-method)
        """

    async def delete(self) -> None:
        """
        Deletes the specified message from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.delete)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messagedelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Message.get_available_subresources)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#messageget_available_subresources-method)
        """


_Message = Message


class Queue(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Queue)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queue)
    """

    attributes: Awaitable[Dict[QueueAttributeNameType, str]]
    url: str
    dead_letter_source_queues: QueueDeadLetterSourceQueuesCollection
    meta: "SQSResourceMeta"  # type: ignore

    async def Message(self, receipt_handle: str) -> "_Message":
        """
        Creates a Message resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.Message)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuemessage-method)
        """

    async def add_permission(
        self, **kwargs: Unpack[AddPermissionRequestQueueAddPermissionTypeDef]
    ) -> None:
        """
        Adds a permission to a queue for a specific
        [principal](https://docs.aws.amazon.com/general/latest/gr/glos-chap.html#P).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.add_permission)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueadd_permission-method)
        """

    async def change_message_visibility_batch(
        self,
        **kwargs: Unpack[
            ChangeMessageVisibilityBatchRequestQueueChangeMessageVisibilityBatchTypeDef
        ],
    ) -> ChangeMessageVisibilityBatchResultTypeDef:
        """
        Changes the visibility timeout of multiple messages.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.change_message_visibility_batch)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuechange_message_visibility_batch-method)
        """

    async def delete(self) -> None:
        """
        Deletes the queue specified by the `QueueUrl`, regardless of the queue's
        contents.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.delete)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuedelete-method)
        """

    async def delete_messages(
        self, **kwargs: Unpack[DeleteMessageBatchRequestQueueDeleteMessagesTypeDef]
    ) -> DeleteMessageBatchResultTypeDef:
        """
        Deletes up to ten messages from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.delete_messages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuedelete_messages-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.get_available_subresources)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`SQS.Client.get_queue_attributes` to update the attributes of
        the Queue
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.load)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueload-method)
        """

    async def purge(self) -> None:
        """
        Deletes available messages in a queue (including in-flight messages) specified
        by the `QueueURL`
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.purge)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuepurge-method)
        """

    async def receive_messages(
        self, **kwargs: Unpack[ReceiveMessageRequestQueueReceiveMessagesTypeDef]
    ) -> List["_Message"]:
        """
        Retrieves one or more messages (up to 10), from the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.receive_messages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuereceive_messages-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`SQS.Client.get_queue_attributes` to update the attributes of
        the Queue
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.reload)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuereload-method)
        """

    async def remove_permission(
        self, **kwargs: Unpack[RemovePermissionRequestQueueRemovePermissionTypeDef]
    ) -> None:
        """
        Revokes any permissions in the queue policy that matches the specified `Label`
        parameter.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.remove_permission)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueremove_permission-method)
        """

    async def send_message(
        self, **kwargs: Unpack[SendMessageRequestQueueSendMessageTypeDef]
    ) -> SendMessageResultTypeDef:
        """
        Delivers a message to the specified queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_message)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuesend_message-method)
        """

    async def send_messages(
        self, **kwargs: Unpack[SendMessageBatchRequestQueueSendMessagesTypeDef]
    ) -> SendMessageBatchResultTypeDef:
        """
        You can use `SendMessageBatch` to send up to 10 messages to the specified queue
        by assigning either identical or different values to each message (or by not
        assigning values at
        all).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.send_messages)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queuesend_messages-method)
        """

    async def set_attributes(
        self, **kwargs: Unpack[SetQueueAttributesRequestQueueSetAttributesTypeDef]
    ) -> None:
        """
        Sets the value of one or more queue attributes, like a policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.Queue.set_attributes)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#queueset_attributes-method)
        """


_Queue = Queue


class SQSResourceMeta(ResourceMeta):
    client: SQSClient


class SQSServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource)
    [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/)
    """

    meta: "SQSResourceMeta"  # type: ignore
    queues: ServiceResourceQueuesCollection

    async def Message(self, queue_url: str, receipt_handle: str) -> "_Message":
        """
        Creates a Message resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Message)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourcemessage-method)
        """

    async def Queue(self, url: str) -> "_Queue":
        """
        Creates a Queue resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.Queue)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourcequeue-method)
        """

    async def create_queue(
        self, **kwargs: Unpack[CreateQueueRequestServiceResourceCreateQueueTypeDef]
    ) -> "_Queue":
        """
        Creates a new standard or FIFO queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.create_queue)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourcecreate_queue-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.get_available_subresources)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourceget_available_subresources-method)
        """

    async def get_queue_by_name(
        self, **kwargs: Unpack[GetQueueUrlRequestServiceResourceGetQueueByNameTypeDef]
    ) -> "_Queue":
        """
        Returns the URL of an existing Amazon SQS queue.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sqs.html#SQS.ServiceResource.get_queue_by_name)
        [Show types-aiobotocore-full documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sqs/service_resource/#sqsserviceresourceget_queue_by_name-method)
        """
