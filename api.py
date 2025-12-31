from fastapi import FastAPI
from scrape_ai_news import fetch_ai_news, summarize_headlines

app = FastAPI(
    title="AI News Summarizer API",
    version="1.0.0",
    description="Fetches latest AI news and returns a summarized digest."
)

@app.get("/health")
def health_check():
    return {"status": "ok"}

@app.get("/ai-news")
def get_ai_news():
    """
    Fetch an AI news article, summarize it with OpenAI,
    and return both the raw scraped text and the formatted summary.
    """
    # fetch_ai_news returns: (article_paragraphs, link)
    article_paragraphs, link = fetch_ai_news()

    # handle failure / empty scrape
    if not article_paragraphs or not link:
        return {
            "status": "error",
            "message": "Could not fetch AI news.",
            "article_paragraphs": [],
            "link": link,
            "summary": None,
        }

    # summarize using OpenAI
    summary_text = summarize_headlines(article_paragraphs, link)

    return {
        "status": "ok",
        "link": link,
        "article_paragraphs": article_paragraphs,
        "summary": summary_text,  # the WhatsApp-style summary string
    }
