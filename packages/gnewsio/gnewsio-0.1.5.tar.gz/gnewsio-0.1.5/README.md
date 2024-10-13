# GNews IO Client

A Python client for the gnews.io APIs that supports category, country, and language filtering.

### Installation

```cmd
pip install gnewsio
```

### Usage
```python
from gnews.client_builder import Gnews
from gnews.enums import Category, Country, Language
from datetime import datetime

gnews_client = (Gnews(api_key="YOUR-API-KEY")
                .set_category(Category.NATION)
                .set_country(Country.UNITED_STATES)
                .set_language(Language.ENGLISH)
                .set_from_date(datetime(2024, 10, 11, 0, 0, 0))  # YYYY-MM-DDThh:mm:ssZ
                .set_to_date(datetime(2024, 10, 11, 23, 59, 59))  # YYYY-MM-DDThh:mm:ssZ
                .build())

try:
    # Fetch the top headlines
    response = gnews_client.fetch_top_headlines()
    print(f"Total Articles: {response.total_articles}")
    for article in response.articles:
        print(article)
except Exception as e:
    print(f"Error: {e}")
```