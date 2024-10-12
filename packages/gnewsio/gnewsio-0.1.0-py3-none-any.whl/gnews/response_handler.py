class Article:
    def __init__(self, title, description, content, url, image, published_at, source_name, source_url):
        self.title = title
        self.description = description
        self.content = content
        self.url = url
        self.image = image
        self.published_at = published_at
        self.source_name = source_name
        self.source_url = source_url

    @classmethod
    def from_json(cls, data):
        source = data.get('source', {})
        return cls(
            title=data.get("title"),
            description=data.get("description"),
            content=data.get("content"),
            url=data.get("url"),
            image=data.get("image"),
            published_at=data.get("publishedAt"),
            source_name=source.get("name"),
            source_url=source.get("url")
        )

    def __str__(self):
        return (f"Title: {self.title}\n"
                f"Description: {self.description}\n"
                f"URL: {self.url}\n"
                f"Image URL: {self.image}\n"
                f"Content: {self.content}")


class ResponseObject:
    def __init__(self, total_articles, articles):
        self.total_articles = total_articles
        self.articles = articles

    @classmethod
    def from_json(cls, data):
        articles = [Article.from_json(article) for article in data["articles"]]
        return cls(
            total_articles=data["totalArticles"],
            articles=articles
        )
