import typing as t
from .com import ComObject, ComField, EnumComField
from enum import Enum


class TaskCompatibility(Enum):
    """
    TASK_COMPATIBILITY: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_compatibility

    """

    TASK_COMPATIBILITY_AT = 0
    TASK_COMPATIBILITY_V1 = 1
    TASK_COMPATIBILITY_V2 = 2
    TASK_COMPATIBILITY_V2_1 = 3
    TASK_COMPATIBILITY_V2_2 = 4
    TASK_COMPATIBILITY_V2_3 = 5
    TASK_COMPATIBILITY_V2_4 = 6


class TaskInstancesPolicy(Enum):
    """
    TASK_INSTANCES_POLICY: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_instances_policy

    """

    TASK_INSTANCES_PARALLEL = 0
    TASK_INSTANCES_QUEUE = 1
    TASK_INSTANCES_IGNORE_NEW = 2
    TASK_INSTANCES_STOP_EXISTING = 3


# time limit format:
# PnYnMnDTnHnMnS 
#  PT5M = 5 minutes
#  pT0S = run indefinitely
#  P3DT3H15M = 3 days, 3 hours and 15 minutes
def duration(years: int=None, months: int=None, days: int=None, hours: int=None, minutes: int=None, seconds: int=None) -> str:
    content = ['P']
    if years and years > 0:
        content.append(f"{years}Y")
    if months and months > 0:
        content.append(f"{months}M")
    if days and days > 0:
        content.append(f"{days}D")
    content.append("T")
    if hours and hours > 0:
        content.append(f"{hours}H")
    if minutes and minutes > 0:
        content.append(f"{minutes}M")
    if seconds:
        content.append(f"{seconds}S")
    return "".join(content)

class TaskSettings(ComObject):
    """
    ITaskSettings: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itasksettings

    """

    allow_demand_start: bool = ComField("AllowDemandStart")
    allow_hard_terminate: bool = ComField("AllowHardTerminate")
    compatibility: TaskCompatibility = EnumComField("Compatibility", TaskCompatibility)
    deleted_expired_task_after: str = ComField("DeletedExpiredTaskAfter")
    disallow_start_if_on_batteries: bool = ComField("DisallowStartIfOnBatteries")
    enabled: bool = ComField("Enabled")
    execution_time_limit: str = ComField("ExecutionTimeLimit")
    hidden: bool = ComField("Hidden")
    # idle_settings: str = ComField("IdleSettings")
    multiple_instances: TaskInstancesPolicy = EnumComField(
        "MultipleInstances", TaskInstancesPolicy
    )
    # network_settings: bool = ComField("NetworkSettings")
    priority: int = ComField("Priority")
    restart_count: int = ComField("RestartCount")
    restart_interval: str = ComField("RestartInterval")
    run_only_if_idle: bool = ComField("RunOnlyIfIdle")
    run_only_if_network_available: bool = ComField("RunOnlyIfNetworkAvailable")
    start_when_available: bool = ComField("StartWhenAvailable")
    stop_if_going_on_batteries: bool = ComField("StopIfGoingOnBatteries")
    wake_to_run: bool = ComField("WakeToRun")
    xml_text: str = ComField("XmlText")

    # def xml_text(self) -> str:
    #     return self.com_object.XmlText()
