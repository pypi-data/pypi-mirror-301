import json
import os
import platform
from typing import List, Union
from domain.entities.bookmark.Bookmark import Bookmark
from domain.entities.folder.Folder import Folder
from domain.repositories.bookmark.IBookmarkRepo import IBookmarkRepo
from domain.entities.whitelist.Whitelist import Whitelist


class BraveBookmarkRepo(IBookmarkRepo):
    """Bookmark repository implementation for Brave."""

    def __init__(
        self,
        brave_bookmarks_path: Union[str, None] = None,
    ):
        """Initialize the BraveBookmarkRepo.

        Args:
            brave_bookmarks_path (_type_: str or None): Path to the Brave bookmarks file
        """
        self.__brave_bookmarks_path = (
            brave_bookmarks_path or self.__get_brave_bookmarks_export_path()
        )

    def get_bkmks(self, whitelist: Whitelist = None) -> Folder:
        bookmarks_export = None
        with open(self.__brave_bookmarks_path, "r", encoding="utf-8") as f:
            bookmarks_export = json.load(f)

        brave_bkmks = self.__parse_brave_bookmarks(
            bookmarks_export=bookmarks_export, whitelist=whitelist
        )

        return brave_bkmks

    def __get_brave_bookmarks_export_path(self):
        """Retrieve the path to the Brave bookmarks file.

        Raises:
            OSError: Unsupported operating system
            FileNotFoundError: Brave bookmarks file not found

        Returns:
            _type_: str: Path to the Brave bookmarks file
        """
        maybe_brave_bookmarks_path = os.getenv("BRAVE_BOOKMARKS_PATH")

        if not maybe_brave_bookmarks_path:
            system = platform.system()
            if system == "Windows":
                maybe_brave_bookmarks_path = os.path.expandvars(
                    r"%LOCALAPPDATA%\BraveSoftware\Brave-Browser\User Data\Default\Bookmarks"
                )
            elif system == "Darwin":  # macOS
                maybe_brave_bookmarks_path = os.path.expanduser(
                    "~/Library/Application Support/BraveSoftware/Brave-Browser/Default/Bookmarks"
                )
            elif system == "Linux":
                maybe_brave_bookmarks_path = os.path.expanduser(
                    "~/.config/BraveSoftware/Brave-Browser/Default/Bookmarks"
                )
            else:
                raise OSError(f"Unsupported operating system: {system}")

        if not os.path.exists(maybe_brave_bookmarks_path):
            raise FileNotFoundError(
                f"Brave bookmarks file not found: {maybe_brave_bookmarks_path}, try setting the BRAVE_BOOKMARKS_PATH environment variable if the file is in a custom location."
            )

        return maybe_brave_bookmarks_path

    def __rec_parse__brave_bookmark(
        self, bookmark_or_folder: dict, current_path: str, whitelist: Whitelist = None
    ) -> Union[Folder, Bookmark, None]:
        """Recursively parse a Brave bookmark or folder.

        Args:
            bookmark_or_folder (_type_: dict): Brave bookmark or folder
            current_path (_type_: str): Current path
            only_parse_whitelisted (_type_: bool): Whether to only parse whitelisted bookmarks and folders

        Returns:
            _type_: Union[Folder, Bookmark, None]: Parsed bookmark or folder (or None if not whitelisted)
        """
        if "type" not in bookmark_or_folder:
            raise ValueError("Invalid Brave bookmark or folder: missing 'type' key")

        bookmark_or_folder_name = bookmark_or_folder["name"]
        new_path = f"{current_path}/{bookmark_or_folder_name}"
        if bookmark_or_folder["type"] == "folder":
            children: Union[Folder, Bookmark] = []

            if "children" not in bookmark_or_folder:
                return Folder(name=bookmark_or_folder_name, children=children)

            for child in bookmark_or_folder["children"]:
                parsed_child = self.__rec_parse__brave_bookmark(
                    bookmark_or_folder=child,
                    current_path=new_path,
                    whitelist=whitelist,
                )
                if parsed_child is not None:
                    children.append(parsed_child)

            if len(children) == 0:
                return None

            return Folder(name=bookmark_or_folder_name, children=children)
        elif bookmark_or_folder["type"] == "url":
            bookmark_url = bookmark_or_folder["url"]
            bookmark_or_folder_name = (
                bookmark_or_folder_name
                if bookmark_or_folder_name != bookmark_url
                else ""
            )

            is_whitelisted = True
            if whitelist is not None:
                is_whitelisted = whitelist.is_whitelisted(new_path)
                if not is_whitelisted:
                    return None
            if "url" not in bookmark_or_folder:
                raise ValueError("Invalid Brave bookmark: missing 'url' key")

            return Bookmark(name=bookmark_or_folder_name, url=bookmark_url)
        else:
            raise ValueError(
                f"Invalid Brave bookmark or folder: unsupported type '{bookmark_or_folder['type']}'"
            )

    def __rec_filter_folder(self, folder: Folder) -> Folder:
        """Recursively filter out None-Types of a Folder's children.

        Args:
             folder (_type_: Folder): Folder to filter

        Returns:

             _type_: Folder: Folder with empty folders removed
        """
        children = [child for child in folder.children if child is not None]
        children = [
            self.__rec_filter_folder(child) if isinstance(child, Folder) else child
            for child in children
        ]

        return Folder(name=folder.name, children=children)

    def __parse_brave_bookmarks(
        self, bookmarks_export: dict, whitelist: Whitelist = None
    ) -> List[Union[Folder, Bookmark]]:
        """Parse the Brave bookmarks export into a list of Folder and Bookmark instances.

        Args:
            bookmarks_export (_type_: dict): Brave bookmarks export

        Returns:
            _type_: Folder: Bookmarks root folder
        """
        if "roots" not in bookmarks_export:
            raise ValueError("Invalid Brave bookmarks export: missing 'roots' key")

        if "bookmark_bar" not in bookmarks_export["roots"]:
            raise ValueError(
                "Invalid Brave bookmarks export: missing 'bookmark_bar' key"
            )

        root_folder = Folder(
            name="root",
            children=[
                self.__rec_parse__brave_bookmark(
                    bookmark_or_folder=child, current_path="", whitelist=whitelist
                )
                for child in bookmarks_export["roots"]["bookmark_bar"]["children"]
            ],
        )

        filtered_root_folder = self.__rec_filter_folder(root_folder)

        return filtered_root_folder.children
