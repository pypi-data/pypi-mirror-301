from pathspec import PathSpec, patterns


class Whitelist:
    """A whitelist of patterns to match against."""

    # patterns
    __whitelist_spec: PathSpec

    def __init__(self, whitelist_file_content: str) -> None:
        self.__whitelist_spec = PathSpec.from_lines(
            patterns.GitWildMatchPattern, whitelist_file_content.splitlines()
        )

    def is_whitelisted(self, path: str) -> bool:
        """Check if a path is whitelisted.

        Args:
            path (_type_: str): Path to check

        Returns:
            _type_: bool: Whether the path is whitelisted
        """
        matches = self.__whitelist_spec.match_file(path)

        return matches
