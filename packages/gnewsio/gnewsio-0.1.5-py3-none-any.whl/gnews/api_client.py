import requests
import logging
from urllib.parse import urlencode
from gnews.response_handler import ResponseObject

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class APIClient:
    BASE_URL = "https://gnews.io/api/v4/top-headlines"

    def __init__(self, api_key, category=None, country=None, language=None, from_date=None, to_date=None):
        self.api_key = api_key
        self.category = category
        self.country = country
        self.language = language
        self.from_date = from_date
        self.to_date = to_date

    def fetch_top_headlines(self):
        params = {
            "apikey": self.api_key,
            "category": self.category,
            "country": self.country,
            "lang": self.language,
            "from": self.from_date,
            "to": self.to_date,
            "expand": "content",
            "max": 10  # Example: you can limit the number of articles returned
        }

        # Remove None values from params
        params = {key: value for key, value in params.items() if value is not None}

        response = requests.get(self.BASE_URL, params=params)
        full_url = f"{self.BASE_URL}?{urlencode(params)}"
        logger.info(f"Fetching data from URL: {full_url}")

        if response.status_code == 200:
            return ResponseObject.from_json(response.json())
        elif response.status_code in [400, 401, 403]:
            raise Exception(f"Client error: {response.status_code}")
        elif response.status_code == 429:
            raise Exception("Rate limit exceeded (HTTP 429). Please retry after some time.")
        elif response.status_code >= 500:
            raise Exception(f"Server error: {response.status_code}")
        else:
            response.raise_for_status()
