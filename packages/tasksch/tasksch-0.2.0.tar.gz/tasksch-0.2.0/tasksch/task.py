from .com import ComObject, ComField
from .trigger import TaskTriggerCollection
from .action import ActionCollection
from .settings import TaskSettings
from .principle import Principle


class TaskRegistrationInfo(ComObject):
    """
    IRegistrationInfo: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iregistrationinfo

    """

    author: str = ComField("Author")
    date: str = ComField("Date")
    description: str = ComField("Description")
    documentation: str = ComField("Documentation")

    @property
    def security_descriptor(self):
        return self.com_object.SecurityDescriptor


class TaskDefinition(ComObject):
    """
    ITaskDefinition: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itaskdefinition

    """

    registration_info: TaskRegistrationInfo = ComField(
        "RegistrationInfo", TaskRegistrationInfo
    )
    principal: Principle = ComField("Principal", Principle)
    triggers: TaskTriggerCollection = ComField("Triggers", TaskTriggerCollection)
    actions: ActionCollection = ComField("Actions", ActionCollection)
    settings: TaskSettings = ComField("Settings", TaskSettings)
    data: str = ComField("Data")
    xml_text: str = ComField("XmlText")


class RegisteredTask(ComObject):
    """
    IRegisteredTask: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-iregisteredtask

    """

    name: str = ComField("Name")
    path: str = ComField("Path")
    enabled: bool = ComField("Enabled")
    last_runtime: str = ComField("LastRunTime")
    definition: TaskDefinition = ComField("Definition", TaskDefinition)
