import requests
from bs4 import BeautifulSoup
import re

def extract_features(url, keyword):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Meta Title & Description
        title = soup.title.string if soup.title else ""
        meta_desc = soup.find("meta", attrs={"name": "description"})
        meta_desc_content = meta_desc["content"] if meta_desc else ""

        # Word Count
        text = soup.get_text()
        word_count = len(text.split())

        # Keyword Density
        keyword_count = text.lower().count(keyword.lower())
        keyword_density = (keyword_count / word_count) * 100 if word_count > 0 else 0

        # Alt Tag %
        images = soup.find_all("img")
        alt_tags = [img for img in images if img.get("alt")]
        alt_tag_percent = (len(alt_tags) / len(images) * 100) if images else 0

        return {
            "Word_Count": word_count,
            "Keyword_Density": round(keyword_density, 2),
            "Meta_Title_Length": len(title),
            "Meta_Desc_Length": len(meta_desc_content),
            "Alt_Tag_Percent": round(alt_tag_percent, 2)
        }
    except Exception as e:
        print("Error extracting features:", e)
        return None
