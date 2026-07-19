from app.services.optimization.strategy import OptimizerStrategy

class SchemaOptimizer(OptimizerStrategy):
    """
    Concrete optimization strategy to construct valid JSON-LD schema markup.
    """

    async def optimize(self, context: dict) -> dict:
        """
        Builds a standard JSON-LD schema dictionary based on DOM extraction details.
        """
        title = context.get("title", "AeroTech Web Page").strip()
        desc = context.get("description", "").strip()
        url = context.get("url", "https://example.com").strip()
        h1s = context.get("headings", {}).get("h1", [])

        # Default Schema template
        schema = {
            "@context": "https://schema.org",
            "@type": "WebPage",
            "name": title,
            "url": url
        }
        if desc:
            schema["description"] = desc

        # Upgrade to Article schema if the page contains a distinct headline (H1)
        if h1s:
            schema["@type"] = "Article"
            schema["headline"] = h1s[0]
            schema["mainEntityOfPage"] = {
                "@type": "WebPage",
                "@id": url
            }

        return {
            "json_ld_schema": schema
        }
