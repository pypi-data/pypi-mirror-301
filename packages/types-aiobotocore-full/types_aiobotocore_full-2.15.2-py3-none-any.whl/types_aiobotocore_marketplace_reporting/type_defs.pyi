"""
Type annotations for marketplace-reporting service type definitions.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_marketplace_reporting/type_defs/)

Usage::

    ```python
    from types_aiobotocore_marketplace_reporting.type_defs import GetBuyerDashboardInputRequestTypeDef

    data: GetBuyerDashboardInputRequestTypeDef = ...
    ```
"""

import sys
from typing import Dict, List, Sequence

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "GetBuyerDashboardInputRequestTypeDef",
    "ResponseMetadataTypeDef",
    "GetBuyerDashboardOutputTypeDef",
)

GetBuyerDashboardInputRequestTypeDef = TypedDict(
    "GetBuyerDashboardInputRequestTypeDef",
    {
        "dashboardIdentifier": str,
        "embeddingDomains": Sequence[str],
    },
)
ResponseMetadataTypeDef = TypedDict(
    "ResponseMetadataTypeDef",
    {
        "RequestId": str,
        "HTTPStatusCode": int,
        "HTTPHeaders": Dict[str, str],
        "RetryAttempts": int,
        "HostId": NotRequired[str],
    },
)
GetBuyerDashboardOutputTypeDef = TypedDict(
    "GetBuyerDashboardOutputTypeDef",
    {
        "embedUrl": str,
        "dashboardIdentifier": str,
        "embeddingDomains": List[str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
