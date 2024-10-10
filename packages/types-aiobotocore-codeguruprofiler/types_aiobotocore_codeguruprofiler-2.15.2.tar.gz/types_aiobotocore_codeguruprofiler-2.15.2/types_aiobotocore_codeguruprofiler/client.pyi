"""
Type annotations for codeguruprofiler service client.

[Open documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)

Usage::

    ```python
    from aiobotocore.session import get_session
    from types_aiobotocore_codeguruprofiler.client import CodeGuruProfilerClient

    session = get_session()
    async with session.create_client("codeguruprofiler") as client:
        client: CodeGuruProfilerClient
    ```
"""

import sys
from typing import Any, Dict, Mapping, Type

from aiobotocore.client import AioBaseClient
from botocore.client import ClientMeta

from .paginator import ListProfileTimesPaginator
from .type_defs import (
    AddNotificationChannelsRequestRequestTypeDef,
    AddNotificationChannelsResponseTypeDef,
    BatchGetFrameMetricDataRequestRequestTypeDef,
    BatchGetFrameMetricDataResponseTypeDef,
    ConfigureAgentRequestRequestTypeDef,
    ConfigureAgentResponseTypeDef,
    CreateProfilingGroupRequestRequestTypeDef,
    CreateProfilingGroupResponseTypeDef,
    DeleteProfilingGroupRequestRequestTypeDef,
    DescribeProfilingGroupRequestRequestTypeDef,
    DescribeProfilingGroupResponseTypeDef,
    GetFindingsReportAccountSummaryRequestRequestTypeDef,
    GetFindingsReportAccountSummaryResponseTypeDef,
    GetNotificationConfigurationRequestRequestTypeDef,
    GetNotificationConfigurationResponseTypeDef,
    GetPolicyRequestRequestTypeDef,
    GetPolicyResponseTypeDef,
    GetProfileRequestRequestTypeDef,
    GetProfileResponseTypeDef,
    GetRecommendationsRequestRequestTypeDef,
    GetRecommendationsResponseTypeDef,
    ListFindingsReportsRequestRequestTypeDef,
    ListFindingsReportsResponseTypeDef,
    ListProfileTimesRequestRequestTypeDef,
    ListProfileTimesResponseTypeDef,
    ListProfilingGroupsRequestRequestTypeDef,
    ListProfilingGroupsResponseTypeDef,
    ListTagsForResourceRequestRequestTypeDef,
    ListTagsForResourceResponseTypeDef,
    PostAgentProfileRequestRequestTypeDef,
    PutPermissionRequestRequestTypeDef,
    PutPermissionResponseTypeDef,
    RemoveNotificationChannelRequestRequestTypeDef,
    RemoveNotificationChannelResponseTypeDef,
    RemovePermissionRequestRequestTypeDef,
    RemovePermissionResponseTypeDef,
    SubmitFeedbackRequestRequestTypeDef,
    TagResourceRequestRequestTypeDef,
    UntagResourceRequestRequestTypeDef,
    UpdateProfilingGroupRequestRequestTypeDef,
    UpdateProfilingGroupResponseTypeDef,
)

if sys.version_info >= (3, 12):
    from typing import Literal, Unpack
else:
    from typing_extensions import Literal, Unpack

__all__ = ("CodeGuruProfilerClient",)

class BotocoreClientError(Exception):
    MSG_TEMPLATE: str

    def __init__(self, error_response: Mapping[str, Any], operation_name: str) -> None:
        self.response: Dict[str, Any]
        self.operation_name: str

class Exceptions:
    ClientError: Type[BotocoreClientError]
    ConflictException: Type[BotocoreClientError]
    InternalServerException: Type[BotocoreClientError]
    ResourceNotFoundException: Type[BotocoreClientError]
    ServiceQuotaExceededException: Type[BotocoreClientError]
    ThrottlingException: Type[BotocoreClientError]
    ValidationException: Type[BotocoreClientError]

