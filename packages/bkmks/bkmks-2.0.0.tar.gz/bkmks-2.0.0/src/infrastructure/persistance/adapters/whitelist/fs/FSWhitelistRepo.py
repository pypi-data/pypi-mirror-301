import os
from domain.entities.whitelist.Whitelist import Whitelist
from domain.repositories.whitelist.IWhitelistRepo import IWhitelistRepo


class FSWhitelistRepo(IWhitelistRepo):
    """Whitelist repository implementation based on a whitelist file in the filesystem."""

    def __init__(self, whitelist_path: str):
        if not os.path.exists(whitelist_path):
            raise FileNotFoundError(f"Whitelist file not found: {whitelist_path}")
        self.__wl_path = whitelist_path

    def get_whitelist(self) -> list[str]:
        with open(self.__wl_path, "r", encoding="utf-8") as f:
            whitelist_file_content = f.read()

        return Whitelist(whitelist_file_content=whitelist_file_content)
