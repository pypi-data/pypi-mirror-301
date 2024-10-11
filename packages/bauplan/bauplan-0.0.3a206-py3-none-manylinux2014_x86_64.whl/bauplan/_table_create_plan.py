from typing import Dict, List, Optional

import grpc

from bauplan._protobufs.commander_pb2 import RunnerEvent

from ._bpln_proto.commander.service.v2.service_pb2 import (
    TableCreatePlanApplyRequest,
    TableCreatePlanApplyResponse,
    TableCreatePlanRequest,
    TableCreatePlanResponse,
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


class TableCreatePlanApplyState:
    """
    TableCreatePlanApplyState tracks information about what happened during the course of an "table create" job
    that plans a job to create an empty table based on your cloud storage to your Bauplan data catalog.

    It represents the state of the job, including job ID, job status (failure/success),
    error description (if any), and a list of events describing each step of the job.

    It also includes the output of the job: a string containing the YAML of the import plan.
    """

    job_id: str
    plan: Optional[str] = None
    error: Optional[str] = None
    job_status: Optional[str] = None
    runner_events: Optional[List[RunnerEvent]]

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.runner_events = []


class TableCreatePlanState:
    """
    TableCreatePlanState tracks information about what happened during the course of an "table create" job
    that plans a job to create an empty table based on your cloud storage to your Bauplan data catalog.

    It represents the state of the job, including job ID, job status (failure/success),
    error description (if any), and a list of events describing each step of the job.

    It also includes the output of the job: a string containing the YAML of the import plan.
    """

    job_id: str
    plan: str
    error: Optional[Dict] = None
    can_auto_apply: bool = False
    files_to_be_imported: List[str]
    job_status: Optional[str] = None
    runner_events: Optional[List[RunnerEvent]]

    def __init__(self, job_id: str) -> None:
        self.job_id = job_id
        self.runner_events = []
        self.files_to_be_imported = []


def _dump_plan_to_yaml(plan: Dict) -> str:
    import yaml

    yaml.Dumper.ignore_aliases = lambda *args: True
    return yaml.safe_dump(plan)


def _load_plan_from_yaml(plan: str) -> Dict:
    import yaml

    yaml.Dumper.ignore_aliases = lambda *args: True
    return yaml.safe_load(plan)


def _handle_table_create_plan_apply_log(log: RunnerInfo, state: TableCreatePlanApplyState) -> bool:
    if log.runner_event.apply_plan_done.error_message:
        state.error = log.runner_event.apply_plan_done.error_message
        state.job_status = JobStatus.failed
        _print_debug(f'Apply plan failed, error is: {state.error}')
        return True
    if log.runner_event.apply_plan_done.success:
        state.job_status = JobStatus.success
        _print_debug('Apply plan successful')
        return True
    return False


def _handle_table_create_plan_log(log: RunnerInfo, state: TableCreatePlanState) -> bool:
    runner_event = log.runner_event
    event_type = runner_event.WhichOneof('event')
    if event_type == 'job_completion':
        match runner_event.job_completion.WhichOneof('outcome'):
            case 'success':
                state.job_status = JobStatus.success
            case 'failure':
                state.job_status = JobStatus.failed
            case 'rejected':
                state.job_status = JobStatus.rejected
            case 'cancellation':
                state.job_status = JobStatus.cancelled
            case 'timeout':
                state.job_status = JobStatus.timeout
            case _:
                state.job_status = JobStatus.unknown
        return True

    if log.runner_event.table_create_plan_done_event.error_message:
        state.error = log.runner_event.import_plan_created.error_message
        state.job_status = JobStatus.failed
        _print_debug(f'Create import plan failed, error is: {state.error}')
        return True
    if log.runner_event.table_create_plan_done_event.success:
        table_create_plan_done_event = log.runner_event.table_create_plan_done_event

        state.job_status = JobStatus.success
        plan_yaml = table_create_plan_done_event.plan_as_yaml
        if plan_yaml is not None:
            state.plan = _load_plan_from_yaml(plan_yaml)

        state.can_auto_apply = table_create_plan_done_event.can_auto_apply
        state.files_to_be_imported = list(table_create_plan_done_event.files_to_be_imported)
        _print_debug('Table create plan success')
        return True
    return False


class _TableCreate(_OperationContainer):
    @_lifecycle
    def plan(
        self,
        search_uri: str,
        table_name: str,
        ref: str,
        replace: bool,
        namespace: Optional[str] = None,
        no_cache: bool = False,
        args: Optional[Dict[str, str]] = None,
        lifecycle_handler: _JobLifeCycleHandler = None,
    ) -> TableCreatePlanState:
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

        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)

        _print_debug(
            'Table create  plan',
            'search_uri',
            search_uri,
            'from_ref',
            ref,
            'table_name',
            table_name,
            'ref',
            ref,
            'no_cache',
            no_cache,
        )

        response: TableCreatePlanResponse = client_v2.TableCreatePlan(
            TableCreatePlanRequest(
                search_string=search_uri,
                default_namespace=namespace,
                trigger_run_opts={'cache': not no_cache},
                args=args or {},
                ref=ref,
                table=table_name,
                table_replace=replace,
            ),
            metadata=metadata_v2,
        )
        job_id = JobId(id=response.job_id)
        lifecycle_handler.register_job_id(job_id)
        _print_debug('table create plan job_id', response.job_id)
        log_stream: grpc.Call = client_v1.SubscribeLogs(job_id, metadata=metadata_v1)
        lifecycle_handler.register_log_stream(log_stream)
        state = TableCreatePlanState(job_id=job_id.id)
        for log in log_stream:
            if _handle_table_create_plan_log(log, state):
                break

        if state.can_auto_apply:
            _print_debug('table create plan job_id', response.job_id)
            self.apply(plan=state.plan)
        else:
            state.job_status = JobStatus.failed
            state.error = 'table creation successful but table has conflicts'

        return state

    @_lifecycle
    def apply(
        self,
        plan: Dict,
        args: Optional[Dict[str, str]] = None,
        no_cache: bool = False,
        lifecycle_handler: _JobLifeCycleHandler = None,
    ) -> TableCreatePlanApplyState:
        """
        Apply a Bauplan table import plan for a given branch.
        This is the equivalent of running through the CLI the ``bauplan import apply`` command.

        The user needs to pass a dict of the plan, as generated by the `plan` function defined in this module.

        This uses a _JobLifecyleHandler to handle timeout issues (future: KeyboardInterrupt)
        We register the job_id, log_stream, and flight_client with the lifecycle_handler
        so we can do a graceful shutdown behind the scenes upon TimeoutError exception.
        """
        # make sure the inviariants are met
        if not plan or not isinstance(plan, Dict):
            raise ValueError('`plan` str is required')

        yaml_as_string = _dump_plan_to_yaml(plan=plan)

        # this does basic validation for now
        client_v1, metadata_v1 = self._common.get_commander_and_metadata(args)
        client_v2, metadata_v2 = self._common.get_commander_v2_and_metadata(args)
        _print_debug(
            'Table create plan apply',
            'no_cache',
            no_cache,
        )
        response: TableCreatePlanApplyResponse = client_v2.TableCreatePlanApply(
            TableCreatePlanApplyRequest(
                plan_yaml=yaml_as_string,
                trigger_run_opts={'cache': not no_cache},
                args=args or {},
            ),
            metadata=metadata_v2,
        )
        job_id = JobId(id=response.job_id)
        lifecycle_handler.register_job_id(job_id)
        _print_debug('Apply import plan job_id', response.job_id)
        log_stream: grpc.Call = client_v1.SubscribeLogs(
            job_id,
            metadata=metadata_v1,
        )
        lifecycle_handler.register_log_stream(log_stream)
        state = TableCreatePlanApplyState(job_id=job_id.id)
        for log in log_stream:
            if _handle_table_create_plan_apply_log(log, state):
                break
        if not state.job_status:
            raise Exception(state.__repr__)
        return state
