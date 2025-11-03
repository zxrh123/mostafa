"""
Knowledge Base Crawler
Learns from MikroTik forums and updates knowledge base
"""

import asyncio
import aiohttp
from typing import List, Dict, Optional
import logging
from datetime import datetime
from app.core.config import settings
import json

logger = logging.getLogger(__name__)


class KnowledgeBaseCrawler:
    """
    Crawler for MikroTik knowledge base
    Learns from forums, documentation, and community resources
    """
    
    def __init__(self):
        self.knowledge_base: Dict[str, List[Dict]] = {}
        self.running = False
        self.sources = [
            "https://forum.mikrotik.com",
            "https://wiki.mikrotik.com",
        ]
    
    async def start(self):
        """Start knowledge base crawler"""
        if not settings.KNOWLEDGE_BASE_ENABLED:
            logger.info("Knowledge Base Crawler is disabled")
            return
        
        self.running = True
        logger.info("?? Starting Knowledge Base Crawler...")
        
        # Initial crawl
        await self.crawl_all_sources()
        
        # Schedule periodic updates
        asyncio.create_task(self._periodic_update())
    
    async def stop(self):
        """Stop knowledge base crawler"""
        self.running = False
        logger.info("?? Knowledge Base Crawler stopped")
    
    async def _periodic_update(self):
        """Periodically update knowledge base"""
        while self.running:
            await asyncio.sleep(settings.KNOWLEDGE_BASE_UPDATE_INTERVAL)
            if self.running:
                await self.crawl_all_sources()
    
    async def crawl_all_sources(self):
        """Crawl all knowledge sources"""
        for source in self.sources:
            try:
                await self.crawl_source(source)
            except Exception as e:
                logger.error(f"Error crawling source {source}: {e}")
    
    async def crawl_source(self, url: str):
        """Crawl a specific source"""
        try:
            async with aiohttp.ClientSession() as session:
                # In production, implement actual web scraping
                # For now, we'll use a placeholder
                logger.info(f"Crawling {url}...")
                
                # Simulate knowledge extraction
                knowledge = {
                    "source": url,
                    "timestamp": datetime.now().isoformat(),
                    "topics": [
                        {
                            "title": "RouterOS Scripting Best Practices",
                            "content": "Always use dry-run before executing scripts...",
                            "tags": ["scripting", "best-practices"]
                        },
                        {
                            "title": "Troubleshooting Interface Issues",
                            "content": "Check interface status, MTU settings...",
                            "tags": ["interfaces", "troubleshooting"]
                        }
                    ]
                }
                
                self.knowledge_base[url] = knowledge.get("topics", [])
                logger.info(f"? Crawled {len(knowledge.get('topics', []))} topics from {url}")
                
        except Exception as e:
            logger.error(f"Error crawling {url}: {e}")
    
    def search_knowledge(self, query: str) -> List[Dict]:
        """Search knowledge base"""
        results = []
        query_lower = query.lower()
        
        for source, topics in self.knowledge_base.items():
            for topic in topics:
                if (
                    query_lower in topic.get("title", "").lower() or
                    query_lower in topic.get("content", "").lower() or
                    any(query_lower in tag.lower() for tag in topic.get("tags", []))
                ):
                    results.append({
                        **topic,
                        "source": source
                    })
        
        return results
    
    def get_knowledge_for_intent(self, intent: str) -> List[Dict]:
        """Get relevant knowledge for a specific intent"""
        intent_keywords = {
            "monitor": ["monitoring", "status", "performance"],
            "execute": ["scripting", "commands", "execution"],
            "fix": ["troubleshooting", "repair", "issues"],
            "analyze": ["analysis", "diagnostics", "logs"]
        }
        
        keywords = intent_keywords.get(intent, [])
        results = []
        
        for keyword in keywords:
            results.extend(self.search_knowledge(keyword))
        
        return results[:5]  # Return top 5 results
