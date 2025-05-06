import argparse
import pathlib
import datetime
from typing import List
import tabulate
import sys


def perror(e: BaseException) -> None:
    print(f"ERROR: {e}")
    sys.exit(1)

def add_record(todo: str, todo_file_path: pathlib.Path) -> None:
    assert ";" not in todo, "Todo message cannot contain ;"

    if not todo_file_path.exists():
        with open(todo_file_path, "x") as file:
            file.close()
    
    try:
        with open(todo_file_path, "r") as file:
            lines = sum(1 for _ in file) + 1

        with open(todo_file_path, "a") as file:
            timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H:%M")
            full_message = f"{lines};{timestamp};{todo}\n"
            file.write(full_message)
    except FileNotFoundError as e:
        raise e


def nuke_todo(todo_file_path: pathlib.Path) -> None:
    assert todo_file_path.exists(), "Todo file does not exists"
    
    todo_file_path.unlink()


def list_todo(todo_file_path: pathlib.Path):

    assert todo_file_path.exists(), "Todo file does not exists"

    headers = ["Index", "Timestamp", "Todo"]
    lines = []


    with open(todo_file_path, "r") as file:
        for line in file:
            lines.append(line.split(";"))

    table = [headers] + lines 

    print(tabulate.tabulate(table, headers="firstrow"))


def remove_todo(indexes: List[int], todo_file_path: pathlib.Path) -> None:
    assert todo_file_path.exists(), "Todo file does not exists"

    with open(todo_file_path, "r") as file:
        lines = [line for line in file]

    with open(todo_file_path, "w") as file:
        for line in lines:
            line_index = int(line.split(";", 1)[0])
            if not line_index in indexes:
                file.write(line)


def update_record(index: int, new_todo: str, todo_file_path: pathlib.Path) -> None:
    assert todo_file_path.exists(), "Todo file does not exists"

    with open(todo_file_path, "r") as file:
        lines = [line for line in file]

    with open(todo_file_path, "w") as file:
        for line in lines:
            line_index = int(line.split(";", 1)[0])
            if line_index == index:
                timestamp = datetime.datetime.now().strftime("%d-%m-%YT%H:%M")
                new_line = f"{line_index};{timestamp};{new_todo}\n"
                file.write(new_line)
            else:
                file.write(line)


def main() -> None:
    main_parser = argparse.ArgumentParser()

    group = main_parser.add_mutually_exclusive_group()

    group.add_argument("--add", type=str, help="Add item to the end of todo list")
    group.add_argument("--rm", type=int, help="Remove item from todo list by index", nargs="*")
    group.add_argument("--update", help="Update item from todo list by index", nargs=2)
    group.add_argument("--nuke", action="store_true", help="Nuke the todo list file")
    group.add_argument("--list", action="store_true", help="List the todo list file")

    args = vars(main_parser.parse_args())

    _todo_file_path = pathlib.Path("~/Documents/todolist").expanduser()

    print("HELLOOO")

    if len(sys.argv) == 1:
        list_todo(_todo_file_path)
    else:
        if args["list"]:
            list_todo(_todo_file_path)
        elif args["nuke"]:
            try:
                nuke_todo(_todo_file_path)
                print("Nuked todo file")
            except AssertionError as e: perror(e)
        elif args["add"] is not None:
            add_record(args["add"], _todo_file_path)
        elif args["rm"] is not None:
            remove_todo(args["rm"], _todo_file_path)
        elif args["update"] is not None:
            update_record(int(args["update"][0]), args["update"][1], _todo_file_path)
