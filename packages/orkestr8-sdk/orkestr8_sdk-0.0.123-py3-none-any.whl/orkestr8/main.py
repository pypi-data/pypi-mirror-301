import logging
import os
from enum import Enum
from typing import List

import dotenv

from orkestr8.cli import parse_args
from orkestr8.commands.base import Command
from orkestr8.commands.train import TrainCommand
from orkestr8.commands.update import UpdateCommand

logger = logging.getLogger()
logging.basicConfig(level=logging.INFO)


class Dispatch(Enum):
    TRAIN = "train"
    RUN = "run"
    UPDATE = "update"


dotenv.load_dotenv()


def handle_env_vars(args):
    assign_env_variables(args)
    check_env_variables(args)


def assign_env_variables(args):
    os.environ["DEST_FILE_PATH"] = args.dest_file_path
    os.environ["REMOTE_FILE_PATH"] = args.remote_file_path


def check_env_variables(args):
    required_variables = ["AWS_ACCESS_KEY", "AWS_SECRET_KEY", "AWS_BUCKET_NAME"]

    for v in required_variables:
        if not os.environ.get(v):
            attr = getattr(args, v.lower(), None)
            if attr is None:
                raise RuntimeError(f"Improper configuration. '{v}' is not set")
            else:
                os.environ[v] = attr


def run(args) -> None:
    commands_to_run: List[Command] = []
    command = Dispatch(args.command)
    if command == Dispatch.TRAIN:
        commands_to_run.append(TrainCommand(args))
    elif command == Dispatch.UPDATE:
        commands_to_run.append(UpdateCommand(args))
    elif command == Dispatch.RUN:
        commands_to_run.append(UpdateCommand(args))
        commands_to_run.append(TrainCommand(args))
    for c in commands_to_run:
        c.run()


def main():
    args = parse_args()
    logger.info(args)
    handle_env_vars(args)
    run(args)


if __name__ == "__main__":
    main()
