import os
from datetime import datetime
from gnews.enums import Category, Country, Language
from gnews.api_client import APIClient


class Gnews:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_key = api_key or os.getenv("GNEWS_IO__API_KEY")
        if not self.api_key:
            raise ValueError(
                "API key must be provided either directly or through the environment variable GNEWS_IO__API_KEY.")

        self.category = None
        self.country = None
        self.language = None
        self.from_date = None
        self.to_date = None

    def set_category(self, category: Category):
        self.category = category.value
        return self

    def set_country(self, country: Country):
        self.country = country.value
        return self

    def set_language(self, language: Language):
        self.language = language.value
        return self

    def set_from_date(self, from_date: datetime):
        self.from_date = from_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return self

    def set_to_date(self, to_date: datetime):
        self.to_date = to_date.strftime("%Y-%m-%dT%H:%M:%SZ")
        return self

    def build(self):
        # Passing all set parameters to the APIClient
        return APIClient(
            api_key=self.api_key,
            category=self.category,
            country=self.country,
            language=self.language,
            from_date=self.from_date,
            to_date=self.to_date
        )
