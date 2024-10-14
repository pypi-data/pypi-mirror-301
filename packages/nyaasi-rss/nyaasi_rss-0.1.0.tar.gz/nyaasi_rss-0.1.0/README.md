# NyaaSI RSS Package

This package provides a simple interface to fetch and parse RSS feeds from [nyaa.si](https://nyaa.si/).

## Installation

You can install the package using pip:

```bash
pip install nyaasi_rss
```

## Usage

Here’s how you can use the package:

```bash
from nyaasi_rss import RSSFetcher

fetcher = RSSFetcher("https://nyaa.si/?page=rss")
rss_channel = fetcher.fetch_and_parse()

for item in rss_channel.items:
    print(f"{item.title} - Seeders: {item.seeders}")
```
