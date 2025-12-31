import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openai import OpenAI
import os
import random

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

# 1. Scrape AI news headlines from TechCrunch
def fetch_ai_news():
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                      "AppleWebKit/537.36 (KHTML, like Gecko) "
                      "Chrome/120.0.0.0 Safari/537.36",
        "Accept-Language": "en-US,en;q=0.9",
    }

    url = "https://techcrunch.com/category/artificial-intelligence/"

    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching listing page: {e}")
        return [], None   # always return (article_text_list, link)

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    # grab first few article links
    for item in soup.select("h3 a")[:5]:
        title = item.get_text(strip=True)
        link = item.get("href")

        if not link or not title:
            continue

        if link.startswith("/"):
            link = "https://techcrunch.com" + link

        articles.append({"title": title, "link": link})

    print("Articles found on listing page:")
    print(articles)

    if not articles:
        return [], None

    # pick a random article
    article = random.choice(articles)

    print(f"=== Random article ===\n{article}")
    print(f"=== Random article link ===\n{article['link']}")

    # fetch the article page
    try:
        response_article = requests.get(article["link"], headers=headers, timeout=10)
        response_article.raise_for_status()
    except Exception as e:
        print(f"Error fetching article page: {e}")
        return [], article["link"]

    soup_article = BeautifulSoup(response_article.text, "html.parser")

    # collect all paragraphs from the article
    article_summary_helper = []
    for item in soup_article.select("p"):
        text = item.get_text(strip=True)
        if text:
            article_summary_helper.append(text)

    print("=== Article summary helper ===")
    print(article_summary_helper)

    return article_summary_helper, article["link"]


# 2. Summarize the article using OpenAI
def summarize_headlines(article_paragraphs, link):
    if not article_paragraphs:
        return "No AI news found today."

    # combine paragraphs into one block of text
    body_text = "\n".join(article_paragraphs)

    today_str = datetime.now().strftime("%d %b %Y")

    prompt = f"""You are an assistant that summarizes one AI news article for a busy person.

Return the result in EXACTLY this structure (no extra text before or after):

<AI News title>
4-5 bullet points that briefly summarize the key updates
<article link>

More details:
- The first line should be: AI News — {today_str}
- The next line should be: Title: (infer a short, clear title from the article text)
- Then 4-5 short bullet points (start each with • ). All bullet points should be insightful, not generic.
- Last line: the article link: {link}
- Do NOT invent facts or links.

Here is the article body:

{body_text}
"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt,
    )

    summary_text = response.output_text.strip()
    return summary_text


def main():
    print("Fetching AI news...")
    article_paragraphs, link = fetch_ai_news()

    if not article_paragraphs or not link:
        print("\n===== SUMMARY TO SEND =====\n")
        print("No AI news found today.")
        print("\n===========================\n")
        return

    summary = summarize_headlines(article_paragraphs, link)

    print("\n===== SUMMARY TO SEND =====\n")
    print(summary)
    print("\n===========================\n")


if __name__ == "__main__":
    main()
