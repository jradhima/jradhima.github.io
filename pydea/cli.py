#!/usr/bin/env python3
"""CLI for pydea - minimal markdown blog generator."""

import argparse
import sys


def main():
    parser = argparse.ArgumentParser(prog="pydea", description="Minimal markdown blog generator")
    subparsers = parser.add_subparsers(dest="command")

    subparsers.add_parser("build", help="Build the site to output/")

    new_parser = subparsers.add_parser("new", help="Create a new post")
    new_parser.add_argument("title", help="Post title")

    args = parser.parse_args()

    if args.command == "build":
        from pydea.build import build
        build()
    elif args.command == "new":
        from pydea.new import new_post
        new_post(args.title)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
