# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

from typing import Dict, List, Union, Optional
from typing_extensions import Literal, TypeAlias

from .._compat import PYDANTIC_V2
from .._models import BaseModel
from .unary_condition import UnaryCondition
from .node_item_output import NodeItemOutput
from .plan_config_output import PlanConfigOutput
from .workflow_config_output import WorkflowConfigOutput
from .compound_condition_output import CompoundConditionOutput

__all__ = [
    "ConfigRetrieveResponse",
    "StateMachineConfigOutput",
    "StateMachineConfigOutputMachine",
    "StateMachineConfigOutputMachineNextNode",
    "StateMachineConfigOutputMachineNextNodeCase",
    "StateMachineConfigOutputMachineNextNodeCaseCondition",
]

StateMachineConfigOutputMachineNextNodeCaseCondition: TypeAlias = Union[UnaryCondition, CompoundConditionOutput]


class StateMachineConfigOutputMachineNextNodeCase(BaseModel):
    condition: StateMachineConfigOutputMachineNextNodeCaseCondition
    """Representation of a boolean function with a single input e.g.

    the condition specified by input_name: x operator: 'contains' ref_value: 'c'
    would evaluate to True if x == 'cat' Operators are defined in the constant
    function store CONDITIONAL_ACTION_MAP
    """

    value: str


class StateMachineConfigOutputMachineNextNode(BaseModel):
    default: str

    cases: Optional[List[StateMachineConfigOutputMachineNextNodeCase]] = None


class StateMachineConfigOutputMachine(BaseModel):
    next_node: StateMachineConfigOutputMachineNextNode
    """A switch statement for state machines to select the next state to execute."""

    workflow_config: "WorkflowConfigOutput"

    write_to_state: Optional[Dict[str, str]] = None


class StateMachineConfigOutput(BaseModel):
    machine: Dict[str, StateMachineConfigOutputMachine]

    starting_node: str

    id: Optional[str] = None

    account_id: Optional[str] = None

    application_variant_id: Optional[str] = None

    base_url: Optional[str] = None

    concurrency_default: Optional[bool] = None

    datasets: Optional[List[object]] = None

    done_string: Optional[str] = None

    egp_api_key_override: Optional[str] = None

    egp_ui_evaluation: Optional[object] = None

    evaluations: Optional[List["NodeItemOutput"]] = None

    final_output_nodes: Optional[List[str]] = None

    initial_state: Optional[object] = None

    nodes_to_log: Union[str, List[str], None] = None

    num_workers: Optional[int] = None

    streaming_nodes: Optional[List[str]] = None

    type: Optional[Literal["workflow", "plan", "state_machine"]] = None


ConfigRetrieveResponse: TypeAlias = Union[PlanConfigOutput, WorkflowConfigOutput, StateMachineConfigOutput]

if PYDANTIC_V2:
    StateMachineConfigOutput.model_rebuild()
    StateMachineConfigOutputMachine.model_rebuild()
    StateMachineConfigOutputMachineNextNode.model_rebuild()
    StateMachineConfigOutputMachineNextNodeCase.model_rebuild()
else:
    StateMachineConfigOutput.update_forward_refs()  # type: ignore
    StateMachineConfigOutputMachine.update_forward_refs()  # type: ignore
    StateMachineConfigOutputMachineNextNode.update_forward_refs()  # type: ignore
    StateMachineConfigOutputMachineNextNodeCase.update_forward_refs()  # type: ignore
