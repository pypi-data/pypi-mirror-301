"""Definitions for workflow statuses and nodes"""

__all__ = ["WorkflowStatus", "NodeInfo", "WorkflowRunAttemptData", "NodeStatus"]

import datetime
from enum import Enum
from typing import Optional
from pydantic import BaseModel, Field, computed_field

from ..constants import TASK_MAIN_ID, STEP_MAIN_ID


# Unfortunately, we cannot subclass a subclass of a Enum, so we must duplicate
# our statues. At some point, these statuses will likely diverge anyways.


class WorkflowStatus(Enum):
    """The status of a workflow run"""

    RUNNING = "RUNNING"  # OPEN
    SUSPENDED = "SUSPENDED"  # OPEN
    FAILED = "FAILED"  # CLOSED
    CANCELLED = "CANCELLED"  # CLOSED
    COMPLETED = "COMPLETED"  # CLOSED
    TERMINATED = "TERMINATED"  # CLOSED
    TIMED_OUT = "TIMED_OUT"  # CLOSED
    CONTINUED_AS_NEW = "CONTINUED_AS_NEW"  # CLOSED


class NodeStatus(Enum):
    """The status of a node within a workflow or workflow run"""

    RUNNING = "RUNNING"  # OPEN
    SUSPENDED = "SUSPENDED"  # OPEN
    FAILED = "FAILED"  # CLOSED
    CANCELLED = "CANCELLED"  # CLOSED
    COMPLETED = "COMPLETED"  # CLOSED
    TERMINATED = "TERMINATED"  # CLOSED
    TIMED_OUT = "TIMED_OUT"  # CLOSED
    CONTINUED_AS_NEW = "CONTINUED_AS_NEW"  # CLOSED


class NodeInfo(BaseModel):
    """
    Each task or step in a workflow run is a "node". This keeps track of which
    node the workflow run is in.
    """

    task: str = Field(description="The task that the node is in", default=TASK_MAIN_ID)
    step: str = Field(description="The step that the node is in", default=STEP_MAIN_ID)
    status: Optional[NodeStatus] = Field(
        description="The status of the node", default=NodeStatus.RUNNING
    )

    @computed_field  # type: ignore[prop-decorator]
    @property
    def id(self) -> str:
        """The node's identifier within the workflow run"""
        return f"{self.task}/{self.step}"


class WorkflowRunAttemptData(BaseModel):
    """Data about a workflow run attempt"""

    attempt_id: str
    workflow_id: str
    workflow_run_id: str
    created_at: datetime.datetime = Field(default_factory=datetime.datetime.utcnow)
