"""Knowledge base ingestion service."""

from __future__ import annotations

import httpx
from bs4 import BeautifulSoup
from loguru import logger


class KnowledgeBaseCrawler:
    def __init__(self) -> None:
        self.sources = [
            "https://forum.mikrotik.com",
            "https://help.mikrotik.com/docs/display/ROS/",
        ]

    async def fetch_articles(self, limit: int = 5) -> list[dict[str, str]]:
        articles: list[dict[str, str]] = []
        async with httpx.AsyncClient(timeout=15) as client:
            for source in self.sources:
                try:
                    response = await client.get(source)
                    response.raise_for_status()
                except Exception as exc:  # pragma: no cover
                    logger.warning("Failed to crawl {}: {}", source, exc)
                    continue
                soup = BeautifulSoup(response.text, "lxml")
                for link in soup.find_all("a")[:limit]:
                    title = link.get_text(strip=True)
                    href = link.get("href")
                    if title and href:
                        articles.append({"title": title, "url": href, "source": source})
        return articles


async def refresh_knowledge_base() -> list[dict[str, str]]:
    crawler = KnowledgeBaseCrawler()
    articles = await crawler.fetch_articles(limit=10)
    logger.info("Knowledge base refreshed: {} new articles", len(articles))
    return articles
