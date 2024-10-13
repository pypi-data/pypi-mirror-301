from argparse import ArgumentParser


def _build_global_option_parser() -> ArgumentParser:
    "Parent parser to define optoins used for ALL commands"
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--aws-access-key", nargs="?", action="store")
    parser.add_argument("--aws-secret-key", nargs="?", action="store")
    parser.add_argument("--aws-bucket-name", nargs="?", action="store")
    parser.add_argument(
        "-y",
        dest="default_yes",
        action="store_true",
        help="Apply yes by default to all inputs",
    )
    return parser


def _build_file_location_parser() -> ArgumentParser:
    parser = ArgumentParser(add_help=False)
    parser.add_argument("--remote-file-path", nargs="?")
    parser.add_argument("--dest-file-path", nargs="?")
    return parser


def parse_args():
    all_option_parser = _build_global_option_parser()
    file_option_parser = _build_file_location_parser()

    # This creates 'mutually' exclusive parsers
    parser = ArgumentParser(prog="Orchkestr8 ML train runner")
    subparsers = parser.add_subparsers(dest="command", help="Invocation commands")
    # This creates 'mutually' exclusive parsers

    train_parser = subparsers.add_parser(
        "train", help="Runs the training logic only", parents=[all_option_parser]
    )
    train_parser.add_argument(
        "model_module",
        action="store",
        help="The module that contains the model to run. Module MUST have a `run` method defined",
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Runs the data update and training logic",
        parents=[all_option_parser, file_option_parser],
    )
    run_parser.add_argument(
        "--model-module",
        action="store",
        help="The module that contains the model to run. Module MUST have a `run` method defined",
    )
    run_parser.add_argument(
        "--remote_file_path", help="Where to direct Orkestr8 to pull the file from"
    )
    run_parser.add_argument(
        "--dest_file_path", help="Where to direct Orkestr8 to write file path"
    )

    update_parser = subparsers.add_parser(
        "update", help="Runs the data update function.", parents=[all_option_parser]
    )
    update_parser.add_argument(
        "remote_file_path", help="Where to direct Orkestr8 to pull the file from"
    )
    update_parser.add_argument(
        "dest_file_path", help="Where to direct Orkestr8 to write file path"
    )

    # ArgumentParser("stop", description="Writes to a file", parents=[parser])
    return parser.parse_args()
