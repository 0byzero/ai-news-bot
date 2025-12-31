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
    Fetch AI news, summarize them with OpenAI,
    and return both the raw articles and the formatted summary.
    """
    articles = fetch_ai_news()

    if not articles:
        return {
            "status": "error",
            "message": "Could not fetch AI news.",
            "articles": [],
            "summary": None,
        }

    summary_text = summarize_headlines(articles)

    return {
        "status": "ok",
        "summary": summary_text, # the WhatsApp-style summary string
    }
