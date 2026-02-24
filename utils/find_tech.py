import requests
from typing import List, TypedDict


class HtmlContent(TypedDict):
    html: str
    headers: dict[str, str]


class TechInfo(TypedDict):
    technologies: List[str]
    headers:dict[str, str]


def get_html(url: str) -> HtmlContent | str:
    """
    Fetches the HTML content and specific security/technology headers from a given URL.

    Args:
        url (str): The target URL or domain.

    Returns:
        dict | str: A dictionary containing 'html' and 'headers' if successful, 
                     otherwise an error message string.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }   

    headers_to_check = [
    "X-Powered-By", "Server", "X-AspNet-Version", 
    "Strict-Transport-Security",
    "X-Frame-Options", "X-Content-Type-Options"
    ]

    headeres_found = {}

    try:
        full_url = url if url.startswith(('http://', 'https://')) else f"https://{url}"
        
        response = requests.get(full_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        for header in headers_to_check:
            value = response.headers.get(header, "Not Found")
            headeres_found[header] = value
        return {"html": response.text, "headers": headeres_found}
    except requests.exceptions.RequestException as e:
        return f"Error fetching HTML content: {e}"


def find_tech(url: str) -> TechInfo | str:
    """
    Analyzes the HTML content and headers of a URL to identify the underlying technology stack.

    Args:
        url (str): The target URL to analyze.

    Returns:
        dict | str: A dictionary containing 'technologies' (list) and 'headers',
                     or an error message string if the analysis fails.
    """
    try:
        content = get_html(url)
        if isinstance(content, str):
            return content  
        html = content["html"].lower()
        headers = content["headers"]

        results = []

        if "_astro/" in html:
            results.append("Astro")
        
        if "gtag" in html:
            results.append("Google Analytics")

        if "elementor-section" in html:
            results.append("Elementor")

        if "https://www.googletagmanager.com" in html:
            results.append("Google Tag Manager")

        if "text-" in html or "bg-" in html or "border-"  in html:
            results.append("Tailwind CSS")

        if any(x in html for x in ["wp-content", "wp-includes", "elementor/", "ver-wp"]):
            results.append("WordPress")

        if any(x in html for x in ["__next_f", "/_next/static", "next-hal-stack"]):
            results.append("Next.js")

        if "data-shopify" in html or "cdn.shopify.com" in html:
            results.append("Shopify")

        react_indicators = ["id='root'", 'id="root"', "react-dom", "__react", "data-reactroot"]
        if any(x in html for x in react_indicators):
            results.append("React")

        styled_indicators = ["data-styled=", "data-styled-components", "sc-component-id"]
        if any(x in html for x in styled_indicators):
            results.append("Styled Components")
            
        if not results:
            results.append("Unknown Technology")

        return {"technologies": results, "headers": headers}
    
    except Exception as e:
        return f"Error analyzing technology: {e}"