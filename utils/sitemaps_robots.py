import requests
from bs4 import BeautifulSoup

def fetcher(url):
    try:
        response = requests.get(f"https://{url}", timeout=10)
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
    sitemaps_names = ["/sitemap.xml", "/sitemap_index.xml", "/sitemap-0.xml", "/sitemap-index.xml"]
    for sitemap in sitemaps_names:
        try:
            fetcher_response = fetcher(f'{url}{sitemap}')
            if fetcher_response:
                urls.extend(extract_urls_from_sitemap(fetcher_response))
        except requests.RequestException as e:
            pass
    if urls:
        return urls

def find_robots(url):
    try:
       fetcher_response = fetcher(f'{url}/robots.txt')
       if fetcher_response:
           return fetcher_response
    except requests.RequestException as e:
        print(f"Error fetching robots.txt: {e}")
        return None