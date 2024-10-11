from argparse import ArgumentParser

from furiosa_llm.cli.serve import add_serve_args


def main():
    parser = ArgumentParser(description="furiosa-llm CLI")
    subparsers = parser.add_subparsers()

    serve_parser = subparsers.add_parser("serve", help="serve model")
    add_serve_args(serve_parser)

    args = parser.parse_args()

    if hasattr(args, "dispatch_function"):
        args.dispatch_function(args)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
