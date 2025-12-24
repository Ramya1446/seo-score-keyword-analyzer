import streamlit as st
from scripts.keyword_utils import get_page_text, keyword_density, get_trending_keywords, keyword_match_percentage

st.set_page_config(page_title="SEO Analyzer", page_icon="🔍")

st.title("🔍 SEO Analyzer & Keyword Recommender")

# Inputs
url = st.text_input("Enter Website URL", "https://www.python.org/")
target_keyword = st.text_input("Enter Target Keyword", "coding")

if st.button("Analyze"):
    # Extract page text
    text = get_page_text(url)

    if not text:
        st.error("Could not fetch website content.")
    else:
        # Word count
        word_count = len(text.split())

        # Keyword density
        density = keyword_density(text, target_keyword)

        # Trending keywords
        trending_keywords = get_trending_keywords(text, top_n=10)

        # Keyword match %
        match_percent = keyword_match_percentage(target_keyword, trending_keywords)

        # SEO Score (weighted example)
        score = 0
        score += min(word_count / 1000, 1) * 30
        score += min(density / 2, 1) * 20
        score += (match_percent / 100) * 20
        score += 30  # placeholder for meta/alt checks

        # Display results
        st.subheader("📊 Extracted Features")
        st.json({
            "Word_Count": word_count,
            "Keyword_Density (%)": round(density, 2),
        })

        st.subheader("Predicted SEO Score")
        st.write(f"**{score:.2f} / 100**")

        st.subheader("Keyword Match %")
        st.write(f"**{match_percent:.2f}%**")

        st.subheader("🔥 Trending Keywords")
        st.write(trending_keywords)
