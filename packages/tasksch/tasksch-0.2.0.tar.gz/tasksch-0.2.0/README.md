tsksch
------

A python pywin32 wrapper library for Windows Task Scheduler.


##### List All Scheduled Tasks

```python
from tasksch.scheduler import TaskService


with TaskService() as ts:
    root = ts.root_folder() 
    for folder in root.walk():
        print(f"DIR: {folder.path}")
        for task in folder.tasks():
            print(f"TSK: {task.path}") 

```

##### Create New Folder


```python
from tasksch.scheduler import TaskService

with TaskService() as ts:
    root = ts.root_folder()
    if not root.find("\\NEW FOLDER"):
        root.create_folder("\\NEW FOLDER")

```

##### Create New Task  


```python
from tasksch folder import TaskFolder
from tasksch.scheduler import TaskService
from tasksch.com import local_datetime
from tasksch.settings import duration, TaskInstancesPolicy
from tasksch.principle import TaskRunlevelType


with TaskService() as ts:
    root = ts.root_folder()

    folder = root.find(folder_name)
    if not folder:
        return

    existing_task = folder.find_task(task_name)
    if existing_task:
        return

    task = service.new_task()

    reg_info = task.registration_info
    reg_info.author = 'Mark Gemmill'
    reg_info.description = 'Test Task'

    action = task.actions.create_exec_action()
    action.path = r"C:\Users\username\execute.bat"
    action.working_directory = r"C:\Users\username"

    trigger = task.triggers.create_daily_trigger()
    trigger.start_boundary = local_datetime(2024, 1, 1, 5, 30) 
    trigger.days_interval = 1
    trigger.enabled = True

    settings = task.settings
    settings.enabled = True
    settings.hidden = True
    settings.multiple_instances = TaskInstancesPolicy.TASK_INSTANCES_IGNORE_NEW 
    settings.allow_demand_start = True
    settings.execution_time_limit = duration(hours=1, minutes=30)

    principal = task.principal
    principal.user_id = 'mark'
    principal.run_level = TaskRunlevelType.TASK_RUNLEVEL_HIGHEST

    folder.register_new_task_definition(
        task, 
        task_name, 
        'username',
        'Ckr1t',
    )

```
