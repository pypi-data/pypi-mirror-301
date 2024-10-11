"""This subpackage contains all classes that host processes (e.g. dagster-webserver)
use to manipulate and represent definitions that are resident
in user processes and containers.  e.g. ExternalPipeline.

It also contains classes that represent historical representations
that have been persisted. e.g. HistoricalPipeline
"""

from dagster._core.remote_representation.external import (
    ExternalExecutionPlan as ExternalExecutionPlan,
    ExternalJob as ExternalJob,
    ExternalPartitionSet as ExternalPartitionSet,
    ExternalRepository as ExternalRepository,
    ExternalSchedule as ExternalSchedule,
    ExternalSensor as ExternalSensor,
)
from dagster._core.remote_representation.external_data import (
    ExecutionParamsErrorSnap as ExecutionParamsErrorSnap,
    ExecutionParamsSnap as ExecutionParamsSnap,
    ExternalJobData as ExternalJobData,
    ExternalJobRef as ExternalJobRef,
    ExternalJobSubsetResult as ExternalJobSubsetResult,
    ExternalRepositoryData as ExternalRepositoryData,
    PartitionConfigSnap as PartitionConfigSnap,
    PartitionExecutionErrorSnap as PartitionExecutionErrorSnap,
    PartitionNamesSnap as PartitionNamesSnap,
    PartitionSetExecutionParamSnap as PartitionSetExecutionParamSnap,
    PartitionSetSnap as PartitionSetSnap,
    PartitionTagsSnap as PartitionTagsSnap,
    PresetSnap as PresetSnap,
    RepositoryErrorSnap as RepositoryErrorSnap,
    ScheduleExecutionErrorSnap as ScheduleExecutionErrorSnap,
    ScheduleSnap as ScheduleSnap,
    SensorExecutionErrorSnap as SensorExecutionErrorSnap,
    SensorSnap as SensorSnap,
    TargetSnap as TargetSnap,
    external_job_data_from_def as external_job_data_from_def,
    external_repository_data_from_def as external_repository_data_from_def,
)
from dagster._core.remote_representation.handle import (
    JobHandle as JobHandle,
    RepositoryHandle as RepositoryHandle,
)
from dagster._core.remote_representation.historical import HistoricalJob as HistoricalJob
from dagster._core.remote_representation.origin import (
    IN_PROCESS_NAME as IN_PROCESS_NAME,
    CodeLocationOrigin as CodeLocationOrigin,
    GrpcServerCodeLocationOrigin as GrpcServerCodeLocationOrigin,
    InProcessCodeLocationOrigin as InProcessCodeLocationOrigin,
    ManagedGrpcPythonEnvCodeLocationOrigin as ManagedGrpcPythonEnvCodeLocationOrigin,
    RemoteInstigatorOrigin as RemoteInstigatorOrigin,
    RemoteJobOrigin as RemoteJobOrigin,
    RemoteRepositoryOrigin as RemoteRepositoryOrigin,
)

# ruff: isort: split
from dagster._core.remote_representation.code_location import (
    CodeLocation as CodeLocation,
    GrpcServerCodeLocation as GrpcServerCodeLocation,
    InProcessCodeLocation as InProcessCodeLocation,
)
from dagster._core.remote_representation.job_index import JobIndex as JobIndex
from dagster._core.remote_representation.represented import RepresentedJob as RepresentedJob
