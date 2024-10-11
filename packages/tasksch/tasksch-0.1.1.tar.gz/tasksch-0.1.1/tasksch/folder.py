import typing as t
from .com import ComObject, ComField 
from .task import RegisteredTask, TaskDefinition
from enum import Enum
from .principle import TaskLogonType

class TaskCreation(Enum):
    """
    TASK_CREATION: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/ne-taskschd-task_creation 

    """
    TASK_VALIDATE_ONLY = 0x1
    TASK_CREATE = 0x2
    TASK_UPDATE = 0x4
    TASK_CREATE_OR_UPDATE = 0x2 | 0x4
    TASK_DISABLE = 0x8
    TASK_DONT_ADD_PRINCIPAL_ACE = 0x10
    TASK_IGNORE_REGISTRATION_TRIGGERS = 0x20




class TaskFolder(ComObject):
    """
    ITaskFolder: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itaskfolder

    """

    name: str = ComField("Name")
    path: str = ComField("Path")

    def get_security_descriptor(self):
        return self.com_object.GetSecurityDescriptor()

    def create_folder(self, folder_name: str) -> "TaskFolder":
        """
        Win32 API calls for a sddl, but it isn't clear how to get such a value:

        HRESULT CreateFolder(
          [in]  BSTR        subFolderName,
          [in]  VARIANT     sddl,
          [out] ITaskFolder **ppFolder

        N.B. Calling CreateFolder without the sddl still works.

        """
        result = self.find(folder_name)
        if result:
            print(f"created folder exists: {result.path}")
            return result
        return TaskFolder(
            self.com_object.CreateFolder(
                folder_name,
            )
        )

    def delete_folder(self, folder_name: str):
        # TODO: likely need to check the folder exists before deleting
        self.com_object.DeleteFolder(folder_name, 0)

    def get_folder(self, folder_path: str) -> "TaskFolder":
        return TaskFolder(self.com_object.GetFolder(folder_path))

    def get_folders(self):
        # return TaskFolderCollection(self.com_object.GetFolders(0))
        for folder in self.com_object.GetFolders(0):
            yield TaskFolder(folder)

    def tasks(self):
        for task in self.com_object.GetTasks(0):
            yield RegisteredTask(task)

    def register_new_task_definition(self, task: TaskDefinition, path: str, user_id: str, password: str):
        self.com_object.RegisterTaskDefinition(
            path, 
            task.com_object, 
            TaskCreation.TASK_CREATE.value, 
            user_id, 
            password, 
            TaskLogonType.TASK_LOGON_NONE.value, 
        )

    def walk(self) -> t.Generator["TaskFolder", None, None]:
        for child in self.get_folders():
            yield child
            yield from child.walk()

    def find(self, path: str):
        for child in self.walk():
            child_path = child.path
            if not path.startswith(child_path):
                continue
            if child_path == path or child_path.endswith(path):
                return child

    def find_task(self, task_name: str) -> RegisteredTask | None:
        for task in self.tasks():
            if task.name == task_name:
                return task
