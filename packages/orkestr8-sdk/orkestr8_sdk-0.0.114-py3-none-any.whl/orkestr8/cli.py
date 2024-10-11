from argparse import ArgumentParser


def parse_args():
    parser = ArgumentParser(prog="Orchkestr8 ML train runner", add_help=False)
    parser.add_argument("--aws-access-key", nargs="?", action="store")
    parser.add_argument("--aws-secret-key", nargs="?", action="store")
    parser.add_argument("--aws-bucket-name", nargs="?", action="store")
    parser.add_argument("--project-location", nargs="?", action="store")
    parser.add_argument(
        "-y",
        dest="default_yes",
        action="store_true",
        help="Apply yes by default to all inputs",
    )

    subparsers = parser.add_subparsers(dest="command", help="Invocation commands")
    # This creates 'mutually' exclusive parsers
    train_parser = subparsers.add_parser(
        "train", help="Runs the training logic only", parents=[parser]
    )
    train_parser.add_argument(
        "model_module",
        action="store",
        help="The module that contains the model to run. Module MUST have a `run` method defined",
    )
    run_parser = subparsers.add_parser(
        "run", help="Runs the data update and training logic", parents=[parser]
    )
    run_parser.add_argument(
        "--model_module",
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
        "update", help="Runs the data update function.", parents=[parser]
    )
    update_parser.add_argument(
        "remote_file_path", help="Where to direct Orkestr8 to pull the file from"
    )
    update_parser.add_argument(
        "dest_file_path", help="Where to direct Orkestr8 to write file path"
    )

    subparsers.add_parser("stop", help="Writes to a file", parents=[parser])
    return parser.parse_args()
