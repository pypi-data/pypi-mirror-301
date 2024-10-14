class InvalidURLError(ValueError):
    def __init__(self, url: str):
        super().__init__(
            f"Invalid URL provided: {url}. Expected URL to start with 'https://nyaa.si/?page=rss'."
        )


class RSSFetchError(Exception):
    def __init__(self, url: str, attempts: int):
        super().__init__(
            f"Failed to fetch RSS feed from {url} after {attempts} attempts."
        )


class MissingElementError(ValueError):
    def __init__(self, element: str):
        super().__init__(f"Missing required XML element: {element}.")
