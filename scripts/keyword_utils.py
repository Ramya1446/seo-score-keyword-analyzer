import re
import requests
from bs4 import BeautifulSoup
from collections import Counter
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer

ps = PorterStemmer()
stop_words = set(stopwords.words("english"))

# Fetch and clean page text
def get_page_text(url):
    try:
        response = requests.get(url, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")

        # Only extract from main content
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        text = soup.get_text(separator=" ")
        return re.sub(r"\s+", " ", text.strip())
    except Exception as e:
        print(f"Error fetching {url}: {e}")
        return ""

# Keyword density
def keyword_density(text, keyword):
    words = re.findall(r"\b\w+\b", text.lower())
    stemmed_words = [ps.stem(w) for w in words]
    stemmed_keyword = ps.stem(keyword.lower())

    total_words = len(stemmed_words)
    keyword_count = stemmed_words.count(stemmed_keyword)

    return (keyword_count / total_words * 100) if total_words else 0

# Trending keywords
def get_trending_keywords(text, top_n=10):
    words = re.findall(r"\b\w+\b", text.lower())
    filtered = [w for w in words if w not in stop_words and len(w) > 2]
    freq = Counter(filtered)
    return [word for word, _ in freq.most_common(top_n)]

# Keyword match percentage (target keyword vs trending list)
def keyword_match_percentage(target_keyword, trending_keywords):
    if not trending_keywords:
        return 0
    match_count = sum(1 for kw in trending_keywords if target_keyword.lower() in kw.lower())
    return (match_count / len(trending_keywords)) * 100
