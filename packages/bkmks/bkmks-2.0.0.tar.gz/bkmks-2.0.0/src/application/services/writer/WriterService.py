from datetime import datetime
from domain.entities.whitelist.Whitelist import Whitelist
from domain.repositories.bookmark.IBookmarkRepo import IBookmarkRepo
from domain.entities.folder.Folder import Folder


class WriterService:
    __bkmks_repo: IBookmarkRepo
    __whitelist: Whitelist
    __current_time: datetime

    def __init__(
        self,
        current_time: datetime,
        bkmks_repo: IBookmarkRepo,
        whitelist: Whitelist = None,
    ):
        self.__current_time = current_time
        self.__bkmks_repo = bkmks_repo
        self.__whitelist = whitelist

    def print_bkmks_json(self):
        """Returns a JSON of all"""

        bkmks_and_folders = self.__bkmks_repo.get_bkmks(whitelist=self.__whitelist)
        root_folder = Folder(name="Bookmarks", children=bkmks_and_folders)

        json_str = (
            "{"
            + f'"created": "{self.__current_time}", "bookmarks": {root_folder.to_json()}'
            + "}"
        )
        return json_str
