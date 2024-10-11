"""
mstask.h
https://learn.microsoft.com/en-us/windows/win32/api/mstask/

taskschd.h 
https://learn.microsoft.com/en-us/windows/win32/api/taskschd/

"""
import re
import win32com.client
from .folder import TaskFolder
from .com import ComField
from .task import TaskDefinition


class TaskService:
    """
    ITaskService: https://learn.microsoft.com/en-us/windows/win32/api/taskschd/nn-taskschd-itaskservice

    """

    def __init__(self):
        self.com_object = win32com.client.Dispatch("Schedule.Service")

    user: str = ComField("CurrentUser")
    server: str = ComField("TargetServer")
    connected: bool = ComField("Connected")

    def open(self):
        self.com_object.Connect()

    def get_folder(self, folder_name: str):
        result = self.com_object.GetFolder(folder_name)
        return TaskFolder(result)

    def root_folder(self):
        return self.get_folder("\\")

    def new_task(self) -> TaskDefinition:
        return TaskDefinition(self.com_object.NewTask(0))

    def registered_tasks(self, folder_path_filter=None, task_filter=None):
        task_rx = re.compile(task_filter or ".*")
        for folder in self.root_folder().walk():
            if folder_path_filter and not folder.path.startswith(folder_path_filter):
                continue
            for task in folder.tasks():
                if task_filter:
                    if not task_rx.match(task.name):
                        continue
                yield task

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
