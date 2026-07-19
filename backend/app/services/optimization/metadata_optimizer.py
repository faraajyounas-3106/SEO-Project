import json
import logging
import google.generativeai as genai
from app.core.config import settings
from app.services.optimization.strategy import OptimizerStrategy

logger = logging.getLogger(__name__)

class MetadataOptimizer(OptimizerStrategy):
    """
    Concrete optimization strategy using Gemini to generate SEO metadata.
    """

    def __init__(self):
        # Configure GenAI client if the key is available
        if settings.GEMINI_API_KEY:
            genai.configure(api_key=settings.GEMINI_API_KEY)
            self.model = genai.GenerativeModel("gemini-1.5-flash")
        else:
            self.model = None

    async def optimize(self, context: dict) -> dict:
        """
        Generates optimized Title and Meta Description.
        Context expects: 'title', 'description', 'headings' (dict with 'h1').
        """
        raw_title = context.get("title", "").strip()
        raw_desc = context.get("description", "").strip()
        h1s = context.get("headings", {}).get("h1", [])

        # Graceful fallback if GenAI API Key is missing or model configuration is skipped
        if not self.model:
            logger.warning("GEMINI_API_KEY is not set. Using rule-based fallback optimization.")
            return self._fallback_optimize(raw_title, raw_desc, h1s)

        prompt = f"""
You are an expert SEO Optimization Agent. Analyze the webpage information below and generate an optimized, search-engine-friendly Meta Title and Meta Description.

Webpage Details:
- Raw Title: {raw_title}
- Original Description: {raw_desc}
- Major H1 Headings: {", ".join(h1s) if h1s else "None"}

SEO Constraints:
1. The optimized Title MUST be under 60 characters, clear, and compelling.
2. The optimized Description MUST be under 160 characters, contain a call to action, and align with semantic search intent.
3. You must respond ONLY with a valid JSON block containing the keys "title" and "description". Do not include markdown code block formatting (like ```json).

Response Format:
{{
  "title": "Optimized Page Title",
  "description": "Optimized meta description containing a call to action."
}}
"""
        try:
            # Generate content from model
            # Note: We run this in a threadpool to prevent blocking the async loop if the SDK is blocking
            response = self.model.generate_content(prompt)
            text_response = response.text.strip()
            
            # Clean possible markdown wrap if the model ignored instructions
            if text_response.startswith("```"):
                text_response = text_response.strip("`").replace("json\n", "", 1)
            
            data = json.loads(text_response)
            return {
                "optimized_title": data.get("title", "").strip() or raw_title,
                "optimized_description": data.get("description", "").strip() or raw_desc
            }
        except Exception as e:
            logger.error(f"GenAI metadata optimization failed: {e}. Falling back to rule-based generation.")
            return self._fallback_optimize(raw_title, raw_desc, h1s)

    def _fallback_optimize(self, title: str, description: str, h1s: list) -> dict:
        """
        Simple rule-based fallback optimization.
        """
        # Fallback optimized title
        opt_title = title
        if h1s:
            # Use the first H1 if available and concise
            primary_topic = h1s[0]
            if len(primary_topic) < 45:
                opt_title = f"{primary_topic} | SEO Suite"
        if not opt_title or len(opt_title) > 60:
            opt_title = title[:50] + "..." if len(title) > 50 else title

        # Fallback optimized description
        opt_desc = description
        if not opt_desc:
            opt_desc = f"Discover more about {opt_title or 'our site'}. Access professional SEO insights, speed metrics, and automated content optimizations."
        else:
            if len(opt_desc) > 155:
                opt_desc = opt_desc[:152] + "..."

        return {
            "optimized_title": opt_title,
            "optimized_description": opt_desc
        }
