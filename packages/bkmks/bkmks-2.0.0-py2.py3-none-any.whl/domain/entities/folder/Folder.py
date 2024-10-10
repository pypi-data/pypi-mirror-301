from typing import List, Union

from dataclasses import dataclass, field

from domain.entities.bookmark.Bookmark import Bookmark
from domain.interfaces.JSONable.JSONable import JSONable


@dataclass
class Folder(JSONable):
    """
    A folder containing bookmarks and subfolders.
    """

    name: str
    # Children (sub-folders and bookmarks)
    children: List[Union["Folder", Bookmark]] = field(default_factory=list)

    def to_json(self) -> str:
        if not all([isinstance(child, JSONable) for child in self.children]):
            raise ValueError("All children must be JSONable")

        return f'{{"name": "{self.name}", "children": [{",".join([child.to_json() for child in self.children])}]}}'
