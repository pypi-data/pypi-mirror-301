import os

from domain.entities.bookmark.Bookmark import Bookmark
from domain.entities.folder.Folder import Folder
from infrastructure.persistance.adapters.bookmark.brave.BraveBookmarkRepo import (
    BraveBookmarkRepo,
)
from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import (
    FSWhitelistRepo,
)

mock_brave_export_path = f"{os.path.dirname(__file__)}/__mocks__/mock_brave_export.json"

mock_whitelist_path = f"{os.path.dirname(__file__)}/__mocks__/.bkmks"


class TestBraveBookmarkRepo:
    def test_get_full_toolbar(self):
        brave_bookmark_repo = BraveBookmarkRepo(
            brave_bookmarks_path=mock_brave_export_path
        )
        full_toolbar = brave_bookmark_repo.get_bkmks()

        expected_bookmarks_folder = [
            Folder(
                name="whitelisted root level Folder",
                children=[
                    Folder(
                        name="1. level whitelisted Folder",
                        children=[
                            Bookmark(
                                name="2. Level whitelisted Bookmark",
                                url="https://whitelist.com",
                            ),
                            Bookmark(
                                name="2. Level blacklisted Bookmark",
                                url="https://blacklist.com",
                            ),
                        ],
                    ),
                    Bookmark(
                        name="1. Level whitelisted Bookmark",
                        url="https://whitelist.com",
                    ),
                    Bookmark(
                        name="1. Level blacklisted Bookmark",
                        url="https://blacklist.com",
                    ),
                ],
            ),
            Bookmark(
                name="root level whitelisted bookmark", url="https://whitelist.com"
            ),
            Bookmark(
                name="root level blacklisted bookmark", url="https://blacklist.com"
            ),
        ]

        assert full_toolbar == expected_bookmarks_folder

    def test_get_whitelisted_toolbar(self):
        whitelisted_repo = FSWhitelistRepo(whitelist_path=mock_whitelist_path)
        whitelist = whitelisted_repo.get_whitelist()
        brave_whitelisted_bookmark_repo = BraveBookmarkRepo(
            brave_bookmarks_path=mock_brave_export_path
        )
        whitelisted_toolbar = brave_whitelisted_bookmark_repo.get_bkmks(
            whitelist=whitelist
        )

        assert whitelisted_toolbar == [
            Folder(
                name="whitelisted root level Folder",
                children=[
                    Folder(
                        name="1. level whitelisted Folder",
                        children=[
                            Bookmark(
                                name="2. Level whitelisted Bookmark",
                                url="https://whitelist.com",
                            ),
                        ],
                    ),
                    Bookmark(
                        name="1. Level whitelisted Bookmark",
                        url="https://whitelist.com",
                    ),
                ],
            ),
            Bookmark(
                name="root level whitelisted bookmark", url="https://whitelist.com"
            ),
        ]
