import requests
from bs4 import BeautifulSoup
from termcolor import colored

def fetcher(url):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
        "Accept-Language": "es-ES,es;q=0.9,en;q=0.8",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1"
    }
    try:
        response = requests.get(f"https://{url}", headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except requests.RequestException:
        return None
    

def extract_urls_from_sitemap(sitemap_content):
    urls = []
    if sitemap_content:
        soup = BeautifulSoup(sitemap_content, "xml")
        for loc in soup.find_all("loc"):
            urls.append(loc.text)
    return urls


def find_sitemaps(url):
    urls = []
    sitemaps_names = [
    "/sitemap.xml",
    "/sitemap_index.xml",
    "/sitemap-index.xml",
    "/sitemap-0.xml",
    "/sitemap1.xml",
    "/sitemap2.xml",
    "/sitemap3.xml",
    "/sitemap-1.xml",
    "/sitemap-2.xml",
    "/sitemap-3.xml",
    "/sitemap_posts.xml",
    "/sitemap_pages.xml",
    "/sitemap_categories.xml",
    "/sitemap_tags.xml",
    "/sitemap_products.xml",
    "/sitemap_authors.xml",
    "/sitemap_news.xml",
    "/sitemap_images.xml",
    "/sitemap_video.xml",
    "/wp-sitemap.xml",
    "/wp-sitemap-posts-post-1.xml",
    "/wp-sitemap-posts-page-1.xml",
    "/wp-sitemap-taxonomies-category-1.xml",
    "/wp-sitemap-users-1.xml",
    "/sitemap_products_1.xml",
    "/sitemap_collections_1.xml",
    "/sitemap_blogs_1.xml",
    "/sitemap_pages_1.xml",
    "/news-sitemap.xml",
    "/video-sitemap.xml",
    "/image-sitemap.xml",
    "/mobile-sitemap.xml",
    "/local-sitemap.xml",
    "/product-sitemap.xml",
    "/category-sitemap.xml",
    "/page-sitemap.xml",
    "/post-sitemap.xml",
    "/tag-sitemap.xml",
    "/author-sitemap.xml",
    "/sitemaps/sitemap.xml",
    "/sitemaps/sitemap_index.xml",
    "/sitemap/sitemap.xml",
    "/sitemap/index.xml",
    "/feed/sitemap.xml",
]
    for sitemap in sitemaps_names:
        print(colored(f"[i] checking for sitemap: {sitemap}", "grey", attrs=["bold"]).ljust(80), end="\r", flush=True)
        try:
            fetcher_response = fetcher(f'{url}{sitemap}')
            if fetcher_response:
                urls.extend(extract_urls_from_sitemap(fetcher_response))
        except requests.RequestException:
            pass
    if urls:
        print(" " * 100, end="\r", flush=True) 
        return sorted(urls)
    return None

def find_robots(url):
    try:
       fetcher_response = fetcher(f'{url}/robots.txt')
       if fetcher_response:
           return fetcher_response
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return None