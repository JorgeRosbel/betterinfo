import requests
from typing import List, TypedDict
from .extract_metadata import extract_metadata, Metadata
import re


class HtmlContent(TypedDict):
    html: str
    headers: dict[str, str]


class TechInfo(TypedDict):
    technologies: List[str]
    headers:dict[str, str]
    metadata: Metadata
    plugins: List[dict[str, str]]


def get_wordpress_plugins(html: str) -> list[dict]:
    """
    Extrae los plugins de WordPress usados en un sitio web
    a partir del HTML plano de la página.

    Args:
        html: Contenido HTML de la página como string.

    Returns:
        Lista de dicts con { name, version, source } de cada plugin encontrado.
    """
    plugins: dict[str, dict] = {}

    # --- Patrón 1: rutas en /wp-content/plugins/<plugin-name>/ ---
    # Cubre <script src>, <link href>, <img src>, etc.
    pattern_path = re.compile(
        r'/wp-content/plugins/([a-zA-Z0-9_-]+)(?:/[^"\'>\s]*)?'
        r'(?:["\'\s].*?(?:ver|version)[=\s]+["\']?([0-9][0-9a-zA-Z._-]*))?',
        re.IGNORECASE,
    )

    for match in pattern_path.finditer(html):
        name = match.group(1)
        version = match.group(2)  # puede ser None

        if name not in plugins:
            plugins[name] = {
                "name": name,
                "version": version or "unknown",
                "source": "wp-content/plugins path",
            }
        elif version and plugins[name]["version"] == "unknown":
            plugins[name]["version"] = version

    # --- Patrón 2: ?ver=X.X.X en assets conocidos de plugins ---
    # Captura la versión de assets ya detectados por el patrón anterior
    pattern_ver = re.compile(
        r'/wp-content/plugins/([a-zA-Z0-9_-]+)/[^"\'>\s]*\?(?:[^"\'>\s]*&)?ver=([0-9][0-9a-zA-Z._-]*)',
        re.IGNORECASE,
    )
    for match in pattern_ver.finditer(html):
        name = match.group(1)
        version = match.group(2)
        if name in plugins and plugins[name]["version"] == "unknown":
            plugins[name]["version"] = version

    # --- Patrón 3: comentarios HTML generados por plugins ---
    # Ej: <!-- This site is using Plugin Name 1.2.3 -->
    pattern_comment = re.compile(
        r'<!--[^-]*?plugin[s]?\s*[:\-]?\s*([a-zA-Z0-9][a-zA-Z0-9_\- ]{2,40}?)(?:\s+v?([0-9][0-9a-zA-Z._-]*))?(?:\s+active|\s+enabled|-->)',
        re.IGNORECASE,
    )
    for match in pattern_comment.finditer(html):
        raw_name = match.group(1).strip()
        version = match.group(2)
        slug = raw_name.lower().replace(" ", "-")
        if slug and slug not in plugins:
            plugins[slug] = {
                "name": raw_name,
                "version": version or "unknown",
                "source": "HTML comment",
            }

    # --- Patrón 4: generator meta tag (algunos plugins lo usan) ---
    pattern_meta = re.compile(
        r'<meta[^>]+name=["\']generator["\'][^>]+content=["\']([^"\']+)["\']',
        re.IGNORECASE,
    )
    for match in pattern_meta.finditer(html):
        content = match.group(1)
       
        if "wordpress" in content.lower():
            continue
        
        parts = content.rsplit(" ", 1)
        name = parts[0].strip()
        version = parts[1] if len(parts) == 2 and re.match(r"[0-9]", parts[1]) else "unknown"
        slug = name.lower().replace(" ", "-")
        if slug not in plugins:
            plugins[slug] = {
                "name": name,
                "version": version,
                "source": "meta generator",
            }

    return list(plugins.values())


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
        
        metadata = extract_metadata(content["html"])
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

        return {"technologies": results, "headers": headers, "metadata": metadata , "plugins": get_wordpress_plugins(html)}
    
    except Exception as e:
        return f"Error analyzing technology: {e}"