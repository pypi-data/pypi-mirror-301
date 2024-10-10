"""
Type annotations for networkmonitor service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_networkmonitor.client import CloudWatchNetworkMonitorClient

    session = get_session()
    async with session.create_client("networkmonitor") as client:
        client: CloudWatchNetworkMonitorClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListMonitorsPaginator
from .type_defs import (
    CreateMonitorInputRequestTypeDef,
    CreateMonitorOutputTypeDef,
    CreateProbeInputRequestTypeDef,
    CreateProbeOutputTypeDef,
    DeleteMonitorInputRequestTypeDef,
    DeleteProbeInputRequestTypeDef,
    GetMonitorInputRequestTypeDef,
    GetMonitorOutputTypeDef,
    GetProbeInputRequestTypeDef,
    GetProbeOutputTypeDef,
    ListMonitorsInputRequestTypeDef,
    ListMonitorsOutputTypeDef,
    ListTagsForResourceInputRequestTypeDef,
    ListTagsForResourceOutputTypeDef,
    TagResourceInputRequestTypeDef,
    UntagResourceInputRequestTypeDef,
    UpdateMonitorInputRequestTypeDef,
    UpdateMonitorOutputTypeDef,
    UpdateProbeInputRequestTypeDef,
    UpdateProbeOutputTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CloudWatchNetworkMonitorClient",)

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

class CloudWatchNetworkMonitorClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CloudWatchNetworkMonitorClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#close)
        """

    async def create_monitor(
        self, **kwargs: Unpack[CreateMonitorInputRequestTypeDef]
    ) -> CreateMonitorOutputTypeDef:
        """
        Creates a monitor between a source subnet and destination IP address.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.create_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#create_monitor)
        """

    async def create_probe(
        self, **kwargs: Unpack[CreateProbeInputRequestTypeDef]
    ) -> CreateProbeOutputTypeDef:
        """
        Create a probe within a monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.create_probe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#create_probe)
        """

    async def delete_monitor(
        self, **kwargs: Unpack[DeleteMonitorInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a specified monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.delete_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#delete_monitor)
        """

    async def delete_probe(
        self, **kwargs: Unpack[DeleteProbeInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified probe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.delete_probe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#delete_probe)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#generate_presigned_url)
        """

    async def get_monitor(
        self, **kwargs: Unpack[GetMonitorInputRequestTypeDef]
    ) -> GetMonitorOutputTypeDef:
        """
        Returns details about a specific monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.get_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#get_monitor)
        """

    async def get_probe(
        self, **kwargs: Unpack[GetProbeInputRequestTypeDef]
    ) -> GetProbeOutputTypeDef:
        """
        Returns the details about a probe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.get_probe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#get_probe)
        """

    async def list_monitors(
        self, **kwargs: Unpack[ListMonitorsInputRequestTypeDef]
    ) -> ListMonitorsOutputTypeDef:
        """
        Returns a list of all of your monitors.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.list_monitors)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#list_monitors)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceInputRequestTypeDef]
    ) -> ListTagsForResourceOutputTypeDef:
        """
        Lists the tags assigned to this resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#list_tags_for_resource)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Adds key-value pairs to a monitor or probe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceInputRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Removes a key-value pair from a monitor or probe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#untag_resource)
        """

    async def update_monitor(
        self, **kwargs: Unpack[UpdateMonitorInputRequestTypeDef]
    ) -> UpdateMonitorOutputTypeDef:
        """
        Updates the `aggregationPeriod` for a monitor.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.update_monitor)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#update_monitor)
        """

    async def update_probe(
        self, **kwargs: Unpack[UpdateProbeInputRequestTypeDef]
    ) -> UpdateProbeOutputTypeDef:
        """
        Updates a monitor probe.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.update_probe)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#update_probe)
        """

    def get_paginator(self, operation_name: Literal["list_monitors"]) -> ListMonitorsPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/#get_paginator)
        """

    async def __aenter__(self) -> "CloudWatchNetworkMonitorClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/networkmonitor.html#CloudWatchNetworkMonitor.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_networkmonitor/client/)
        """
