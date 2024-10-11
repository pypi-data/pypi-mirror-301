"""
Type annotations for supplychain service type definitions.

[Open documentation](https://youtype.github.io/boto3_stubs_docs/mypy_boto3_supplychain/type_defs/)

Usage::

    ```python
    from mypy_boto3_supplychain.type_defs import BillOfMaterialsImportJobTypeDef

    data: BillOfMaterialsImportJobTypeDef = ...
    ```
"""

import sys
from datetime import datetime
from typing import Dict, List, Mapping, Sequence, Union

from .literals import (
    ConfigurationJobStatusType,
    DataIntegrationEventTypeType,
    DataIntegrationFlowFileTypeType,
    DataIntegrationFlowLoadTypeType,
    DataIntegrationFlowSourceTypeType,
    DataIntegrationFlowTargetTypeType,
    DataIntegrationFlowTransformationTypeType,
    DataLakeDatasetSchemaFieldTypeType,
)

if sys.version_info >= (3, 12):
    from typing import NotRequired, TypedDict
else:
    from typing_extensions import NotRequired, TypedDict

__all__ = (
    "BillOfMaterialsImportJobTypeDef",
    "CreateBillOfMaterialsImportJobRequestRequestTypeDef",
    "ResponseMetadataTypeDef",
    "DataIntegrationFlowDatasetOptionsTypeDef",
    "DataIntegrationFlowS3OptionsTypeDef",
    "DataIntegrationFlowSQLTransformationConfigurationTypeDef",
    "DataLakeDatasetSchemaFieldTypeDef",
    "DeleteDataIntegrationFlowRequestRequestTypeDef",
    "DeleteDataLakeDatasetRequestRequestTypeDef",
    "GetBillOfMaterialsImportJobRequestRequestTypeDef",
    "GetDataIntegrationFlowRequestRequestTypeDef",
    "GetDataLakeDatasetRequestRequestTypeDef",
    "PaginatorConfigTypeDef",
    "ListDataIntegrationFlowsRequestRequestTypeDef",
    "ListDataLakeDatasetsRequestRequestTypeDef",
    "ListTagsForResourceRequestRequestTypeDef",
    "TimestampTypeDef",
    "TagResourceRequestRequestTypeDef",
    "UntagResourceRequestRequestTypeDef",
    "UpdateDataLakeDatasetRequestRequestTypeDef",
    "CreateBillOfMaterialsImportJobResponseTypeDef",
    "CreateDataIntegrationFlowResponseTypeDef",
    "DeleteDataIntegrationFlowResponseTypeDef",
    "DeleteDataLakeDatasetResponseTypeDef",
    "GetBillOfMaterialsImportJobResponseTypeDef",
    "ListTagsForResourceResponseTypeDef",
    "SendDataIntegrationEventResponseTypeDef",
    "DataIntegrationFlowDatasetSourceConfigurationTypeDef",
    "DataIntegrationFlowDatasetTargetConfigurationTypeDef",
    "DataIntegrationFlowS3SourceConfigurationTypeDef",
    "DataIntegrationFlowS3TargetConfigurationTypeDef",
    "DataIntegrationFlowTransformationTypeDef",
    "DataLakeDatasetSchemaOutputTypeDef",
    "DataLakeDatasetSchemaTypeDef",
    "ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef",
    "ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef",
    "SendDataIntegrationEventRequestRequestTypeDef",
    "DataIntegrationFlowSourceTypeDef",
    "DataIntegrationFlowTargetTypeDef",
    "DataLakeDatasetTypeDef",
    "CreateDataLakeDatasetRequestRequestTypeDef",
    "CreateDataIntegrationFlowRequestRequestTypeDef",
    "DataIntegrationFlowTypeDef",
    "UpdateDataIntegrationFlowRequestRequestTypeDef",
    "CreateDataLakeDatasetResponseTypeDef",
    "GetDataLakeDatasetResponseTypeDef",
    "ListDataLakeDatasetsResponseTypeDef",
    "UpdateDataLakeDatasetResponseTypeDef",
    "GetDataIntegrationFlowResponseTypeDef",
    "ListDataIntegrationFlowsResponseTypeDef",
    "UpdateDataIntegrationFlowResponseTypeDef",
)

