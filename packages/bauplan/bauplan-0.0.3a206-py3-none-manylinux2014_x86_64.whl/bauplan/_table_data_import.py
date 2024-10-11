from typing import Dict, List, Optional

import grpc

from bauplan._protobufs.commander_pb2 import RunnerEvent

from ._bpln_proto.commander.service.v2.service_pb2 import (
    TableDataImportRequest,
    TableDataImportResponse,
)
from ._common import (
    JobStatus,
    _JobLifeCycleHandler,
    _lifecycle,
    _OperationContainer,
    _print_debug,
)
from ._protobufs.bauplan_pb2 import (
    JobId,
    RunnerInfo,
)


class TableDataImportState:
    """
    TableDataImportState tracks information about what happened during the course of an "table create" job
    that plans a job to create an empty table based on your cloud storage to your Bauplan data catalog.

    It represents the state of the job, including job ID, job status (failure/success),
    error description (if any), and a list of events describing each step of the job.

    It also includes the output of the job: a string containing the YAML of the import plan.
    """

    job_id: str
    error: Optional[str] = None
    job_status: Optional[str] = None
    runner_events: Optional[List[RunnerEvent]]

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.runner_events = []
        self.files_to_be_imported = []


def _handle_log(log: RunnerInfo, run_state: TableDataImportState) -> bool:
    runner_event = log.runner_event
    event_type = runner_event.WhichOneof('event')
    if event_type == 'job_completion':
        match runner_event.job_completion.WhichOneof('outcome'):
            case 'success':
                run_state.job_status = JobStatus.success
            case 'failure':
                run_state.job_status = JobStatus.failed
                run_state.error = runner_event.job_completion.failure.error_message
            case 'rejected':
                run_state.job_status = JobStatus.rejected
            case 'cancellation':
                run_state.job_status = JobStatus.cancelled
            case 'timeout':
                run_state.job_status = JobStatus.timeout
            case _:
                run_state.job_status = JobStatus.unknown
        return True
    return False


class _TableImport(_OperationContainer):
    @_lifecycle
    def data_import(
        self,
        search_uri: str,
        table_name: str,
        ref: str,
        namespace: str,
        continue_on_error: bool = False,
        import_duplicate_files: bool = False,
        best_effort: bool = False,
        transformation_query: Optional[str] = None,
        no_cache: bool = False,
        args: Optional[Dict[str, str]] = None,
        lifecycle_handler: _JobLifeCycleHandler = None,
    ) -> TableDataImportState:
        """
        Create a table import plan from an S3 location.
        This is the equivalent of running through the CLI the ``bauplan import plan`` command.

        This uses a _JobLifecyleHandler to handle timeout issues (future: KeyboardInterrupt)
        We register the job_id, log_stream, and flight_client with the lifecycle_handler
        so we can do a graceful shutdown behind the scenes upon TimeoutError exception.
        """
        if not isinstance(table_name, str) or not table_name.strip():
            raise ValueError('table_name is required')
        if not isinstance(search_uri, str) or not search_uri.strip():
            raise ValueError('search_string is required')
        if not search_uri.startswith('s3://'):
            raise ValueError('search_uri must be an S3 path, e.g., s3://bucket-name/*.parquet')
        if not isinstance(ref, str) or not ref.strip():
            raise ValueError('ref is required')
        if not isinstance(continue_on_error, bool):
            raise ValueError('continue_on_error must be a bool')
        if not isinstance(import_duplicate_files, bool):
            raise ValueError('import_duplicate_files must be a bool')
        if transformation_query and not isinstance(transformation_query, str):
            raise ValueError('transformation_query must be a str')

        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)

        _print_debug(
            'Data import plan',
            'search_uri',
            search_uri,
            'from_ref',
            ref,
            'table_name',
            table_name,
            'ref',
            ref,
            'continue_on_error',
            continue_on_error,
            'import_duplicate_files',
            continue_on_error,
            'transformation_query',
            transformation_query,
            'no_cache',
            no_cache,
        )

        response: TableDataImportResponse = client_v2.TableDataImport(
            TableDataImportRequest(
                search_string=search_uri,
                continue_on_error=continue_on_error,
                best_effort=best_effort,
                import_duplicate_files=import_duplicate_files,
                trigger_run_opts={'cache': not no_cache},
                args=args or {},
                ref=ref,
                table_name=table_name,
                default_namespace=namespace,
            ),
            metadata=metadata_v2,
        )
        job_id = JobId(id=response.job_id)
        lifecycle_handler.register_job_id(job_id)
        _print_debug('table data import plan job_id', response.job_id)
        log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
        lifecycle_handler.register_log_stream(log_stream)
        state = TableDataImportState(job_id=job_id.id)
        # ATM there is no termination event so runner only sends a "JobComplete"
        for log in log_stream:
            _handle_log(log, state)
        return state
