from datetime import datetime
import typing as t
from .com import ComObject, ComField, DateTimeComField, EnumComField
from enum import Enum


class TriggerType(Enum):
    TASK_TRIGGER_EVENT = 0
    TASK_TRIGGER_TIME = 1
    TASK_TRIGGER_DAILY = 2
    TASK_TRIGGER_WEEKLY = 3
    TASK_TRIGGER_MONTHLY = 4
    TASK_TRIGGER_MONTHLYDOW = 5
    TASK_TRIGGER_IDLE = 6
    TASK_TRIGGER_REGISTRATION = 7
    TASK_TRIGGER_BOOT = 8
    TASK_TRIGGER_LOGON = 9
    TASK_TRIGGER_SESSION_STATE_CHANGE = 11
    TASK_TRIGGER_CUSTOM_TRIGGER_01 = 12


class RepetitionPattern(ComObject):
    """
    IRepetitionPattern: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-irepetitionpattern

    """

    duration: str = ComField("Duration")
    interval: str = ComField("Interval")
    stop_at_duration_end: bool = ComField("StopAtDurationEnd")

    def display(self):
        return ", ".join(
            [
                f"duration: {self.duration}",
                f"interval: {self.interval}",
                f"stop_at_duration_end: {self.stop_at_duration_end}",
            ]
        )


class TaskTrigger(ComObject):
    """
    ITrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itrigger

    """

    id: str = ComField("Id")
    type: TriggerType = EnumComField("Type", TriggerType)
    enabled: bool = ComField("Enabled")
    start_boundary: datetime = DateTimeComField("StartBoundary")
    end_boundary: datetime = DateTimeComField("EndBoundary")
    execution_time_limit: str = ComField("ExecutionTimeLimit")
    repetition: RepetitionPattern = ComField("Repetition", RepetitionPattern)

    def display(self):
        return [
            ("", "TRIGGER"),
            ("id", self.id),
            ("type", self.type),
            ("enabled", self.enabled),
            ("start boundary", self.start_boundary),
            ("end boundary", self.end_boundary),
            ("execute time limit", self.execution_time_limit),
            ("repetition", self.repetition.display()),
        ]


class DailyTaskTrigger(TaskTrigger):
    """
    IDailyTrigger: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-idailytrigger

    """

    days_interval: int = ComField("DaysInterval")
    random_delay: str = ComField("RandomDelay")

    def display(self):
        values = super().display()
        values.append(("days interval", self.days_interval))
        values.append(("random delay", self.random_delay))
        print("returning...")
        return values


TriggerTypeFactory = {
    2: DailyTaskTrigger,
}


class TaskTriggerCollection(ComObject):
    """
    ITriggerCollection: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itriggercollection

    """

    count: int = ComField("Count")

    def create_daily_trigger(self) -> DailyTaskTrigger:
        return DailyTaskTrigger(self.com_object.Create(TriggerType.TASK_TRIGGER_DAILY.value))

    def __iter__(self) -> t.Generator[TaskTrigger, t.Any, t.Any]:
        for trigger in self.com_object:
            task_type = TriggerTypeFactory.get(trigger.Type, TaskTrigger)
            yield task_type(trigger)
