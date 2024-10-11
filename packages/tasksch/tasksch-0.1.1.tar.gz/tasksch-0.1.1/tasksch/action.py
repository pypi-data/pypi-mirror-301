import typing as t
from .com import ComObject, ComField, EnumComField
from enum import Enum


class TaskActionType(Enum):
    TASK_ACTION_EXEC = 0
    TASK_ACTION_COM_HANDLER = 5
    TASK_ACTION_SEND_EMAIL = 6
    TASK_ACTION_SHOW_MESSAGE = 7


class Action(ComObject):
    """
    IAction: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iaction

    """

    id: str = ComField("Id")
    type: TaskActionType = EnumComField("Type", TaskActionType)

    def display(self):
        return [
            ("", "ACTION"),
            ("id", self.id),
            ("type", self.type),
        ]


class ExecAction(Action):
    """
    IExecAction: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iexecaction

    """

    arguments: str = ComField("Arguments")
    path: str = ComField("Path")
    working_directory: str = ComField("WorkingDirectory")

    def display(self):
        value = super().display()
        value.append(("arguments", self.arguments))
        value.append(("path", self.path))
        value.append(("working_directory", self.working_directory))
        return value


ActionTypeFactory = {
    0: ExecAction,
}


class ActionCollection(ComObject):
    """
    IActionCollection: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iactioncollection

    """

    count: int = ComField("Count")

    def __iter__(self) -> t.Generator[Action, None, None]:
        for action in self.com_object:
            action_type = ActionTypeFactory.get(action.Type, Action)
            yield action_type(action)

    def create_exec_action(self) -> ExecAction:
        return ExecAction(self.com_object.Create(TaskActionType.TASK_ACTION_EXEC.value))