BillOfMaterialsImportJobTypeDef = TypedDict(
    "BillOfMaterialsImportJobTypeDef",
    {
        "instanceId": str,
        "jobId": str,
        "status": ConfigurationJobStatusType,
        "s3uri": str,
        "message": NotRequired[str],
    },
)
CreateBillOfMaterialsImportJobRequestRequestTypeDef = TypedDict(
    "CreateBillOfMaterialsImportJobRequestRequestTypeDef",
    {
        "instanceId": str,
        "s3uri": str,
        "clientToken": NotRequired[str],
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
DataIntegrationFlowDatasetOptionsTypeDef = TypedDict(
    "DataIntegrationFlowDatasetOptionsTypeDef",
    {
        "loadType": NotRequired[DataIntegrationFlowLoadTypeType],
        "dedupeRecords": NotRequired[bool],
    },
)
DataIntegrationFlowS3OptionsTypeDef = TypedDict(
    "DataIntegrationFlowS3OptionsTypeDef",
    {
        "fileType": NotRequired[DataIntegrationFlowFileTypeType],
    },
)
DataIntegrationFlowSQLTransformationConfigurationTypeDef = TypedDict(
    "DataIntegrationFlowSQLTransformationConfigurationTypeDef",
    {
        "query": str,
    },
)
DataLakeDatasetSchemaFieldTypeDef = TypedDict(
    "DataLakeDatasetSchemaFieldTypeDef",
    {
        "name": str,
        "type": DataLakeDatasetSchemaFieldTypeType,
        "isRequired": bool,
    },
)
DeleteDataIntegrationFlowRequestRequestTypeDef = TypedDict(
    "DeleteDataIntegrationFlowRequestRequestTypeDef",
    {
        "instanceId": str,
        "name": str,
    },
)
DeleteDataLakeDatasetRequestRequestTypeDef = TypedDict(
    "DeleteDataLakeDatasetRequestRequestTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "name": str,
    },
)
GetBillOfMaterialsImportJobRequestRequestTypeDef = TypedDict(
    "GetBillOfMaterialsImportJobRequestRequestTypeDef",
    {
        "instanceId": str,
        "jobId": str,
    },
)
GetDataIntegrationFlowRequestRequestTypeDef = TypedDict(
    "GetDataIntegrationFlowRequestRequestTypeDef",
    {
        "instanceId": str,
        "name": str,
    },
)
GetDataLakeDatasetRequestRequestTypeDef = TypedDict(
    "GetDataLakeDatasetRequestRequestTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "name": str,
    },
)
PaginatorConfigTypeDef = TypedDict(
    "PaginatorConfigTypeDef",
    {
        "MaxItems": NotRequired[int],
        "PageSize": NotRequired[int],
        "StartingToken": NotRequired[str],
    },
)
ListDataIntegrationFlowsRequestRequestTypeDef = TypedDict(
    "ListDataIntegrationFlowsRequestRequestTypeDef",
    {
        "instanceId": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListDataLakeDatasetsRequestRequestTypeDef = TypedDict(
    "ListDataLakeDatasetsRequestRequestTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "nextToken": NotRequired[str],
        "maxResults": NotRequired[int],
    },
)
ListTagsForResourceRequestRequestTypeDef = TypedDict(
    "ListTagsForResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
    },
)
TimestampTypeDef = Union[datetime, str]
TagResourceRequestRequestTypeDef = TypedDict(
    "TagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tags": Mapping[str, str],
    },
)
UntagResourceRequestRequestTypeDef = TypedDict(
    "UntagResourceRequestRequestTypeDef",
    {
        "resourceArn": str,
        "tagKeys": Sequence[str],
    },
)
UpdateDataLakeDatasetRequestRequestTypeDef = TypedDict(
    "UpdateDataLakeDatasetRequestRequestTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "name": str,
        "description": NotRequired[str],
    },
)
CreateBillOfMaterialsImportJobResponseTypeDef = TypedDict(
    "CreateBillOfMaterialsImportJobResponseTypeDef",
    {
        "jobId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
CreateDataIntegrationFlowResponseTypeDef = TypedDict(
    "CreateDataIntegrationFlowResponseTypeDef",
    {
        "instanceId": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataIntegrationFlowResponseTypeDef = TypedDict(
    "DeleteDataIntegrationFlowResponseTypeDef",
    {
        "instanceId": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DeleteDataLakeDatasetResponseTypeDef = TypedDict(
    "DeleteDataLakeDatasetResponseTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "name": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetBillOfMaterialsImportJobResponseTypeDef = TypedDict(
    "GetBillOfMaterialsImportJobResponseTypeDef",
    {
        "job": BillOfMaterialsImportJobTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListTagsForResourceResponseTypeDef = TypedDict(
    "ListTagsForResourceResponseTypeDef",
    {
        "tags": Dict[str, str],
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
SendDataIntegrationEventResponseTypeDef = TypedDict(
    "SendDataIntegrationEventResponseTypeDef",
    {
        "eventId": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
DataIntegrationFlowDatasetSourceConfigurationTypeDef = TypedDict(
    "DataIntegrationFlowDatasetSourceConfigurationTypeDef",
    {
        "datasetIdentifier": str,
        "options": NotRequired[DataIntegrationFlowDatasetOptionsTypeDef],
    },
)
DataIntegrationFlowDatasetTargetConfigurationTypeDef = TypedDict(
    "DataIntegrationFlowDatasetTargetConfigurationTypeDef",
    {
        "datasetIdentifier": str,
        "options": NotRequired[DataIntegrationFlowDatasetOptionsTypeDef],
    },
)
DataIntegrationFlowS3SourceConfigurationTypeDef = TypedDict(
    "DataIntegrationFlowS3SourceConfigurationTypeDef",
    {
        "bucketName": str,
        "prefix": str,
        "options": NotRequired[DataIntegrationFlowS3OptionsTypeDef],
    },
)
DataIntegrationFlowS3TargetConfigurationTypeDef = TypedDict(
    "DataIntegrationFlowS3TargetConfigurationTypeDef",
    {
        "bucketName": str,
        "prefix": str,
        "options": NotRequired[DataIntegrationFlowS3OptionsTypeDef],
    },
)
DataIntegrationFlowTransformationTypeDef = TypedDict(
    "DataIntegrationFlowTransformationTypeDef",
    {
        "transformationType": DataIntegrationFlowTransformationTypeType,
        "sqlTransformation": NotRequired[DataIntegrationFlowSQLTransformationConfigurationTypeDef],
    },
)
DataLakeDatasetSchemaOutputTypeDef = TypedDict(
    "DataLakeDatasetSchemaOutputTypeDef",
    {
        "name": str,
        "fields": List[DataLakeDatasetSchemaFieldTypeDef],
    },
)
DataLakeDatasetSchemaTypeDef = TypedDict(
    "DataLakeDatasetSchemaTypeDef",
    {
        "name": str,
        "fields": Sequence[DataLakeDatasetSchemaFieldTypeDef],
    },
)
ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef = TypedDict(
    "ListDataIntegrationFlowsRequestListDataIntegrationFlowsPaginateTypeDef",
    {
        "instanceId": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef = TypedDict(
    "ListDataLakeDatasetsRequestListDataLakeDatasetsPaginateTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "PaginationConfig": NotRequired[PaginatorConfigTypeDef],
    },
)
SendDataIntegrationEventRequestRequestTypeDef = TypedDict(
    "SendDataIntegrationEventRequestRequestTypeDef",
    {
        "instanceId": str,
        "eventType": DataIntegrationEventTypeType,
        "data": str,
        "eventGroupId": str,
        "eventTimestamp": NotRequired[TimestampTypeDef],
        "clientToken": NotRequired[str],
    },
)
DataIntegrationFlowSourceTypeDef = TypedDict(
    "DataIntegrationFlowSourceTypeDef",
    {
        "sourceType": DataIntegrationFlowSourceTypeType,
        "sourceName": str,
        "s3Source": NotRequired[DataIntegrationFlowS3SourceConfigurationTypeDef],
        "datasetSource": NotRequired[DataIntegrationFlowDatasetSourceConfigurationTypeDef],
    },
)
DataIntegrationFlowTargetTypeDef = TypedDict(
    "DataIntegrationFlowTargetTypeDef",
    {
        "targetType": DataIntegrationFlowTargetTypeType,
        "s3Target": NotRequired[DataIntegrationFlowS3TargetConfigurationTypeDef],
        "datasetTarget": NotRequired[DataIntegrationFlowDatasetTargetConfigurationTypeDef],
    },
)
DataLakeDatasetTypeDef = TypedDict(
    "DataLakeDatasetTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "name": str,
        "arn": str,
        "schema": DataLakeDatasetSchemaOutputTypeDef,
        "createdTime": datetime,
        "lastModifiedTime": datetime,
        "description": NotRequired[str],
    },
)
CreateDataLakeDatasetRequestRequestTypeDef = TypedDict(
    "CreateDataLakeDatasetRequestRequestTypeDef",
    {
        "instanceId": str,
        "namespace": str,
        "name": str,
        "schema": NotRequired[DataLakeDatasetSchemaTypeDef],
        "description": NotRequired[str],
        "tags": NotRequired[Mapping[str, str]],
    },
)
CreateDataIntegrationFlowRequestRequestTypeDef = TypedDict(
    "CreateDataIntegrationFlowRequestRequestTypeDef",
    {
        "instanceId": str,
        "name": str,
        "sources": Sequence[DataIntegrationFlowSourceTypeDef],
        "transformation": DataIntegrationFlowTransformationTypeDef,
        "target": DataIntegrationFlowTargetTypeDef,
        "tags": NotRequired[Mapping[str, str]],
    },
)
DataIntegrationFlowTypeDef = TypedDict(
    "DataIntegrationFlowTypeDef",
    {
        "instanceId": str,
        "name": str,
        "sources": List[DataIntegrationFlowSourceTypeDef],
        "transformation": DataIntegrationFlowTransformationTypeDef,
        "target": DataIntegrationFlowTargetTypeDef,
        "createdTime": datetime,
        "lastModifiedTime": datetime,
    },
)
UpdateDataIntegrationFlowRequestRequestTypeDef = TypedDict(
    "UpdateDataIntegrationFlowRequestRequestTypeDef",
    {
        "instanceId": str,
        "name": str,
        "sources": NotRequired[Sequence[DataIntegrationFlowSourceTypeDef]],
        "transformation": NotRequired[DataIntegrationFlowTransformationTypeDef],
        "target": NotRequired[DataIntegrationFlowTargetTypeDef],
    },
)
CreateDataLakeDatasetResponseTypeDef = TypedDict(
    "CreateDataLakeDatasetResponseTypeDef",
    {
        "dataset": DataLakeDatasetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataLakeDatasetResponseTypeDef = TypedDict(
    "GetDataLakeDatasetResponseTypeDef",
    {
        "dataset": DataLakeDatasetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDataLakeDatasetsResponseTypeDef = TypedDict(
    "ListDataLakeDatasetsResponseTypeDef",
    {
        "datasets": List[DataLakeDatasetTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataLakeDatasetResponseTypeDef = TypedDict(
    "UpdateDataLakeDatasetResponseTypeDef",
    {
        "dataset": DataLakeDatasetTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
GetDataIntegrationFlowResponseTypeDef = TypedDict(
    "GetDataIntegrationFlowResponseTypeDef",
    {
        "flow": DataIntegrationFlowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
ListDataIntegrationFlowsResponseTypeDef = TypedDict(
    "ListDataIntegrationFlowsResponseTypeDef",
    {
        "flows": List[DataIntegrationFlowTypeDef],
        "nextToken": str,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
UpdateDataIntegrationFlowResponseTypeDef = TypedDict(
    "UpdateDataIntegrationFlowResponseTypeDef",
    {
        "flow": DataIntegrationFlowTypeDef,
        "ResponseMetadata": ResponseMetadataTypeDef,
    },
)
