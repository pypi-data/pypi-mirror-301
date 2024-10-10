import argparse
import datetime
from os import path
import os
from application.services.writer.WriterService import WriterService
from domain.repositories.bookmark.IBookmarkRepo import IBookmarkRepo
import questionary
from domain.repositories.whitelist.IWhitelistRepo import IWhitelistRepo
from infrastructure.persistance.adapters.bookmark.brave.BraveBookmarkRepo import (
    BraveBookmarkRepo,
)
from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import (
    FSWhitelistRepo,
)

EXPECTED_WL_FILE_NAME = ".bkmks"
SUPPORTED_BROWSERS = ["brave"]


def main():
    not_supported_msg = "Sorry, this browser does not seem to be supported yet, but PRs are always welcome! See https://github.com/nico-i/bkmks#contributing for more information."

    supported_browsers = SUPPORTED_BROWSERS.copy()
    supported_browsers.append("other")

    parser = argparse.ArgumentParser(
        description="Extract your browser bookmarks into a normalized JSON"
    )
    parser.add_argument(
        "-w",
        "--whitelist",
        help='Path to your bookmark whitelist (aka your ".bkmks" file)',
    )
    parser.add_argument(
        "-b",
        "--browser",
        help="The browser you want to extract bookmarks from",
        choices=supported_browsers,
    )
    parser.add_argument("-o", "--output", help="Output file path")
    args, _ = parser.parse_known_args()

    set_args = {k: v for k, v in vars(args).items() if v is not None}
    are_any_args_set = len(set_args) == 0

    if are_any_args_set:
        if not args.browser:
            args.browser = questionary.select(
                "Select the browser you want to extract bookmarks from:",
                choices=supported_browsers,
            ).ask()

        if args.browser == "other":
            print(not_supported_msg)
            return

        if not args.whitelist:
            use_wl = questionary.confirm(
                "Would you like to only extract whitelisted bookmarks?", default=False
            ).ask()
            if use_wl:
                args.whitelist = questionary.path(
                    "Enter the path to your bookmark whitelist:",
                    default=path.join(os.getcwd(), ".bkmks"),
                ).ask()

        if args.whitelist:
            if not os.path.exists(args.whitelist):
                print(
                    f'Whitelist file could not be found at "{args.whitelist}". Aborting...'
                )
                return
            if not os.path.isfile(args.whitelist):
                print(
                    f'Whitelist path must lead to a file named "{EXPECTED_WL_FILE_NAME}". Aborting...'
                )
                return
            if not args.whitelist.endswith(EXPECTED_WL_FILE_NAME):
                print(
                    f'Whitelist file must be named "{EXPECTED_WL_FILE_NAME}"! Aborting...'
                )
                return

        if not args.output:
            write_to_file = questionary.confirm(
                "Would you like to write the output to a file (will otherwise be printed to console)?",
                default=True,
            ).ask()
            if write_to_file:
                args.output = questionary.path(
                    "Enter the output file path:", default="bookmarks.json"
                ).ask()

    if are_any_args_set and args.browser is None:
        print(
            'Please at least set the "--browser" flag when using CLI flags to run the program. See "--help" for more details. Aborting...'
        )
        return

    bkmks_repo: IBookmarkRepo
    if args.browser == "brave":
        bkmks_repo = BraveBookmarkRepo()
    elif args.browser == "other":
        print(not_supported_msg)
        return

    wl_repo: IWhitelistRepo = None
    if args.whitelist:
        wl_repo = FSWhitelistRepo(whitelist_path=args.whitelist)

    whitelist = None if wl_repo is None else wl_repo.get_whitelist()

    writer_service = WriterService(
        bkmks_repo=bkmks_repo, whitelist=whitelist, current_time=datetime.datetime.now()
    )

    json_str = writer_service.print_bkmks_json()

    if not args.output:
        print(json_str)
        return

    with open(args.output, "w", encoding="utf-8") as f:
        f.write(json_str)


if __name__ == "__main__":
    main()
