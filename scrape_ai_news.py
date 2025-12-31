import requests
from bs4 import BeautifulSoup
from datetime import datetime
from openai import OpenAI
import os
from datetime import datetime
import time
import random


client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))



# 1. Scrape AI news headlines from a sample site (you can change URLs later)
def fetch_ai_news():
    headers = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Accept-Language": "en-US,en;q=0.9",
    }


    url = "https://techcrunch.com/category/artificial-intelligence/"  # example AI news page
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}")
        return []   # so your summarizer prints "No AI news found today.

    if response.status_code != 200:
        print(f"Failed to fetch page, status code: {response.status_code}")
        return []

    soup = BeautifulSoup(response.text, "html.parser")

    articles = []

    # This CSS selector may need adjustment depending on the site structure
    for item in soup.select("h3 a")[:5]:  # first 5 articles
        title = item.get_text(strip=True)
        link = item.get("href")
        if link and link.startswith("/"):
            link = "https://techcrunch.com/" + link
        if title == '' or title in articles:
            continue
        if title != '' or title not in articles:
            articles.append({"title": title, "link": link})
    
    print (articles)

    article = random.choice(articles)

    print (f"===Random article===\n {artile}")


    try:
        response_article = requests.get(article[link], headers=headers, timeout=10)
        response_article.raise_for_status()
    except Exception as e:
        print(f"Error fetching page: {e}")
        return []   # so your summarizer prints "No AI news found today.

    if response_article.status_code != 200:
        print(f"Failed to fetch page, status code: {response_article.status_code}")
        return []

    
    soup_article = BeautifulSoup(response_article.text, "html.parser")

    article_summary_helper = []
    for item in soup_article.select("h2 p"):
        heading = item.get_text(strip=True)
        desc = item.get_text(strip=True)
        artile_summary_helper.append({"heading":heading,"desc":desc})
    print (f"===Article summary===\n {artile_summary_helper}")

    return article_summary_helper


# 2. Very simple "summary" function (placeholder for real LLM later)

def summarize_headlines(article):
    if not article:
        return "No AI news found today."

    # Build a block of text from the scraped articles
    headlines_text = article

    # We’ll use the current date in the title
    today_str = datetime.now().strftime("%d %b %Y")

    # This is the PROMPT that goes into `input=`
    prompt = f""" You are an assistant that summarizes AI news for a busy person.
    You will be given a list of AI news headlines with links.
    Return the result in EXACTLY this structure (no extra text before or after):
    <AI News title>
    4-5 bullet points that briefly summarize the key updates across all headlines
    <article link(s) on separate lines>
    More details:
        - The first line should be something like: AI News — {today_str}.
        - The second line should Title, the format will be Title: {headlines_text}
        - The next lines should be 8-10 short bullet points (start each with • ) All the bullet points should be insightful, not generic.
        - After the bullets, add the article links.
        - Do NOT invent links; only use the links I provided.
    Here are the headlines and links:
    {headlines_text}"""

    response = client.responses.create(
        model="gpt-4.1-mini",
        input=prompt
    )

    # Get the generated text from the response
    summary_text = response.output_text.strip()
    return summary_text





def main():
    print("Fetching AI news...")
    articles = fetch_ai_news()
    summary = summarize_headlines(articles)

    print("\n===== SUMMARY TO SEND =====\n")
    print(summary)
    print("\n===========================\n")

    # Later: instead of print, send this summary to WhatsApp / Telegram


if __name__ == "__main__":
    main()
