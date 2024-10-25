from airflow import Dataset
from airflow.decorators import dag, task
from pendulum import datetime
from openai import OpenAI
from airflow.utils.email import send_email
import pandas as pd
import yfinance as yf
import os

OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
FROM_EMAIL = os.getenv('AIRFLOW__SMTP__SMTP_MAIL_FROM')


def get_openai_response(prompt, model="gpt-4o"):
    client = OpenAI()
    client.api_key = OPENAI_API_KEY
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[{"role": "system", "content": "You are a professional financial news analyst, highly experienced in summarizing stock market trends and financial news concisely."},
                      {"role": "user", "content": prompt}]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error calling OpenAI API: {e}")
        return None


default_args = {
    "owner": "Yeonguk",
    "retries": 1,
    "email": [FROM_EMAIL],
    "email_on_failure": True,
    "email_on_retry": True
}

@dag(
    start_date=datetime(2024, 1, 1),
    schedule="@daily",
    catchup=False,
    doc_md=__doc__,
    default_args=default_args,
    tags=["example"],
)
def news_evaluation_example():
    @task(
        outlets=[Dataset("current_news")]
    )
    def extract_news(**context) -> list[dict]:
        try:
            symbol = 'AAPL'
            company = yf.Ticker(symbol)
            news_data = company.news
            print(f"Fetched {len(news_data)} news articles for {symbol}.")

        except:
            print("API currently not available, using hardcoded data instead.")
            news_data = [
                {"title": "Apple’s New Password Manager Is Free. That’s Just One Reason to Use It.",
                 "link": "https://finance.yahoo.com/m/62e670bf-3843-3952-ba84-b85bd46698ef/apple%E2%80%99s-new-password-manager.html",
                 "relatedTickers": ["AAPL"]},
                {"title": "Jim Cramer’s Bullish Stance on Apple Inc (NASDAQ:AAPL): Insights from Mike Sievert",
                 "link": "https://finance.yahoo.com/news/jim-cramer-bullish-stance-apple-002626037.html",
                 "relatedTickers": ["AAPL"]},
                {"title": "With the Launch of iPhone 16, How Are Billionaires Investing in Apple Stock?",
                 "link": "https://finance.yahoo.com/m/a3d71a3b-cce4-3a61-9d66-7596b27450ce/with-the-launch-of-iphone-16%2C.html",
                 "relatedTickers": ["AAPL"]},
            ]
            print(f"Using {len(news_data)} hardcoded news articles.")

        extracted_news = [
            {
                "title": article.get("title"),
                "link": article.get("link"),
                "relatedTickers": article.get("relatedTickers")
            }
            for article in news_data
        ]
        
        return extracted_news

    @task
    def summarize_news(extracted_news: list[dict]) -> list[dict]:
        summarized_news = []
        for article in extracted_news:
            prompt = f"Please summarize this news article in one sentence: {article['title']}"
            summary = get_openai_response(prompt)
            article["summary"] = summary if summary else "Summary not available."
            summarized_news.append(article)
        return summarized_news
    
    @task
    def evaluate_news(summarized_news: list[dict]) -> list[dict]:
        evaluated_news = []
        for article in summarized_news:
            prompt = (
                f"Evaluate the sentiment of the following article and provide a score (-10 to 10) and brief reasoning:\n"
                f"Title: {article['title']}\nSummary: {article['summary']}"
            )
            sentiment = get_openai_response(prompt)
            article["sentiment"] = sentiment if sentiment else "Sentiment not available."
            evaluated_news.append(article)
        return evaluated_news
    
    @task
    def email_news(evaluated_news: list[dict]):
        try:
            # HTML 형식으로 뉴스 내용 구성
            content = """
            <html>
                <body>
                    <h2>Daily News Evaluation</h2>
                    <table border="1" cellpadding="5" cellspacing="0">
                        <tr>
                            <th>Title</th>
                            <th>Summary</th>
                            <th>Sentiment</th>
                            <th>Link</th>
                        </tr>
            """
            for article in evaluated_news:
                content += f"""
                    <tr>
                        <td>{article['title']}</td>
                        <td>{article['summary']}</td>
                        <td>{article['sentiment']}</td>
                        <td><a href="{article['link']}">Read more</a></td>
                    </tr>
                """
            content += """
                    </table>
                </body>
            </html>
            """
            send_email(
                to=FROM_EMAIL,
                subject="Daily News Evaluation",
                html_content=content
            )
            print("Email sent successfully.")
        except Exception as e:
            print(f"Error sending email: {e}")

    extracted_news = extract_news()
    summarized_news = summarize_news(extracted_news)
    evaluated_news = evaluate_news(summarized_news)
    email_news(evaluated_news)

news_evaluation_example()
