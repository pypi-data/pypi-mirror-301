import typing as t
from .com import ComObject, ComField, EnumComField
from enum import Enum


class TaskLogonType(Enum):
    """
    TASK_LOGON_TYPE: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_logon_type

    """

    TASK_LOGON_NONE = 0
    TASK_LOGON_PASSWORD = 1
    TASK_LOGON_S4U = 2
    TASK_LOGON_INTERACTIVE_TOKEN = 3
    TASK_LOGON_GROUP = 4
    TASK_LOGON_SERVICE_ACCOUNT = 5
    TASK_LOGON_INTERACTIVE_TOKEN_OR_PASSWORD = 6


class TaskRunlevelType(Enum):
    """
    TASK_RUNLEVEL_TYPE: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_runlevel_type

    """

    TASK_RUNLEVEL_LUA = 0
    TASK_RUNLEVEL_HIGHEST = 1


class Principle(ComObject):
    """
    IPrincipal: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iprincipal

    """

    display_name: str = ComField("DisplayName")
    group_id: str = ComField("GroupId")
    id: str = ComField("Id")
    logon_type: TaskLogonType = EnumComField("LogonType", TaskLogonType)
    run_level: TaskRunlevelType = EnumComField("RunLevel", TaskRunlevelType)
    user_id: str = ComField("UserId")

    def display(self):
        return [
            ("DisplayName", self.display_name),
            ("GroupId", self.group_id),
            ("Id", self.id),
            ("LogonType", self.logon_type),
            ("RunLevel", self.run_level),
            ("UserId", self.user_id),
        ]
