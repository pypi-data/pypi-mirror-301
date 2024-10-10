from abc import ABC

from domain.entities.whitelist.Whitelist import Whitelist


class IWhitelistRepo(ABC):
    """Repository interface for the whitelist"""

    def get_whitelist(self) -> Whitelist:
        """Get the whitelist"""
        pass
