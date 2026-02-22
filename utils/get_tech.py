import requests
from typing import List

import requests

def get_html(url: str) -> str:
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }   

    headers_to_check = [
    "X-Powered-By", "Server", "X-AspNet-Version", 
    "Strict-Transport-Security", "Content-Security-Policy",
    "X-Frame-Options", "X-Content-Type-Options"
]

    try:
        full_url = url if url.startswith(('http://', 'https://')) else f"https://{url}"
        
        response = requests.get(full_url, headers=headers, timeout=10)
        response.raise_for_status()
        
        for header in headers_to_check:
            value = response.headers.get(header, "Not Found")
            print(f"{header}: {value}")
        return response.text
    except requests.exceptions.RequestException as e:
        return f"Error fetching HTML content: {e}"


def get_tech(url: str) -> List[str] | str:
    try:
        raw_html = get_html(url)
        html = raw_html.lower()

        results = []

        if "_astro/" in html:
            results.append("Astro")

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

        return results
    
    except Exception as e:
        return f"Error analyzing technology: {e}"