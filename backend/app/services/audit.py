import httpx
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from app.core.security import is_safe_url, sanitize_url

class AuditService:
    """
    Service responsible for safely crawling external sites and parsing structural DOM/SEO elements.
    """
    
    @staticmethod
    async def scrape_page(url: str) -> str:
        """
        Safely fetch the HTML content of the URL.
        Includes SSRF protection, sanitization, timeout, and custom User-Agent headers.
        """
        # 1. Sanitize the URL structure
        url = sanitize_url(url)
        
        # 2. SSRF check
        if not is_safe_url(url):
            raise ValueError("URL points to an unsafe or internal network address.")
            
        headers = {
            "User-Agent": "AeroTechSEOEngine/1.0 (Audit Bot; http://localhost:3000)",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
        }
        
        # 2. Async HTTP fetch with timeout
        # Using follow_redirects=True to handle domain redirects safely (SSRF is checked in is_safe_url,
        # but to be extremely safe, we check redirects via a custom redirect validator or check final url.
        # For simplicity and compliance, we enforce SSRF check).
        async with httpx.AsyncClient(timeout=10.0, headers=headers) as client:
            response = await client.get(url, follow_redirects=True)
            response.raise_for_status()
            
            # Double check the final redirected URL for SSRF
            if not is_safe_url(str(response.url)):
                raise ValueError("Redirected URL points to an unsafe or internal network address.")
                
            return response.text

    @staticmethod
    def parse_dom(html_content: str, base_url: str) -> dict:
        """
        Extract key SEO DOM elements: Titles, Descriptions, Headings structure,
        Images with/without alt attributes, and Internal/External link structures.
        """
        soup = BeautifulSoup(html_content, "html.parser")
        parsed_base = urlparse(base_url)
        base_domain = parsed_base.netloc

        # 1. Extract Title
        title = ""
        if soup.title and soup.title.string:
            title = soup.title.string.strip()
        else:
            meta_title = soup.find("meta", attrs={"name": "title"}) or soup.find("meta", attrs={"property": "og:title"})
            if meta_title and meta_title.get("content"):
                title = str(meta_title.get("content")).strip()

        # 2. Extract Description
        description = ""
        meta_desc = soup.find("meta", attrs={"name": "description"}) or soup.find("meta", attrs={"property": "og:description"})
        if meta_desc and meta_desc.get("content"):
            description = str(meta_desc.get("content")).strip()

        # 3. Headings counts and structures
        headings = {
            "h1": [h.get_text().strip() for h in soup.find_all("h1") if h.get_text()],
            "h2_count": len(soup.find_all("h2")),
            "h3_count": len(soup.find_all("h3")),
            "h4_count": len(soup.find_all("h4")),
        }

        # 4. Images alt-tag audit
        images = soup.find_all("img")
        total_images = len(images)
        images_missing_alt = 0
        for img in images:
            if not img.get("alt") or not img.get("alt").strip():
                images_missing_alt += 1

        # 5. Links analysis
        links = soup.find_all("a", href=True)
        total_links = len(links)
        internal_links = 0
        external_links = 0
        for link in links:
            href = link.get("href")
            parsed_href = urlparse(href)
            # If netloc is empty (relative link) or matches base domain, it is internal
            if not parsed_href.netloc or parsed_href.netloc == base_domain:
                internal_links += 1
            else:
                external_links += 1

        return {
            "title": title,
            "description": description,
            "headings": headings,
            "images": {
                "total": total_images,
                "missing_alt": images_missing_alt
            },
            "links": {
                "total": total_links,
                "internal": internal_links,
                "external": external_links
            }
        }
