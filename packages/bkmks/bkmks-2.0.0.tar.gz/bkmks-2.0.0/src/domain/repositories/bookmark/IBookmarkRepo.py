from abc import abstractmethod, ABC
from typing import List, Union
from domain.entities.folder.Folder import Folder
from domain.entities.whitelist.Whitelist import Whitelist
from domain.entities.bookmark.Bookmark import Bookmark


class IBookmarkRepo(ABC):
    """BookmarkRepo interface"""

    @abstractmethod
    def get_bkmks(self, whitelist: Whitelist = None) -> List[Union[Folder, Bookmark]]:
        """Get all bookmarks toolbar starting from the root. Only returns whitelisted bookmarks if a whitelist is passed.

        Returns:
            _type_: List[Union[Folder, Bookmark]]: All bookmarks
        """
        pass
