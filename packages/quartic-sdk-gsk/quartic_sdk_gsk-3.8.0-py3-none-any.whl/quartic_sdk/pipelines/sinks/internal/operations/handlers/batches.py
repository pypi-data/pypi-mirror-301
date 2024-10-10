from typing import Tuple, Type
from quartic_sdk.pipelines.sinks.internal.operations.handlers.base import (
    GQLOperationHandler,
)
from quartic_sdk.pipelines.sinks.internal.operations.operations import (
    ProcedureStepBatchCreate,
    ProcedureStepBatchDelete,
    ProcedureStepBatchUpdate,
)

BATCH_CREATE_MUTATION = """
mutation createBatch(
    $batchName: String!,
    $startTime: CustomDateTime!,
    $procedureStepComponent: ID!,
    $sequential: Boolean,
    $stopTime: CustomDateTime,
    $batchType: ProcedureStepBatchBatchTypeEnumCreate
) {
    ProcedurestepbatchCreate(
        newProcedurestepbatch: {
            batchName: $batchName,
            startTime: $startTime,
            procedureStepComponent: $procedureStepComponent,
            sequential: $sequential,
            stopTime: $stopTime,
            batchType: $batchType
        }
    ) {
        ok
        errors {
            field
            messages
        }
    }
}
"""
BATCH_DELETE_MUTATION = """
mutation deleteBatch($id: ID!) {
    ProcedurestepbatchDelete(id: $id) {
        ok
        errors {
            field
            messages
        }
    }
}
"""
BATCH_UPDATE_MUTATION = """
mutation updateBatch(
    $id: ID!,
    $batchName: String!,
    $startTime: CustomDateTime!,
    $procedureStepComponent: ID!,
    $sequential: Boolean,
    $stopTime: CustomDateTime,
    $batchType: ProcedureStepBatchBatchTypeEnumUpdate
) {
    ProcedurestepbatchUpdate(
        updateProcedurestepbatch: {
            id: $id,
            batchName: $batchName,
            startTime: $startTime,
            procedureStepComponent: $procedureStepComponent,
            sequential: $sequential,
            stopTime: $stopTime,
            batchType: $batchType
        }
    ) {
        ok
        errors {
            field
            messages
        }
    }
}
"""


class ProcedureStepBatchCreateHandler(GQLOperationHandler[ProcedureStepBatchCreate]):
    @classmethod
    def get_optype(cls):
        return ProcedureStepBatchCreate

    def get_success_field(self):
        return "data.ProcedurestepbatchCreate.ok"

    def get_query(self, op: ProcedureStepBatchCreate):
        return BATCH_CREATE_MUTATION, {
            "batchName": op.batch_name,
            "batchType": op.batch_type,
            "procedureStepComponent": op.procedure_step_component,
            "sequential": op.sequential,
            "startTime": op.start_time,
            "stopTime": op.stop_time,
        }


class ProcedureStepBatchDeleteHandler(GQLOperationHandler[ProcedureStepBatchDelete]):
    @classmethod
    def get_optype(cls):
        return ProcedureStepBatchDelete

    def get_success_field(self):
        return "data.ProcedurestepbatchDelete.ok"

    def get_query(self, op: ProcedureStepBatchDelete):
        return BATCH_DELETE_MUTATION, {"id": op.id}


class ProcedureStepBatchUpdateHandler(GQLOperationHandler[ProcedureStepBatchUpdate]):
    @classmethod
    def get_optype(cls):
        return ProcedureStepBatchUpdate

    def get_success_field(self):
        return "data.ProcedurestepbatchUpdate.ok"

    def get_query(self, op: ProcedureStepBatchCreate):
        return BATCH_UPDATE_MUTATION, {
            "id": op.id,
            "batchName": op.batch_name,
            "batchType": op.batch_type,
            "procedureStepComponent": op.procedure_step_component,
            "sequential": op.sequential,
            "startTime": op.start_time,
            "stopTime": op.stop_time,
        }
