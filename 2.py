import requests
import os
from dotenv import load_dotenv

load_dotenv()

API = os.getenv("NEWS_API_KEY")
URL = "https://newsapi.org/v2/everything"


class NewsClient:
    def __init__(self, topic, language, page_size, api=API, url=URL):
        self.topic = topic
        self.language = language
        self.page_size = page_size
        self.api = api
        self.url = url

    def get_news(self):
        prompt = {
            "q": f"{self.topic}",
            "apiKey": f"{self.api}",
            "language": f"{self.language}",
            "pageSize": f"{self.page_size}",
        }
        try:
            response = requests.get(self.url, params=prompt)
            data = response.json()
            articles = data.get("articles", [])
            articles_dict = {}

            for i, article in enumerate(articles, 1):
                articles_dict[i] = {
                    "title": article.get("title"),
                    "author": article.get("author"),
                    "source": article.get("source"),
                    "url": article.get("url"),
                }
            return articles_dict
        except requests.exceptions.RequestException:
            return {"Ошибка": "Нет подключения к интернету"}

    def news_report(self):
        articles_dict = self.get_news()
        if "Ошибка" in articles_dict:
            print(f"{articles_dict['Ошибка']}")
        print("-" * 30)
        for i, info in articles_dict.items():
            print(f"Статья №{i}")
            print(f"Название статьи: {info['title']}")
            print(f"Автор: {info['author']}")
            print(f"Ресурс: {info['source']['name']}")
            print(f"URL: {info['url']}")
            print("-" * 30)


if __name__ == "__main__":
    news = NewsClient("Apple", "ru", "5")
    news.news_report()
