"""
Core AI Brain - The central intelligence of the system
Integrates OpenAI GPT-4 and Google Gemini for intelligent decision making
"""

import openai
import google.generativeai as genai
from typing import Dict, List, Optional, Any
import json
import logging
from app.core.config import settings
import asyncio
from datetime import datetime

logger = logging.getLogger(__name__)


class AIBrain:
    """
    Core AI Brain - Central intelligence system
    Combines GPT-4 and Gemini for optimal decision making
    """
    
    def __init__(self):
        self.openai_client = None
        self.gemini_model = None
        self.ready = False
        self.knowledge_base = {}
        self.execution_history = []
        
    async def initialize(self):
        """Initialize AI models"""
        try:
            # Initialize OpenAI
            if settings.OPENAI_API_KEY:
                openai.api_key = settings.OPENAI_API_KEY
                self.openai_client = openai.AsyncOpenAI(api_key=settings.OPENAI_API_KEY)
                logger.info("? OpenAI GPT-4 initialized")
            
            # Initialize Gemini
            if settings.GEMINI_API_KEY:
                genai.configure(api_key=settings.GEMINI_API_KEY)
                self.gemini_model = genai.GenerativeModel('gemini-pro')
                logger.info("? Google Gemini initialized")
            
            self.ready = True
            logger.info("?? Core AI Brain initialized successfully")
            
        except Exception as e:
            logger.error(f"? Failed to initialize AI Brain: {e}")
            self.ready = False
    
    def is_ready(self) -> bool:
        """Check if AI Brain is ready"""
        return self.ready
    
    async def process_chat_message(
        self,
        message: str,
        user_id: str,
        context: Optional[Dict] = None
    ) -> Dict[str, Any]:
        """
        Process a chat message from user
        Returns AI response with actions and confidence
        """
        if not self.ready:
            return {
                "message": "AI Brain is initializing, please wait...",
                "actions": [],
                "confidence": 0.0
            }
        
        context = context or {}
        
        try:
            # Use GPT-4 for complex reasoning and intent understanding
            gpt_response = await self._process_with_gpt4(message, context)
            
            # Use Gemini for quick validation and additional insights
            gemini_response = await self._process_with_gemini(message, context)
            
            # Combine responses intelligently
            combined_response = self._combine_responses(gpt_response, gemini_response)
            
            # Store in history
            self.execution_history.append({
                "timestamp": datetime.now().isoformat(),
                "user_id": user_id,
                "message": message,
                "response": combined_response
            })
            
            return combined_response
            
        except Exception as e:
            logger.error(f"Error processing chat message: {e}")
            return {
                "message": f"??? ??? ????? ?????? ???????: {str(e)}",
                "actions": [],
                "confidence": 0.0
            }
    
    async def _process_with_gpt4(self, message: str, context: Dict) -> Dict:
        """Process message with OpenAI GPT-4"""
        if not self.openai_client:
            return {"message": "", "intent": "unknown", "confidence": 0.0}
        
        system_prompt = """??? ????? ??? ????? ?? ????? ????? MikroTik RouterOS.
?????:
1. ??? ????? ???????? ?????? ????? (Intent)
2. ????? ??????? RouterOS ???? ??????
3. ?????? ???? ??????? ???????
4. ????? ?????? ?????? ?????? ?????? ????

????? ??????:
- ?? ???? ????? ????? ???? ?????
- ?????? dry-run ??? ??????? ??????
- ??? ???? ????????

??? ???????? ?? ?????????? ??? ??? ????????."""

        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": message}
                ],
                temperature=0.7,
                max_tokens=1000
            )
            
            content = response.choices[0].message.content
            
            # Parse response to extract intent and actions
            intent = self._extract_intent(content)
            actions = self._extract_actions(content)
            confidence = self._calculate_confidence(content, intent)
            
            return {
                "message": content,
                "intent": intent,
                "actions": actions,
                "confidence": confidence
            }
            
        except Exception as e:
            logger.error(f"GPT-4 processing error: {e}")
            return {"message": "", "intent": "error", "confidence": 0.0}
    
    async def _process_with_gemini(self, message: str, context: Dict) -> Dict:
        """Process message with Google Gemini for quick validation"""
        if not self.gemini_model:
            return {"validation": True, "suggestions": []}
        
        try:
            prompt = f"""???? ?? ????? ?????? ??????? ?? MikroTik:
    {message}
    
    ???:
    1. ???? ???? ?? ??? ?????
    2. ???????? ?????
    3. ??????? ???? ?? ????"""
            
            # Run in executor for compatibility
            loop = asyncio.get_event_loop()
            response = await loop.run_in_executor(
                None,
                lambda: self.gemini_model.generate_content(prompt)
            )
            
            return {
                "validation": True,
                "suggestions": response.text if response.text else []
            }
            
        except Exception as e:
            logger.error(f"Gemini processing error: {e}")
            return {"validation": True, "suggestions": []}
    
    def _combine_responses(self, gpt_response: Dict, gemini_response: Dict) -> Dict:
        """Intelligently combine GPT-4 and Gemini responses"""
        combined_message = gpt_response.get("message", "")
        
        # Add Gemini suggestions if available
        if gemini_response.get("suggestions"):
            combined_message += f"\n\n?? ????????: {gemini_response['suggestions']}"
        
        return {
            "message": combined_message,
            "actions": gpt_response.get("actions", []),
            "confidence": gpt_response.get("confidence", 0.0),
            "intent": gpt_response.get("intent", "unknown")
        }
    
    def _extract_intent(self, text: str) -> str:
        """Extract intent from AI response"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ["monitor", "??????", "status", "????"]):
            return "monitor"
        elif any(word in text_lower for word in ["script", "?????", "command", "???"]):
            return "execute"
        elif any(word in text_lower for word in ["fix", "?????", "repair", "??"]):
            return "fix"
        elif any(word in text_lower for word in ["analyze", "?????", "check", "???"]):
            return "analyze"
        else:
            return "general"
    
    def _extract_actions(self, text: str) -> List[Dict]:
        """Extract actionable commands from AI response"""
        actions = []
        
        # Look for RouterOS script patterns
        if "/ip" in text or "/interface" in text or "/system" in text:
            # Extract script block
            script_start = text.find("```")
            if script_start != -1:
                script_end = text.find("```", script_start + 3)
                if script_end != -1:
                    script = text[script_start + 3:script_end].strip()
                    actions.append({
                        "type": "routeros_script",
                        "script": script,
                        "requires_confirmation": True
                    })
        
        return actions
    
    def _calculate_confidence(self, text: str, intent: str) -> float:
        """Calculate confidence score for the response"""
        confidence = 0.7  # Base confidence
        
        # Increase confidence if script is found
        if "/ip" in text or "/interface" in text:
            confidence += 0.2
        
        # Increase confidence if intent is clear
        if intent != "unknown":
            confidence += 0.1
        
        return min(confidence, 1.0)
    
    async def generate_routeros_script(
        self,
        intent: str,
        parameters: Dict[str, Any]
    ) -> str:
        """Generate RouterOS script based on intent and parameters"""
        if not self.openai_client:
            return ""
        
        prompt = f"""???? ????? MikroTik RouterOS ????? ??????:
