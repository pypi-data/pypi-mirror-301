import datetime
from application.services.writer.WriterService import WriterService
from infrastructure.persistance.adapters.bookmark.brave.BraveBookmarkRepo import (
    BraveBookmarkRepo,
)
from infrastructure.persistance.adapters.bookmark.brave.test_BraveBookmarkRepo import (
    mock_brave_export_path,
)


def test_print_bkmks_json():
    mock_brave_bookmark_repo = BraveBookmarkRepo(
        brave_bookmarks_path=mock_brave_export_path
    )

    mock_datetime = datetime.datetime.strptime(
        "2021-09-01T00:00:00.000000", "%Y-%m-%dT%H:%M:%S.%f"
    )

    expected_json_str = '{"created": "2021-09-01 00:00:00", "bookmarks": {"name": "Bookmarks", "children": [{"name": "whitelisted root level Folder", "children": [{"name": "1. level whitelisted Folder", "children": [{"name": "2. Level whitelisted Bookmark", "url": "https://whitelist.com"},{"name": "2. Level blacklisted Bookmark", "url": "https://blacklist.com"}]},{"name": "1. Level whitelisted Bookmark", "url": "https://whitelist.com"},{"name": "1. Level blacklisted Bookmark", "url": "https://blacklist.com"}]},{"name": "root level whitelisted bookmark", "url": "https://whitelist.com"},{"name": "root level blacklisted bookmark", "url": "https://blacklist.com"}]}}'
    mocked_writer_service = WriterService(
        bkmks_repo=mock_brave_bookmark_repo, current_time=mock_datetime
    )

    json_str = mocked_writer_service.print_bkmks_json()
    assert json_str == expected_json_str
