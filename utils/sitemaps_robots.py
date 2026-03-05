from typing import List

import requests
from bs4 import BeautifulSoup
from termcolor import colored
import time
import re




def fetcher(url :str) -> str | None:
    """
    Performs a basic GET request to a domain and returns its raw HTML content.

    Args:
        url (str): The domain or URL to fetch (prepended with https://).

    Returns:
        str | None: The raw HTML source code if successful, or None if the request fails.
    """
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        response = requests.get(f"https://{url}" if not "https://" in url else url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None

def extract_sitemap_list(url:str) -> List[str] | None:
    
    robots = find_robots(url)

    if not robots:
        return None

    pattern = r'\S*sitemap\S*'
    
    matches = re.findall(pattern, robots)
    
    if matches:
        sitemaps_list = [ f"/{item.split("/")[3]}" for item in list(set(matches)) ]
        return sitemaps_list
    else:
        return None

def extract_urls_from_sitemap(sitemap_content :str) -> list[str]:
    """
    Parses XML sitemap content to extract all listed URLs (loc tags).

    Args:
        sitemap_content (str): The raw XML content of a sitemap.

    Returns:
        list[str]: A list of all URLs found within the sitemap.
    """
    urls = []
    if sitemap_content:
        soup = BeautifulSoup(sitemap_content, "xml")
        for loc in soup.find_all("loc"):
            urls.append(loc.text)
    return urls


def find_robots(url :str) -> str | None:
    """
    Attempts to retrieve the robots.txt file from the target domain.

    Args:
        url (str): The target domain or base URL.

    Returns:
        str | None: The raw content of robots.txt if found, otherwise None.
    """
    try:
       fetcher_response = fetcher(f'{url}/robots.txt')
       if fetcher_response:
           return fetcher_response
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return None


def find_sitemaps(url:str, rate_limit:int | float | None = None) -> list[str] | None:
    """
    Brute-forces common sitemap locations and extracts all discovered URLs.

    Args:
        url (str): The target domain or base URL.
        rate_limit (int | float | None): Delay in seconds between requests.

    Returns:
        list[str] | None: A sorted list of all unique URLs found, or None if no sitemaps exist.
    """

    sitemaps_names = extract_sitemap_list(url)

    if not sitemaps_names:
        return None

    urls = []
#     sitemaps_names = [
#     "/sitemap.xml",
#     "/sitemap_index.xml",
#     "/sitemap-index.xml",
#     "/sitemap-0.xml",
#     "/sitemap1.xml",
#     "/sitemap2.xml",
#     "/sitemap3.xml",
#     "/sitemap-1.xml",
#     "/sitemap-2.xml",
#     "/sitemap-3.xml",
#     "/sitemap_posts.xml",
#     "/sitemap_pages.xml",
#     "/sitemap_categories.xml",
#     "/sitemap_tags.xml",
#     "/sitemap_products.xml",
#     "/sitemap_authors.xml",
#     "/sitemap_news.xml",
#     "/sitemap_images.xml",
#     "/sitemap_video.xml",
#     "/wp-sitemap.xml",
#     "/wp-sitemap-posts-post-1.xml",
#     "/wp-sitemap-posts-page-1.xml",
#     "/wp-sitemap-taxonomies-category-1.xml",
#     "/wp-sitemap-users-1.xml",
#     "/sitemap_products_1.xml",
#     "/sitemap_collections_1.xml",
#     "/sitemap_blogs_1.xml",
#     "/sitemap_pages_1.xml",
#     "/news-sitemap.xml",
#     "/video-sitemap.xml",
#     "/image-sitemap.xml",
#     "/mobile-sitemap.xml",
#     "/local-sitemap.xml",
#     "/product-sitemap.xml",
#     "/category-sitemap.xml",
#     "/page-sitemap.xml",
#     "/post-sitemap.xml",
#     "/tag-sitemap.xml",
#     "/author-sitemap.xml",
#     "/sitemaps/sitemap.xml",
#     "/sitemaps/sitemap_index.xml",
#     "/sitemap/sitemap.xml",
#     "/sitemap/index.xml",
#     "/feed/sitemap.xml",
# ]
    for i,sitemap in enumerate(sitemaps_names, start=1):
        print(colored(f"[i] checking for sitemap: {sitemap} ({i}/{len(sitemaps_names)}) ", "grey", attrs=["bold"]).ljust(80), end="\r", flush=True)
        if rate_limit:
            time.sleep(rate_limit)
        try:
            fetcher_response = fetcher(f'{url}{sitemap}')
            if fetcher_response:
                urls.extend(extract_urls_from_sitemap(fetcher_response))
        except requests.RequestException:
            pass
    if urls:
       
        final_urls = []

        for i,item in enumerate(urls, start=1):
            if "sitemap" in item:
                print(colored(f"[i] checking for sitemap: {item} ({i}/{len(urls)}) ", "grey", attrs=["bold"]).ljust(80), end="\r", flush=True)
                fetcher_response = fetcher(item)
                if fetcher_response:
                    final_urls.extend(extract_urls_from_sitemap(fetcher_response))
            else:
                final_urls.extend(item)
        
        print(" " * 100, end="\r", flush=True) 


        return sorted(final_urls)
    return None

