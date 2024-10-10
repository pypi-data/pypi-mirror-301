import os
import pytest

from infrastructure.persistance.adapters.whitelist.fs.FSWhitelistRepo import (
    FSWhitelistRepo,
)

mock_whitelist_path = f"{os.path.dirname(__file__)}/__mocks__/.bkmks"


class TestFSWhitelistRepo:
    def test_non_existent_whitelist(self):
        with pytest.raises(FileNotFoundError):
            FSWhitelistRepo(whitelist_path="non_existent_whitelist_path")

    def test_get_whitelist(self):
        wl_repo = FSWhitelistRepo(whitelist_path=mock_whitelist_path)
        whitelist = wl_repo.get_whitelist()

        patterns = whitelist._Whitelist__whitelist_spec.patterns

        for pattern in patterns:
            assert pattern.pattern in [
                "Test Bookmark",
                "test/deep/path/bookmark",
                "test/deeper/path/fol/der/",
            ]
