import os

from domain.entities.whitelist.Whitelist import Whitelist

mock_whitelist_path = f"{os.path.dirname(__file__)}/__mocks__/.bkmks"


class TestWhitelist:
    def test_is_whitelisted(self):
        with open(mock_whitelist_path, "r", encoding="utf-8") as f:
            whitelist_file_content = f.read()

        whitelist = Whitelist(whitelist_file_content=whitelist_file_content)
        assert whitelist.is_whitelisted("Test Bookmark") is True
        assert whitelist.is_whitelisted("Test Bookmark 2") is False
        assert whitelist.is_whitelisted("root folder/") is False
        assert whitelist.is_whitelisted("root folder/Test Bookmark") is True
        assert whitelist.is_whitelisted("test/blacklisted") is False
        assert whitelist.is_whitelisted("test/deep/") is False
        assert whitelist.is_whitelisted("test/deep/folder/") is True
        assert whitelist.is_whitelisted("test/deep/folder/Bookmark") is True
        assert (
            whitelist.is_whitelisted("test/deep/folder/blacklisted bookmark") is False
        )
        assert whitelist.is_whitelisted("test/deep/folder/another bookmark") is True
        assert whitelist.is_whitelisted("test/deep/folder/blacklisted folder/") is False
