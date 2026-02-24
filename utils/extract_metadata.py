from bs4 import BeautifulSoup
from typing import TypedDict


class Metadata(TypedDict):
    title: str
    description: str


def extract_metadata(html_content: str) -> Metadata:
    """
    Extracts basic metadata from HTML without additional requests.
    """
    soup = BeautifulSoup(html_content, 'html.parser')
    meta_description = soup.find("meta", {"name": "description"})
    description = "No Description or Dynamic Description"
    if meta_description:
        content = meta_description.get("content")
        if isinstance(content, list):
            description = content[0] if content else "No Description or Dynamic Description"
        else:
            description = content if content else "No Description or Dynamic Description"
    return {
        "title": soup.title.string.strip() if soup.title and soup.title.string else "No Title or Dynamic Title",
        "description": description
    }