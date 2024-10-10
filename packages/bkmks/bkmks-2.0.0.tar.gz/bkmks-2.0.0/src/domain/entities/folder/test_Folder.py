import pytest
from src.domain.entities.bookmark.Bookmark import Bookmark
from src.domain.entities.folder.Folder import Folder

mocked_bookmark = Bookmark(name="Test Bookmark", url="https://www.example.com/")


class TestBookmark:
    @pytest.fixture
    def mocked_folder(self):
        return Folder(
            name="Test Folder",
            children=[
                Folder(name="Subfolder", children=[mocked_bookmark]),
                mocked_bookmark,
                mocked_bookmark,
            ],
        )

    @pytest.fixture
    def mocked_folder_json(self):
        return '{"name": "Test Folder", "children": [{"name": "Subfolder", "children": [{"name": "Test Bookmark", "url": "https://www.example.com/"}]},{"name": "Test Bookmark", "url": "https://www.example.com/"},{"name": "Test Bookmark", "url": "https://www.example.com/"}]}'

    def test_to_json(self, mocked_folder, mocked_folder_json):
        json_str = mocked_folder.to_json()
        assert json_str == mocked_folder_json
