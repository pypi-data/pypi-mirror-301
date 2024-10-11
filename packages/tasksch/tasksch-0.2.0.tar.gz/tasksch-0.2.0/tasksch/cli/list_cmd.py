import typing as t
from tasksch import TaskService
from rich.console import Console
from .filter import create_filter

console = Console()


class ShowArgs(t.Protocol):
    folders: bool
    folder_filter: str
    tasks: bool
    task_filter: str


def list_command(args: ShowArgs):
    """
    Print out each matching folder and task paths.

    """

    matching_folder_path = create_filter(args.folder_filter, default=args.folders)
    matching_task_path = create_filter(args.task_filter, default=args.tasks)

    with TaskService() as ts:
        root = ts.root_folder()
        for folder in root.walk():
            if args.folders or matching_folder_path(folder.path):
                console.print(f"[yellow]DIR: {folder.path}[/yellow]")
                for task in folder.tasks():
                    if args.tasks or matching_task_path(task.path):
                        console.print(
                            f"[green b]TSK:[/green b] [white b]{task.path}[/white b]"
                        )
