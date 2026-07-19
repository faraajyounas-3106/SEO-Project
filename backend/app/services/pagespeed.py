import httpx
import asyncio
from app.core.config import settings

class PageSpeedService:
    """
    Service to fetch Core Web Vitals and Lighthouse Performance metrics 
    via Google PageSpeed Insights API.
    """
    
    API_URL = "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"

    @classmethod
    async def fetch_strategy_metrics(cls, url: str, strategy: str) -> dict:
        """
        Fetch metrics for a single strategy (mobile or desktop).
        """
        params = {
            "url": url,
            "strategy": strategy,
            "category": "performance",
        }
        if settings.PAGESPEED_API_KEY:
            params["key"] = settings.PAGESPEED_API_KEY

        # Wrap in try-except with timeout as per rules.md
        try:
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(cls.API_URL, params=params)
                # Handle rate limits (429) or other errors
                response.raise_for_status()
                data = response.json()
                
                # Parse scores and metrics safely
                lh = data.get("lighthouseResult", {})
                categories = lh.get("categories", {})
                perf_category = categories.get("performance", {})
                score = int((perf_category.get("score") or 0) * 100)

                audits = lh.get("audits", {})
                
                # LCP (Largest Contentful Paint)
                lcp_audit = audits.get("largest-contentful-paint", {})
                lcp = float(lcp_audit.get("numericValue", 0) / 1000.0) # convert ms to seconds

                # CLS (Cumulative Layout Shift)
                cls_audit = audits.get("cumulative-layout-shift", {})
                cls = float(cls_audit.get("numericValue", 0))

                # TBT (Total Blocking Time)
                tbt_audit = audits.get("total-blocking-time", {})
                tbt = float(tbt_audit.get("numericValue", 0)) # in ms

                return {
                    "score": score,
                    "lcp": lcp,
                    "cls": cls,
                    "tbt": tbt,
                    "raw_report": data  # to store in JSONB
                }
        except httpx.HTTPStatusError as e:
            # Check for rate limiting
            if e.response.status_code == 429:
                # Custom error dictionary or message
                raise ValueError("Google PageSpeed API rate limit exceeded.") from e
            raise ValueError(f"Google PageSpeed API returned HTTP error: {e.response.status_code}") from e
        except Exception as e:
            raise ValueError(f"Failed to fetch PageSpeed metrics for {strategy}: {str(e)}") from e

    @classmethod
    async def fetch_all_metrics(cls, url: str) -> dict:
        """
        Fetch both desktop and mobile metrics in parallel.
        """
        # Run mobile and desktop audits concurrently
        mobile_task = cls.fetch_strategy_metrics(url, "mobile")
        desktop_task = cls.fetch_strategy_metrics(url, "desktop")
        
        mobile_res, desktop_res = await asyncio.gather(mobile_task, desktop_task, return_exceptions=False)
        
        return {
            "mobile": mobile_res,
            "desktop": desktop_res
        }
