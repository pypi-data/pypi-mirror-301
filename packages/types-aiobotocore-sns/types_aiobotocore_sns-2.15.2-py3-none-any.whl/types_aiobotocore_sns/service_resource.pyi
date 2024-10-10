"""
Type annotations for sns service ServiceResource

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/)

Usage::

    ```python
    from aiobotocore.session import get_session

    from types_aiobotocore_sns.service_resource import SNSServiceResource
    import types_aiobotocore_sns.service_resource as sns_resources

    session = get_session()
    async with session.resource("sns") as resource:
        resource: SNSServiceResource

        my_platform_application: sns_resources.PlatformApplication = resource.PlatformApplication(...)
        my_platform_endpoint: sns_resources.PlatformEndpoint = resource.PlatformEndpoint(...)
        my_subscription: sns_resources.Subscription = resource.Subscription(...)
        my_topic: sns_resources.Topic = resource.Topic(...)
```
"""

import sys
from typing import AsyncIterator, Awaitable, Dict, List, NoReturn, Sequence

from .client import SNSClient
from .type_defs import (
    AddPermissionInputTopicAddPermissionTypeDef,
    ConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef,
    CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef,
    CreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef,
    CreateTopicInputServiceResourceCreateTopicTypeDef,
    PublishInputPlatformEndpointPublishTypeDef,
    PublishInputTopicPublishTypeDef,
    PublishResponseTypeDef,
    RemovePermissionInputTopicRemovePermissionTypeDef,
    SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef,
    SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef,
    SetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef,
    SetTopicAttributesInputTopicSetAttributesTypeDef,
    SubscribeInputTopicSubscribeTypeDef,
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
    "SNSServiceResource",
    "PlatformApplication",
    "PlatformEndpoint",
    "Subscription",
    "Topic",
    "ServiceResourcePlatformApplicationsCollection",
    "ServiceResourceSubscriptionsCollection",
    "ServiceResourceTopicsCollection",
    "PlatformApplicationEndpointsCollection",
    "TopicSubscriptionsCollection",
)

class ServiceResourcePlatformApplicationsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
    """
    def all(self) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def limit(self, count: int) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Return at most this many PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def page_size(self, count: int) -> "ServiceResourcePlatformApplicationsCollection":
        """
        Fetch at most this many PlatformApplications per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def pages(self) -> AsyncIterator[List["PlatformApplication"]]:
        """
        A generator which yields pages of PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

    def __aiter__(self) -> AsyncIterator["PlatformApplication"]:
        """
        A generator which yields PlatformApplications.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.platform_applications)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourceplatformapplicationscollection)
        """

class ServiceResourceSubscriptionsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
    """
    def all(self) -> "ServiceResourceSubscriptionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "ServiceResourceSubscriptionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def limit(self, count: int) -> "ServiceResourceSubscriptionsCollection":
        """
        Return at most this many Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceSubscriptionsCollection":
        """
        Fetch at most this many Subscriptions per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def pages(self) -> AsyncIterator[List["Subscription"]]:
        """
        A generator which yields pages of Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

    def __aiter__(self) -> AsyncIterator["Subscription"]:
        """
        A generator which yields Subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.subscriptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcesubscriptionscollection)
        """

class ServiceResourceTopicsCollection(AIOResourceCollection):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
    """
    def all(self) -> "ServiceResourceTopicsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "ServiceResourceTopicsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

    def limit(self, count: int) -> "ServiceResourceTopicsCollection":
        """
        Return at most this many Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

    def page_size(self, count: int) -> "ServiceResourceTopicsCollection":
        """
        Fetch at most this many Topics per service request.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

    def pages(self) -> AsyncIterator[List["Topic"]]:
        """
        A generator which yields pages of Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

    def __aiter__(self) -> AsyncIterator["Topic"]:
        """
        A generator which yields Topics.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.topics)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#serviceresourcetopicscollection)
        """

class PlatformApplicationEndpointsCollection(AIOResourceCollection):
    def all(self) -> "PlatformApplicationEndpointsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "PlatformApplicationEndpointsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "PlatformApplicationEndpointsCollection":
        """
        Return at most this many PlatformEndpoints.
        """

    def page_size(self, count: int) -> "PlatformApplicationEndpointsCollection":
        """
        Fetch at most this many PlatformEndpoints per service request.
        """

    def pages(self) -> AsyncIterator[List["PlatformEndpoint"]]:
        """
        A generator which yields pages of PlatformEndpoints.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields PlatformEndpoints.
        """

    def __aiter__(self) -> AsyncIterator["PlatformEndpoint"]:
        """
        A generator which yields PlatformEndpoints.
        """

class TopicSubscriptionsCollection(AIOResourceCollection):
    def all(self) -> "TopicSubscriptionsCollection":
        """
        Get all items from the collection, optionally with a custom page size and item count limit.
        """

    def filter(  # type: ignore
        self, *, NextToken: str = ...
    ) -> "TopicSubscriptionsCollection":
        """
        Get items from the collection, passing keyword arguments along as parameters to the underlying service operation, which are typically used to filter the results.
        """

    def limit(self, count: int) -> "TopicSubscriptionsCollection":
        """
        Return at most this many Subscriptions.
        """

    def page_size(self, count: int) -> "TopicSubscriptionsCollection":
        """
        Fetch at most this many Subscriptions per service request.
        """

    def pages(self) -> AsyncIterator[List["Subscription"]]:
        """
        A generator which yields pages of Subscriptions.
        """

    def __iter__(self) -> NoReturn:
        """
        A generator which yields Subscriptions.
        """

    def __aiter__(self) -> AsyncIterator["Subscription"]:
        """
        A generator which yields Subscriptions.
        """

class PlatformEndpoint(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformEndpoint)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpoint)
    """

    attributes: Awaitable[Dict[str, str]]
    arn: str
    meta: "SNSResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes the endpoint for a device and mobile app from Amazon SNS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpointdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpointget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_endpoint_attributes` to update the attributes of
        the PlatformEndpoint
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpointload-method)
        """

    async def publish(
        self, **kwargs: Unpack[PublishInputPlatformEndpointPublishTypeDef]
    ) -> PublishResponseTypeDef:
        """
        Sends a message to an Amazon SNS topic, a text message (SMS message) directly
        to a phone number, or a message to a mobile platform endpoint (when you specify
        the
        `TargetArn`).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.publish)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpointpublish-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_endpoint_attributes` to update the attributes of
        the PlatformEndpoint
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpointreload-method)
        """

    async def set_attributes(
        self, **kwargs: Unpack[SetEndpointAttributesInputPlatformEndpointSetAttributesTypeDef]
    ) -> None:
        """
        Sets the attributes for an endpoint for a device on one of the supported push
        notification services, such as GCM (Firebase Cloud Messaging) and
        APNS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformEndpoint.set_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformendpointset_attributes-method)
        """

_PlatformEndpoint = PlatformEndpoint

class Subscription(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Subscription)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#subscription)
    """

    attributes: Awaitable[Dict[str, str]]
    arn: str
    meta: "SNSResourceMeta"  # type: ignore

    async def delete(self) -> None:
        """
        Deletes a subscription.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#subscriptiondelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#subscriptionget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_subscription_attributes` to update the
        attributes of the Subscription
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#subscriptionload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_subscription_attributes` to update the
        attributes of the Subscription
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#subscriptionreload-method)
        """

    async def set_attributes(
        self, **kwargs: Unpack[SetSubscriptionAttributesInputSubscriptionSetAttributesTypeDef]
    ) -> None:
        """
        Allows a subscription owner to set an attribute of the subscription to a new
        value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Subscription.set_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#subscriptionset_attributes-method)
        """

_Subscription = Subscription

class PlatformApplication(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformApplication)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplication)
    """

    attributes: Awaitable[Dict[str, str]]
    arn: str
    endpoints: PlatformApplicationEndpointsCollection
    meta: "SNSResourceMeta"  # type: ignore

    async def create_platform_endpoint(
        self,
        **kwargs: Unpack[
            CreatePlatformEndpointInputPlatformApplicationCreatePlatformEndpointTypeDef
        ],
    ) -> "_PlatformEndpoint":
        """
        Creates an endpoint for a device and mobile app on one of the supported push
        notification services, such as GCM (Firebase Cloud Messaging) and
        APNS.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.create_platform_endpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplicationcreate_platform_endpoint-method)
        """

    async def delete(self) -> None:
        """
        Deletes a platform application object for one of the supported push
        notification services, such as APNS and GCM (Firebase Cloud
        Messaging).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplicationdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplicationget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_platform_application_attributes` to update the
        attributes of the PlatformApplication
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplicationload-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_platform_application_attributes` to update the
        attributes of the PlatformApplication
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplicationreload-method)
        """

    async def set_attributes(
        self,
        **kwargs: Unpack[
            SetPlatformApplicationAttributesInputPlatformApplicationSetAttributesTypeDef
        ],
    ) -> None:
        """
        Sets the attributes of the platform application object for the supported push
        notification services, such as APNS and GCM (Firebase Cloud
        Messaging).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.PlatformApplication.set_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#platformapplicationset_attributes-method)
        """

