"""
Knowledge Base Crawler - زاحف قاعدة المعرفة
يزحف ويجمع المعلومات من مصادر MikroTik ويحدّث قاعدة المعرفة

المسؤوليات:
- الزحف إلى منتديات ووثائق MikroTik
- استخراج المعلومات المفيدة
- تصنيف وفهرسة المعرفة
- تحديث قاعدة المعرفة تلقائياً
- التعلم من الحلول الشائعة
"""

import asyncio
import logging
from typing import Dict, List, Optional
from datetime import datetime
import aiohttp
from bs4 import BeautifulSoup
import json
from dataclasses import dataclass
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class KnowledgeCategory(Enum):
    """فئات المعرفة"""
    TROUBLESHOOTING = "troubleshooting"
    CONFIGURATION = "configuration"
    BEST_PRACTICES = "best_practices"
    SECURITY = "security"
    OPTIMIZATION = "optimization"
    NETWORKING = "networking"


@dataclass
class KnowledgeEntry:
    """عنصر معرفة"""
    id: str
    title: str
    content: str
    category: KnowledgeCategory
    source: str
    url: str
    created_at: datetime
    relevance_score: float
    tags: List[str]
    language: str


class KnowledgeCrawler:
    """
    زاحف قاعدة المعرفة - Knowledge Crawler
    
    يجمع المعرفة من مصادر MikroTik الرسمية
    """
    
    def __init__(
        self,
        ai_brain,
        update_interval: int = 3600,
        max_entries: int = 1000,
        enabled: bool = True
    ):
        """
        تهيئة الزاحف
        
        Args:
            ai_brain: العقل الصناعي للتحليل
            update_interval: فترة التحديث بالثواني
            max_entries: الحد الأقصى لعناصر المعرفة
            enabled: تفعيل/تعطيل الزاحف
        """
        self.ai_brain = ai_brain
        self.update_interval = update_interval
        self.max_entries = max_entries
        self.enabled = enabled
        
        # قاعدة المعرفة
        self.knowledge_base: List[KnowledgeEntry] = []
        
        # مصادر المعرفة
        self.sources = {
            "wiki": "https://wiki.mikrotik.com",
            "forum": "https://forum.mikrotik.com",
            "help": "https://help.mikrotik.com"
        }
        
        # الكلمات المفتاحية المهمة
        self.important_keywords = [
            "cpu", "memory", "bandwidth", "firewall", "routing",
            "wireless", "vpn", "security", "optimization", "troubleshooting",
            "configuration", "interface", "dhcp", "dns", "nat"
        ]
        
        logger.info("📚 Knowledge Crawler تم تهيئته بنجاح")
    
    async def start_crawling(self):
        """بدء الزحف الدوري"""
        if not self.enabled:
            logger.info("⏸️ Knowledge Crawler معطل")
            return
        
        logger.info("🚀 بدء الزحف الدوري...")
        
        while self.enabled:
            try:
                await self.crawl_all_sources()
                
                # الانتظار حتى الجولة التالية
                await asyncio.sleep(self.update_interval)
            
            except Exception as e:
                logger.error(f"خطأ في الزحف: {e}")
                await asyncio.sleep(60)
    
    async def crawl_all_sources(self):
        """الزحف إلى جميع المصادر"""
        logger.info("🔍 بدء الزحف إلى المصادر...")
        
        tasks = [
            self.crawl_wiki(),
            self.crawl_forum(),
            self.crawl_help_docs()
        ]
        
        results = await asyncio.gather(*tasks, return_exceptions=True)
        
        new_entries = 0
        for result in results:
            if isinstance(result, list):
                new_entries += len(result)
        
        logger.info(f"✅ تم جمع {new_entries} عنصر معرفة جديد")
        
        # تنظيف القديم والاحتفاظ بالأحدث
        self._cleanup_old_entries()
    
    async def crawl_wiki(self) -> List[KnowledgeEntry]:
        """الزحف إلى MikroTik Wiki"""
        logger.info("📖 الزحف إلى Wiki...")
        
        entries = []
        
        try:
            async with aiohttp.ClientSession() as session:
                # هذا مثال - في التطبيق الفعلي، ستحتاج إلى زحف حقيقي
                # مع احترام robots.txt والقيود
                
                # مثال على صفحات مهمة
                important_pages = [
                    "/wiki/Manual:TOC",
                    "/wiki/Manual:Troubleshooting",
                    "/wiki/Manual:Configuration",
                    "/wiki/Manual:Best_Practices"
                ]
                
                for page in important_pages:
                    try:
                        url = self.sources["wiki"] + page
                        
                        # في التطبيق الحقيقي، استخدم aiohttp لجلب الصفحة
                        # async with session.get(url) as response:
                        #     html = await response.text()
                        #     entry = await self._parse_wiki_page(html, url)
                        
                        # مثال بسيط
                        entry = KnowledgeEntry(
                            id=f"wiki-{datetime.now().timestamp()}",
                            title=f"Wiki: {page}",
                            content="محتوى مثال من Wiki",
                            category=KnowledgeCategory.BEST_PRACTICES,
                            source="wiki",
                            url=url,
                            created_at=datetime.now(),
                            relevance_score=0.8,
                            tags=["configuration", "manual"],
                            language="en"
                        )
                        
                        entries.append(entry)
                        
                    except Exception as e:
                        logger.error(f"خطأ في زحف صفحة Wiki: {e}")
            
        except Exception as e:
            logger.error(f"خطأ في الزحف إلى Wiki: {e}")
        
        return entries
    
    async def crawl_forum(self) -> List[KnowledgeEntry]:
        """الزحف إلى MikroTik Forum"""
        logger.info("💬 الزحف إلى Forum...")
        
        entries = []
        
        try:
            # الزحف إلى منتدى MikroTik
            # مع التركيز على المواضيع الحديثة والمفيدة
            
            # مثال بسيط
            entry = KnowledgeEntry(
                id=f"forum-{datetime.now().timestamp()}",
                title="حل مشكلة High CPU Usage",
                content="عند ارتفاع استخدام CPU، جرب تنظيف Connection Tracking",
                category=KnowledgeCategory.TROUBLESHOOTING,
                source="forum",
                url=self.sources["forum"],
                created_at=datetime.now(),
                relevance_score=0.9,
                tags=["cpu", "troubleshooting"],
                language="en"
            )
            
            entries.append(entry)
        
        except Exception as e:
            logger.error(f"خطأ في الزحف إلى Forum: {e}")
        
        return entries
    
    async def crawl_help_docs(self) -> List[KnowledgeEntry]:
        """الزحف إلى وثائق المساعدة"""
        logger.info("📄 الزحف إلى Help Docs...")
        
        entries = []
        
        try:
            # الزحف إلى وثائق المساعدة الرسمية
            
            entry = KnowledgeEntry(
                id=f"help-{datetime.now().timestamp()}",
                title="RouterOS Security Best Practices",
                content="أفضل ممارسات الأمان في RouterOS",
                category=KnowledgeCategory.SECURITY,
                source="help",
                url=self.sources["help"],
                created_at=datetime.now(),
                relevance_score=0.95,
                tags=["security", "best-practices"],
                language="en"
            )
            
            entries.append(entry)
        
        except Exception as e:
            logger.error(f"خطأ في الزحف إلى Help Docs: {e}")
        
        return entries
    
    async def _parse_wiki_page(self, html: str, url: str) -> Optional[KnowledgeEntry]:
        """تحليل صفحة Wiki"""
        try:
            soup = BeautifulSoup(html, 'html.parser')
            
            # استخراج العنوان
            title = soup.find('h1')
            title_text = title.get_text() if title else "Unknown"
            
            # استخراج المحتوى
            content = soup.find('div', {'class': 'mw-parser-output'})
            content_text = content.get_text() if content else ""
            
            # استخدام الذكاء الصناعي لتصنيف المحتوى
            category = await self._categorize_content(title_text, content_text)
            
            # استخراج الكلمات المفتاحية
            tags = self._extract_keywords(content_text)
            
            entry = KnowledgeEntry(
                id=f"wiki-{hash(url)}",
                title=title_text,
                content=content_text[:500],  # أول 500 حرف
                category=category,
                source="wiki",
                url=url,
                created_at=datetime.now(),
                relevance_score=0.8,
                tags=tags,
                language="en"
            )
            
            return entry
        
        except Exception as e:
            logger.error(f"خطأ في تحليل صفحة Wiki: {e}")
            return None
    
    async def _categorize_content(
        self,
        title: str,
        content: str
    ) -> KnowledgeCategory:
        """تصنيف المحتوى باستخدام الذكاء الصناعي"""
        # يمكن استخدام الذكاء الصناعي هنا
        # لكن حالياً نستخدم تصنيف بسيط
        
        content_lower = (title + " " + content).lower()
        
        if any(word in content_lower for word in ["troubleshoot", "problem", "issue", "error"]):
            return KnowledgeCategory.TROUBLESHOOTING
        elif any(word in content_lower for word in ["security", "firewall", "attack"]):
            return KnowledgeCategory.SECURITY
        elif any(word in content_lower for word in ["optimize", "performance", "speed"]):
            return KnowledgeCategory.OPTIMIZATION
        elif any(word in content_lower for word in ["configure", "setup", "install"]):
            return KnowledgeCategory.CONFIGURATION
        else:
            return KnowledgeCategory.BEST_PRACTICES
    
    def _extract_keywords(self, content: str) -> List[str]:
        """استخراج الكلمات المفتاحية"""
        content_lower = content.lower()
        
        keywords = []
        for keyword in self.important_keywords:
            if keyword in content_lower:
                keywords.append(keyword)
        
        return keywords[:5]  # أهم 5 كلمات
    
    def _cleanup_old_entries(self):
        """تنظيف العناصر القديمة والاحتفاظ بالأحدث"""
        if len(self.knowledge_base) > self.max_entries:
            # ترتيب حسب التاريخ والأهمية
            self.knowledge_base.sort(
                key=lambda x: (x.relevance_score, x.created_at),
                reverse=True
            )
            
            # الاحتفاظ بالأحدث
            self.knowledge_base = self.knowledge_base[:self.max_entries]
            
            logger.info(f"🧹 تم تنظيف قاعدة المعرفة. المتبقي: {len(self.knowledge_base)}")
    
    async def search_knowledge(
        self,
        query: str,
        category: Optional[KnowledgeCategory] = None,
        limit: int = 10
    ) -> List[KnowledgeEntry]:
        """البحث في قاعدة المعرفة"""
        query_lower = query.lower()
        
        results = []
        for entry in self.knowledge_base:
            # فحص الفئة
            if category and entry.category != category:
                continue
            
            # فحص التطابق في العنوان أو المحتوى أو الكلمات المفتاحية
            if (
                query_lower in entry.title.lower() or
                query_lower in entry.content.lower() or
                any(query_lower in tag for tag in entry.tags)
            ):
                results.append(entry)
        
        # ترتيب حسب الأهمية
        results.sort(key=lambda x: x.relevance_score, reverse=True)
        
        return results[:limit]
    
    def get_statistics(self) -> Dict:
        """الحصول على إحصائيات قاعدة المعرفة"""
        categories_count = {}
        for entry in self.knowledge_base:
            cat = entry.category.value
            categories_count[cat] = categories_count.get(cat, 0) + 1
        
        return {
            "enabled": self.enabled,
            "total_entries": len(self.knowledge_base),
            "categories": categories_count,
            "sources": list(self.sources.keys()),
            "update_interval": self.update_interval
        }


# مثال على الاستخدام
if __name__ == "__main__":
    async def test_crawler():
        """اختبار الزاحف"""
        from core_ai_brain import CoreAIBrain
        
        ai_brain = CoreAIBrain(
            openai_api_key="your-key",
            gemini_api_key="your-key"
        )
        
        crawler = KnowledgeCrawler(
            ai_brain=ai_brain,
            update_interval=3600,
            max_entries=1000,
            enabled=True
        )
        
        # زحف واحد
        await crawler.crawl_all_sources()
        
        # البحث
        results = await crawler.search_knowledge("cpu high usage")
        
        print(f"🔍 نتائج البحث: {len(results)}")
        for result in results:
            print(f"- {result.title} ({result.category.value})")
        
        # الإحصائيات
        stats = crawler.get_statistics()
        print(f"\n📊 الإحصائيات: {json.dumps(stats, indent=2, ensure_ascii=False)}")
    
    asyncio.run(test_crawler())
