from .cli import create_cli_parser


def run():
    cli_parser = create_cli_parser()
    cli_args = cli_parser.parse_args()
    cli_args.func(cli_args)
