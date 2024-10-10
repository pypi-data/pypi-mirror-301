"""
Type annotations for autoscaling-plans service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_autoscaling_plans.client import AutoScalingPlansClient

    session = get_session()
    async with session.create_client("autoscaling-plans") as client:
        client: AutoScalingPlansClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type, overload

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import DescribeScalingPlanResourcesPaginator, DescribeScalingPlansPaginator
from .type_defs import (
    CreateScalingPlanRequestRequestTypeDef,
    CreateScalingPlanResponseTypeDef,
    DeleteScalingPlanRequestRequestTypeDef,
    DescribeScalingPlanResourcesRequestRequestTypeDef,
    DescribeScalingPlanResourcesResponseTypeDef,
    DescribeScalingPlansRequestRequestTypeDef,
    DescribeScalingPlansResponseTypeDef,
    GetScalingPlanResourceForecastDataRequestRequestTypeDef,
    GetScalingPlanResourceForecastDataResponseTypeDef,
    UpdateScalingPlanRequestRequestTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("AutoScalingPlansClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConcurrentUpdateException: Type[BotocoreClientError]
    InternalServiceException: Type[BotocoreClientError]
    InvalidNextTokenException: Type[BotocoreClientError]
    LimitExceededException: Type[BotocoreClientError]
    ObjectNotFoundException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class AutoScalingPlansClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        AutoScalingPlansClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#exceptions)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#close)
        """

    async def create_scaling_plan(
        self, **kwargs: Unpack[CreateScalingPlanRequestRequestTypeDef]
    ) -> CreateScalingPlanResponseTypeDef:
        """
        Creates a scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.create_scaling_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#create_scaling_plan)
        """

    async def delete_scaling_plan(
        self, **kwargs: Unpack[DeleteScalingPlanRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes the specified scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.delete_scaling_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#delete_scaling_plan)
        """

    async def describe_scaling_plan_resources(
        self, **kwargs: Unpack[DescribeScalingPlanResourcesRequestRequestTypeDef]
    ) -> DescribeScalingPlanResourcesResponseTypeDef:
        """
        Describes the scalable resources in the specified scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.describe_scaling_plan_resources)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#describe_scaling_plan_resources)
        """

    async def describe_scaling_plans(
        self, **kwargs: Unpack[DescribeScalingPlansRequestRequestTypeDef]
    ) -> DescribeScalingPlansResponseTypeDef:
        """
        Describes one or more of your scaling plans.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.describe_scaling_plans)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#describe_scaling_plans)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#generate_presigned_url)
        """

    async def get_scaling_plan_resource_forecast_data(
        self, **kwargs: Unpack[GetScalingPlanResourceForecastDataRequestRequestTypeDef]
    ) -> GetScalingPlanResourceForecastDataResponseTypeDef:
        """
        Retrieves the forecast data for a scalable resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_scaling_plan_resource_forecast_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#get_scaling_plan_resource_forecast_data)
        """

    async def update_scaling_plan(
        self, **kwargs: Unpack[UpdateScalingPlanRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Updates the specified scaling plan.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.update_scaling_plan)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#update_scaling_plan)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_plan_resources"]
    ) -> DescribeScalingPlanResourcesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#get_paginator)
        """

    @overload
    def get_paginator(
        self, operation_name: Literal["describe_scaling_plans"]
    ) -> DescribeScalingPlansPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/#get_paginator)
        """

    async def __aenter__(self) -> "AutoScalingPlansClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/autoscaling-plans.html#AutoScalingPlans.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_autoscaling_plans/client/)
        """
