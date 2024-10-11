import typing as t
from rich.console import Console
from rich.table import Table
from tasksch import TaskService
from tasksch import RegisteredTask
from tasksch import Action
from tasksch import TaskTrigger
from .filter import create_filter


console = Console()


class DisplayArgs(t.Protocol):
    folder_filter: str
    task_filter: str


def display_command(args: object):
    matching_folder_path = create_filter(args.folder_filter, default=True)
    matching_task_path = create_filter(args.task_filter, default=False)

    with TaskService() as ts:
        root = ts.root_folder()
        for folder in root.walk():
            if matching_folder_path(folder.path):
                for task in folder.tasks(include_hidden=True):
                    print(task.path)
                    if matching_task_path(task.path):
                        console.print(
                            f"[green b]TSK:[/green b] [white b]{task.path}[/white b]"
                        )
                        print_task_definition(task)


def yes_no(value: bool) -> str:
    return "YES" if value is True else "NO"


def stringify(value: t.Any) -> str:
    if value is None:
        return ""
    return str(value)


def print_task_definition(task: RegisteredTask):
    """
    General Tab
        Name:
        Location:
        Author:
        Description:
        Hidden:
        Configure For:
        Security Options:
            When running the task, use the follow user account:
            Run only when user is logged in:
            Run whether user is logged in or not:
            Do not store password:
            Run with highest privileges: bool

    Triggers Tab
        Begin the task: Task Type
        Settings:
            Type: enum
            Start: datetime
        Advanced Settings:
            Delay task for up to (random delay): e.g. 1 hour
            Repeat task every: e.g. 5 minutes
                For a duration of: e.g. 1 day
            Stop running tasks at end of repetition duraction: bool
            Stop task if it runs longer than: e.g. 1 hour
            Expire: datetime
            Enabled: bool

    Actions Tab
        Action: Action Type
        Settings:
            Program/Script: path
            Add Arguments: str
            Start in: path

    Conditions Tab
        Idle
            Start the task only if the computer is idle for: e.g. 10 minutes
                Wait for idle for: e.g. 1 hour
                Stop if the computer ceases to be idle: bool
                    Restart if idle state resumes: bool
        Power
            Start the task only if computer on AC power: bool
                Stop the task if computer switches to batter: bool
            Wake the computer to run this task: bool
        Network
            Start only if the following network connection is available: bool
            connection: ???

    Settings Tab
        Allow task to be  run on demand: bool
        Run task as soon as possible after scheduled start is missed: bool
        If task fails restart every: e.g. 5 minutes
            Attempt to restart up to: x times (int)
        Stop the task if it runs longer than: e.g. 1 hour
        If the running task does not end when requested, force it to stop: bool
        If the task is not scheduled to run again, delete it after: e.g. 3 days
        If the task is already running, then the following rule applies: RuleType

    """
    table = Table(show_header=False)
    table.add_column("", max_width=30, style="bold bright_white")
    table.add_column("")
    display_general_tab(table, task)
    display_settings_tab(table, task)
    display_triggers(table, task)
    display_actions(table, task)
    console.print(table)


def display_general_tab(table: Table, task: RegisteredTask):
    dtn = task.definition

    # General Tab
    table.add_section()
    table.add_row("[yellow]GENERAL[/yellow]")
    #     Name:
    table.add_row("Name", stringify(task.name))
    #     Location:
    table.add_row("Location", stringify(task.path))
    #     Author:
    table.add_row("Author", stringify(dtn.registration_info.author))
    #     Description:
    table.add_row("Description", stringify(dtn.registration_info.description))
    #     Hidden:
    table.add_section()
    #     Security Options:
    #         When running the task, use the follow user account:
    table.add_row("User account", stringify(dtn.principal.user_id))
    table.add_row("???", stringify(dtn.principal.logon_type.name))
    #         Run only when user is logged in:
    #         Run whether user is logged in or not:
    table.add_row("Run when", "cannot find setting")
    #         Do not store password:
    #         Run with highest privileges: bool
    table.add_row(
        "Run with highest priviledges",
        yes_no(dtn.principal.run_with_highest_privileges),
    )
    table.add_section()
    table.add_row("Hidden", yes_no(dtn.settings.hidden))
    #     Configure For:
    #     ??????
    table.add_row("Configure For", stringify(dtn.settings.compatibility.name))


def display_settings_tab(table: Table, task: RegisteredTask):
    dtn = task.definition
    # Settings Tab
    table.add_section()
    table.add_row("[yellow]SETTINGS[/yellow]")
    #     Allow task to be  run on demand: bool
    table.add_row("Run on demand?", yes_no(dtn.settings.allow_demand_start))
    #     Run task as soon as possible after scheduled start is missed: bool
    table.add_row("Run after missed start?", yes_no(dtn.settings.start_when_available))
    #     If task fails restart every: e.g. 5 minutes
    table.add_row("On fail, restart every", stringify(dtn.settings.restart_interval))
    #         Attempt to restart up to: x times (int)
    table.add_row("Attempt restart up to", f"{dtn.settings.restart_count} times")
    #     Stop the task if it runs longer than: e.g. 1 hour
    table.add_row(
        "Stop if runs longer than", stringify(dtn.settings.execution_time_limit)
    )
    #     If the running task does not end when requested, force it to stop: bool
    table.add_row("Force to stop if running longer than requested", "????")
    #     If the task is not scheduled to run again, delete it after: e.g. 3 days
    table.add_row(
        "If not scheduled, delete after",
        stringify(dtn.settings.delete_expired_task_after),
    )
    #     If the task is already running, then the following rule applies: RuleType
    table.add_row(
        "If task already running, then", stringify(dtn.settings.multiple_instances.name)
    )


def display_triggers(table: Table, task: RegisteredTask):
    for trigger in task.definition.triggers:
        display_trigger(table, trigger)


def display_trigger(table: Table, trigger: TaskTrigger):
    # Triggers Tab
    table.add_section()
    table.add_row("[yellow]TRIGGER[/yellow]")
    #     Begin the task: Task Type
    table.add_row("Trigger type", "????")
    #     Settings:
    table.add_row("[bright_black]Settings[/bright_black]", "")
    #         Type: enum
    table.add_row("Trigger type", stringify(trigger.type.name))
    #         Start: datetime
    table.add_row("Start", stringify(trigger.start_boundary))
    #     Advanced Settings:
    table.add_row("[bright_black]Advanced[/bright_black]")
    #         Delay task for up to (random delay): e.g. 1 hour
    table.add_row("Delay task up to", "????")
    #         Repeat task every: e.g. 5 minutes
    #             For a duration of: e.g. 1 day
    #         Stop running tasks at end of repetition duraction: bool
    #         Stop task if it runs longer than: e.g. 1 hour
    table.add_row("Stop task after", stringify(trigger.execution_time_limit))
    #         Expire: datetime
    table.add_row("Expire", stringify(trigger.end_boundary))
    #         Enabled: bool
    table.add_row("Enabled", yes_no(trigger.enabled))


def display_actions(table: Table, task: RegisteredTask):
    for action in task.definition.actions:
        display_action(table, action)


def display_action(table: Table, action: Action):
    # Actions Tab
    table.add_section()
    table.add_row("[yellow]ACTION[/yellow]")
    #     Action: Action Type
    table.add_row("Action Type", stringify(action.type.name))
    #     Settings:
    #         Program/Script: path
    #         Add Arguments: str
    #         Start in: path
