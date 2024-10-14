from contextlib import suppress
import time
import httpx
import xml.etree.ElementTree as ET
from datetime import datetime
from .models import RSSChannel, RSSItem
from .exceptions import InvalidURLError, MissingElementError, RSSFetchError


class RSSFetcher:
    def __init__(self, url: str):
        if not url.startswith("https://nyaa.si/?page=rss"):
            raise InvalidURLError(url)
        self.url = url

    def fetch_and_parse(self, max_retry: int = 10) -> RSSChannel:
        rss_feed = self._fetch_rss_feed(max_retry)
        return self._parse_rss(rss_feed)

    def _convert_to_bytes(self, size_str: str) -> int:
        size, unit = size_str.split()
        size = float(size)

        units: dict[str, int] = {
            "B": 1,
            "KiB": 1024,
            "MiB": 1024**2,
            "GiB": 1024**3,
            "TiB": 1024**4,
            "PiB": 1024**5,
            "EiB": 1024**6,
        }

        return int(size * units[unit])

    def _convert_to_dt(self, date_string: str) -> datetime:
        return datetime.strptime(date_string, "%a, %d %b %Y %H:%M:%S %z")

    def _convert_to_bool(self, text: str):
        return text.lower() == "yes"

    def _fetch_rss_feed(self, max_retry: int) -> str:
        for attempt in range(1, max_retry + 1):
            print(f"Fetching RSS feed: Attempt={attempt}")
            with suppress(Exception):
                resp: httpx.Response = httpx.get(self.url)
                resp.raise_for_status()
                return resp.text
            time.sleep(3)
        raise RSSFetchError(self.url, max_retry)

    def _parse_rss(self, rss_feed: str) -> RSSChannel:
        namespaces = {"nyaa": "https://nyaa.si/xmlns/nyaa"}
        root = ET.fromstring(rss_feed)

        channel_element = root.find("channel")
        if channel_element is None:
            raise MissingElementError("channel")

        channel = RSSChannel(
            title=self._get_value_or_raise(channel_element, "title", namespaces),
            description=self._get_value_or_raise(
                channel_element, "description", namespaces
            ),
            link=self._get_value_or_raise(channel_element, "link", namespaces),
        )

        for item in root.findall("channel/item"):
            rss_item = RSSItem(
                title=self._get_value_or_raise(item, "title", namespaces),
                link=self._get_value_or_raise(item, "link", namespaces),
                guid=self._get_value_or_raise(item, "guid", namespaces),
                pub_date=self._convert_to_dt(
                    self._get_value_or_raise(item, "pubDate", namespaces)
                ),
                seeders=int(self._get_value_or_raise(item, "nyaa:seeders", namespaces)),
                leechers=int(
                    self._get_value_or_raise(item, "nyaa:leechers", namespaces)
                ),
                downloads=int(
                    self._get_value_or_raise(item, "nyaa:downloads", namespaces)
                ),
                info_hash=self._get_value_or_raise(item, "nyaa:infoHash", namespaces),
                category=self._get_value_or_raise(item, "nyaa:category", namespaces),
                size_bytes=self._convert_to_bytes(
                    self._get_value_or_raise(item, "nyaa:size", namespaces)
                ),
                trusted=self._convert_to_bool(
                    self._get_value_or_raise(item, "nyaa:trusted", namespaces)
                ),
                remake=self._convert_to_bool(
                    self._get_value_or_raise(item, "nyaa:remake", namespaces)
                ),
            )
            channel.add_item(rss_item)

        return channel

    def _get_value_or_raise(
        self, element: ET.Element, xpath: str, namespaces: dict[str, str]
    ) -> str:
        ele = element.find(xpath, namespaces)
        if ele is None or ele.text is None:
            raise MissingElementError(xpath)
        return ele.text