class CodeGuruProfilerClient(AioBaseClient):
    """
    [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
    [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
    """

    meta: ClientMeta

    @property
    def exceptions(self) -> Exceptions:
        """
        CodeGuruProfilerClient exceptions.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.exceptions)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#exceptions)
        """

    async def add_notification_channels(
        self, **kwargs: Unpack[AddNotificationChannelsRequestRequestTypeDef]
    ) -> AddNotificationChannelsResponseTypeDef:
        """
        Add up to 2 anomaly notifications channels for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.add_notification_channels)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#add_notification_channels)
        """

    async def batch_get_frame_metric_data(
        self, **kwargs: Unpack[BatchGetFrameMetricDataRequestRequestTypeDef]
    ) -> BatchGetFrameMetricDataResponseTypeDef:
        """
        Returns the time series of values for a requested list of frame metrics from a
        time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.batch_get_frame_metric_data)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#batch_get_frame_metric_data)
        """

    def can_paginate(self, operation_name: str) -> bool:
        """
        Check if an operation can be paginated.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.can_paginate)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#can_paginate)
        """

    async def close(self) -> None:
        """
        Closes underlying endpoint connections.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.close)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#close)
        """

    async def configure_agent(
        self, **kwargs: Unpack[ConfigureAgentRequestRequestTypeDef]
    ) -> ConfigureAgentResponseTypeDef:
        """
        Used by profiler agents to report their current state and to receive remote
        configuration
        updates.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.configure_agent)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#configure_agent)
        """

    async def create_profiling_group(
        self, **kwargs: Unpack[CreateProfilingGroupRequestRequestTypeDef]
    ) -> CreateProfilingGroupResponseTypeDef:
        """
        Creates a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.create_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#create_profiling_group)
        """

    async def delete_profiling_group(
        self, **kwargs: Unpack[DeleteProfilingGroupRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Deletes a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.delete_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#delete_profiling_group)
        """

    async def describe_profiling_group(
        self, **kwargs: Unpack[DescribeProfilingGroupRequestRequestTypeDef]
    ) -> DescribeProfilingGroupResponseTypeDef:
        """
        Returns a
        [ProfilingGroupDescription](https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_ProfilingGroupDescription.html)
        object that contains information about the requested profiling
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.describe_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#describe_profiling_group)
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

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.generate_presigned_url)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#generate_presigned_url)
        """

    async def get_findings_report_account_summary(
        self, **kwargs: Unpack[GetFindingsReportAccountSummaryRequestRequestTypeDef]
    ) -> GetFindingsReportAccountSummaryResponseTypeDef:
        """
        Returns a list of
        [FindingsReportSummary](https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_FindingsReportSummary.html)
        objects that contain analysis results for all profiling groups in your AWS
        account.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_findings_report_account_summary)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_findings_report_account_summary)
        """

    async def get_notification_configuration(
        self, **kwargs: Unpack[GetNotificationConfigurationRequestRequestTypeDef]
    ) -> GetNotificationConfigurationResponseTypeDef:
        """
        Get the current configuration for anomaly notifications for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_notification_configuration)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_notification_configuration)
        """

    async def get_policy(
        self, **kwargs: Unpack[GetPolicyRequestRequestTypeDef]
    ) -> GetPolicyResponseTypeDef:
        """
        Returns the JSON-formatted resource-based policy on a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_policy)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_policy)
        """

    async def get_profile(
        self, **kwargs: Unpack[GetProfileRequestRequestTypeDef]
    ) -> GetProfileResponseTypeDef:
        """
        Gets the aggregated profile of a profiling group for a specified time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_profile)
        """

    async def get_recommendations(
        self, **kwargs: Unpack[GetRecommendationsRequestRequestTypeDef]
    ) -> GetRecommendationsResponseTypeDef:
        """
        Returns a list of
        [Recommendation](https://docs.aws.amazon.com/codeguru/latest/profiler-api/API_Recommendation.html)
        objects that contain recommendations for a profiling group for a given time
        period.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_recommendations)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_recommendations)
        """

    async def list_findings_reports(
        self, **kwargs: Unpack[ListFindingsReportsRequestRequestTypeDef]
    ) -> ListFindingsReportsResponseTypeDef:
        """
        List the available reports for a given profiling group and time range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_findings_reports)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_findings_reports)
        """

    async def list_profile_times(
        self, **kwargs: Unpack[ListProfileTimesRequestRequestTypeDef]
    ) -> ListProfileTimesResponseTypeDef:
        """
        Lists the start times of the available aggregated profiles of a profiling group
        for an aggregation period within the specified time
        range.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_profile_times)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_profile_times)
        """

    async def list_profiling_groups(
        self, **kwargs: Unpack[ListProfilingGroupsRequestRequestTypeDef]
    ) -> ListProfilingGroupsResponseTypeDef:
        """
        Returns a list of profiling groups.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_profiling_groups)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_profiling_groups)
        """

    async def list_tags_for_resource(
        self, **kwargs: Unpack[ListTagsForResourceRequestRequestTypeDef]
    ) -> ListTagsForResourceResponseTypeDef:
        """
        Returns a list of the tags that are assigned to a specified resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.list_tags_for_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#list_tags_for_resource)
        """

    async def post_agent_profile(
        self, **kwargs: Unpack[PostAgentProfileRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Submits profiling data to an aggregated profile of a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.post_agent_profile)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#post_agent_profile)
        """

    async def put_permission(
        self, **kwargs: Unpack[PutPermissionRequestRequestTypeDef]
    ) -> PutPermissionResponseTypeDef:
        """
        Adds permissions to a profiling group's resource-based policy that are provided
        using an action
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.put_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#put_permission)
        """

    async def remove_notification_channel(
        self, **kwargs: Unpack[RemoveNotificationChannelRequestRequestTypeDef]
    ) -> RemoveNotificationChannelResponseTypeDef:
        """
        Remove one anomaly notifications channel for a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.remove_notification_channel)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#remove_notification_channel)
        """

    async def remove_permission(
        self, **kwargs: Unpack[RemovePermissionRequestRequestTypeDef]
    ) -> RemovePermissionResponseTypeDef:
        """
        Removes permissions from a profiling group's resource-based policy that are
        provided using an action
        group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.remove_permission)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#remove_permission)
        """

    async def submit_feedback(
        self, **kwargs: Unpack[SubmitFeedbackRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Sends feedback to CodeGuru Profiler about whether the anomaly detected by the
        analysis is useful or
        not.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.submit_feedback)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#submit_feedback)
        """

    async def tag_resource(
        self, **kwargs: Unpack[TagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use to assign one or more tags to a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.tag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#tag_resource)
        """

    async def untag_resource(
        self, **kwargs: Unpack[UntagResourceRequestRequestTypeDef]
    ) -> Dict[str, Any]:
        """
        Use to remove one or more tags from a resource.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.untag_resource)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#untag_resource)
        """

    async def update_profiling_group(
        self, **kwargs: Unpack[UpdateProfilingGroupRequestRequestTypeDef]
    ) -> UpdateProfilingGroupResponseTypeDef:
        """
        Updates a profiling group.

        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.update_profiling_group)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#update_profiling_group)
        """

    def get_paginator(
        self, operation_name: Literal["list_profile_times"]
    ) -> ListProfileTimesPaginator:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client.get_paginator)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/#get_paginator)
        """

    async def __aenter__(self) -> "CodeGuruProfilerClient":
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
        """

    async def __aexit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> Any:
        """
        [Show boto3 documentation](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/codeguruprofiler.html#CodeGuruProfiler.Client)
        [Show types-aiobotocore documentation](https://youtype.github.io/types_aiobotocore_docs/types_aiobotocore_codeguruprofiler/client/)
        """
