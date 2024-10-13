from datetime import datetime, timedelta, timezone
from enum import Enum

from pydantic import Field, field_validator

from plurally.json_utils import dump_to_json_dict
from plurally.models.node import Node


class ScheduleUnit(str, Enum):
    MINUTES = "minutes"
    HOURS = "hours"
    DAYS = "days"
    WEEKS = "weeks"


class Schedule(Node):
    ICON = "schedule"
    IS_TRIGGER = True
    STATES = ("first",)

    class InitSchema(Node.InitSchema):
        """Schedule the execution of the flow on a time interval."""

        every: int = Field(
            1, description="The number of units to wait before executing the next block"
        )
        unit: ScheduleUnit = Field(
            ScheduleUnit.HOURS,
            description="The unit of time to wait before executing the next block",
        )
        first: datetime = Field(
            default_factory=lambda: datetime.now(timezone.utc).replace(tzinfo=None),
            title="First execution",
            examples=["2023-08-01 00:00:00"],
            format="date-time",
            description="The first time to execute the block. If not provided, the current time will be used.",
        )

        @field_validator("first")
        def check_first(cls, value):
            # if has tzinfo, convert to UTC no tzinfo
            if value.tzinfo is not None:
                value = value.astimezone(timezone.utc).replace(tzinfo=None)
            return value

    class InputSchema(Node.InputSchema):
        pass

    class OutputSchema(Node.OutputSchema):
        execution_time: datetime = Field(
            title="Execution Time",
            description="The time when the schedule is triggered.",
            format="date-time",
        )

    DESC = InitSchema.__doc__
    STATES = ("last_exec",)

    def __init__(self, init_inputs: InitSchema):
        self.every = init_inputs.every
        self.unit = init_inputs.unit
        self.last_exec = (
            init_inputs.first
            if init_inputs.first
            else datetime.now(tz=timezone.utc).replace(tzinfo=None)
        )
        super().__init__(init_inputs)

    @property
    def first(self):
        return self.last_exec

    @first.setter
    def first(self, value):
        self.last_exec = value

    @property
    def next(self):
        return self.last_exec + timedelta(**{self.unit.value: self.every})

    def should_run(self, now: datetime):
        return now >= self.next

    def forward(self, _: InputSchema):
        now = datetime.now(tz=timezone.utc).replace(tzinfo=None)
        if self.should_run(now):
            self.last_exec = now
            self.outputs = {"execution_time": now.isoformat()}
        else:
            self.outputs = None

    def serialize(self):
        serialized = super().serialize() | dump_to_json_dict(
            {"every": self.every, "unit": self.unit, "first": self.last_exec}
        )
        return serialized

    def _state(self):
        return {"last_exec": self.last_exec}
