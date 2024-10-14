from dataclasses import dataclass, field
from datetime import datetime
from typing import List


@dataclass
class RSSItem:
    title: str
    link: str
    guid: str
    pub_date: datetime
    seeders: int
    leechers: int
    downloads: int
    info_hash: str
    category: str
    size_bytes: int
    trusted: bool
    remake: bool


@dataclass
class RSSChannel:
    title: str
    description: str
    link: str
    items: List[RSSItem] = field(default_factory=list)

    def add_item(self, item: RSSItem) -> None:
        self.items.append(item)