_PlatformApplication = PlatformApplication

class Topic(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Topic)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topic)
    """

    attributes: Awaitable[Dict[str, str]]
    arn: str
    subscriptions: TopicSubscriptionsCollection
    meta: "SNSResourceMeta"  # type: ignore

    async def add_permission(
        self, **kwargs: Unpack[AddPermissionInputTopicAddPermissionTypeDef]
    ) -> None:
        """
        Adds a statement to a topic's access control policy, granting access for the
        specified Amazon Web Services accounts to the specified
        actions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.add_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicadd_permission-method)
        """

    async def confirm_subscription(
        self, **kwargs: Unpack[ConfirmSubscriptionInputTopicConfirmSubscriptionTypeDef]
    ) -> "_Subscription":
        """
        Verifies an endpoint owner's intent to receive messages by validating the token
        sent to the endpoint by an earlier `Subscribe`
        action.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.confirm_subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicconfirm_subscription-method)
        """

    async def delete(self) -> None:
        """
        Deletes a topic and all its subscriptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.delete)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicdelete-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicget_available_subresources-method)
        """

    async def load(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_topic_attributes` to update the attributes of
        the Topic
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.load)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicload-method)
        """

    async def publish(
        self, **kwargs: Unpack[PublishInputTopicPublishTypeDef]
    ) -> PublishResponseTypeDef:
        """
        Sends a message to an Amazon SNS topic, a text message (SMS message) directly
        to a phone number, or a message to a mobile platform endpoint (when you specify
        the
        `TargetArn`).

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.publish)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicpublish-method)
        """

    async def reload(self) -> None:
        """
        Calls :py:meth:`SNS.Client.get_topic_attributes` to update the attributes of
        the Topic
        resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.reload)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicreload-method)
        """

    async def remove_permission(
        self, **kwargs: Unpack[RemovePermissionInputTopicRemovePermissionTypeDef]
    ) -> None:
        """
        Removes a statement from a topic's access control policy.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.remove_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicremove_permission-method)
        """

    async def set_attributes(
        self, **kwargs: Unpack[SetTopicAttributesInputTopicSetAttributesTypeDef]
    ) -> None:
        """
        Allows a topic owner to set an attribute of the topic to a new value.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.set_attributes)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicset_attributes-method)
        """

    async def subscribe(
        self, **kwargs: Unpack[SubscribeInputTopicSubscribeTypeDef]
    ) -> "_Subscription":
        """
        Subscribes an endpoint to an Amazon SNS topic.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.Topic.subscribe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#topicsubscribe-method)
        """

_Topic = Topic

class SNSResourceMeta(ResourceMeta):
    client: SNSClient

class SNSServiceResource(AIOBoto3ServiceResource):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/)
    """

    meta: "SNSResourceMeta"  # type: ignore
    platform_applications: ServiceResourcePlatformApplicationsCollection
    subscriptions: ServiceResourceSubscriptionsCollection
    topics: ServiceResourceTopicsCollection

    async def PlatformApplication(self, arn: str) -> "_PlatformApplication":
        """
        Creates a PlatformApplication resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformApplication)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourceplatformapplication-method)
        """

    async def PlatformEndpoint(self, arn: str) -> "_PlatformEndpoint":
        """
        Creates a PlatformEndpoint resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.PlatformEndpoint)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourceplatformendpoint-method)
        """

    async def Subscription(self, arn: str) -> "_Subscription":
        """
        Creates a Subscription resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Subscription)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourcesubscription-method)
        """

    async def Topic(self, arn: str) -> "_Topic":
        """
        Creates a Topic resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.Topic)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourcetopic-method)
        """

    async def create_platform_application(
        self,
        **kwargs: Unpack[
            CreatePlatformApplicationInputServiceResourceCreatePlatformApplicationTypeDef
        ],
    ) -> "_PlatformApplication":
        """
        Creates a platform application object for one of the supported push
        notification services, such as APNS and GCM (Firebase Cloud Messaging), to
        which devices and mobile apps may
        register.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.create_platform_application)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourcecreate_platform_application-method)
        """

    async def create_topic(
        self, **kwargs: Unpack[CreateTopicInputServiceResourceCreateTopicTypeDef]
    ) -> "_Topic":
        """
        Creates a topic to which notifications can be published.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.create_topic)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourcecreate_topic-method)
        """

    async def get_available_subresources(self) -> Sequence[str]:
        """
        Returns a list of all the available sub-resources for this Resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/sns.html#SNS.ServiceResource.get_available_subresources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_sns/service_resource/#snsserviceresourceget_available_subresources-method)
        """