?????: {intent}
?????????: {json.dumps(parameters, ensure_ascii=False)}

???????:
1. ?????? ???? RouterOS Script ???????
2. ??? ??????? ????????
3. ???? ?? ??????
4. ?????? ???? ?????????

??????? ??? ???? ???:"""

        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a MikroTik RouterOS scripting expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.3,
                max_tokens=500
            )
            
            script = response.choices[0].message.content.strip()
            
            # Clean script (remove markdown if present)
            if script.startswith("```"):
                script = script.split("```")[1]
                if script.startswith("routeros") or script.startswith("ros"):
                    script = script.split("\n", 1)[1]
                script = script.strip()
            
            return script
            
        except Exception as e:
            logger.error(f"Error generating RouterOS script: {e}")
            return ""
    
    async def analyze_network_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze network monitoring data and provide insights"""
        if not self.openai_client:
            return {"insights": [], "recommendations": []}
        
        prompt = f"""??? ?????? ?????? ??????? ???? ??????:
{json.dumps(data, ensure_ascii=False, indent=2)}

???:
1. ??????? ????????
2. ??????????
3. ???????? ???????
4. ?? ????? ?????"""

        try:
            response = await self.openai_client.chat.completions.create(
                model=settings.OPENAI_MODEL,
                messages=[
                    {"role": "system", "content": "You are a network analysis expert."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5,
                max_tokens=800
            )
            
            analysis = response.choices[0].message.content
            
            return {
                "insights": [analysis],
                "recommendations": self._extract_recommendations(analysis)
            }
            
        except Exception as e:
            logger.error(f"Error analyzing network data: {e}")
            return {"insights": [], "recommendations": []}
    
    def _extract_recommendations(self, text: str) -> List[str]:
        """Extract recommendations from analysis text"""
        recommendations = []
        lines = text.split("\n")
        
        for line in lines:
            if any(keyword in line.lower() for keyword in ["recommend", "?????", "suggest", "??????"]):
                recommendations.append(line.strip())
        
        return recommendations
    
    async def cleanup(self):
        """Cleanup resources"""
        self.ready = False
        logger.info("?? AI Brain cleaned up")
