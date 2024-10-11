import argparse
from .display_cmd import display_command
from .list_cmd import list_command


def create_cli_parser() -> argparse.ArgumentParser:
    program = argparse.ArgumentParser(prog="tasksch")
    commands = program.add_subparsers()

    list_cmd = commands.add_parser("list")
    list_cmd.set_defaults(func=list_command)

    folder_group = list_cmd.add_mutually_exclusive_group()
    folder_group.add_argument("--folders", action="store_true")
    folder_group.add_argument("--folder-filter")

    task_group = list_cmd.add_mutually_exclusive_group()
    task_group.add_argument("--tasks", action="store_true")
    task_group.add_argument("--task-filter")

    display_cmd = commands.add_parser("display")
    display_cmd.set_defaults(func=display_command)
    display_cmd.add_argument("--folder-filter")
    display_cmd.add_argument("--task-filter")

    return program
