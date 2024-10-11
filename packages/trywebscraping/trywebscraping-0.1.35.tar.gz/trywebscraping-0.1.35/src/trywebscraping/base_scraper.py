from typing import Optional, Dict, Any, List
import json

from .query import Query
from .utils import (
    convert_html_to_markdown,
    get_metadata,
    get_clean_html,
    html_to_json,
    most_similar_algorithm,
)


class BaseScraper:
    _MAX_REDIRECTS = 5
    _LOCAL_PROXY_HOST = "5.78.43.227"
    _LOCAL_PROXY_PORT = 8899

    def __init__(self, url: str):
        self.url = url
        self.html: Optional[str] = None
        self.query_handler = Query()

    def get_html(self) -> str:
        raise NotImplementedError("Subclasses must implement get_html method")

    def get_markdown(self, algorithm: Optional[str] = None) -> str:
        html = self.get_html()
        if algorithm == "MostSimilar":
            return most_similar_algorithm(html)
        else:
            return convert_html_to_markdown(html)

    def get_metadata(self) -> Dict[str, str]:
        html = self.get_html()
        return get_metadata(html)

    def get_clean_html(self) -> str:
        html = self.get_html()
        return get_clean_html(html)

    def get_json(self, include_unique_selectors: bool = False) -> str:
        html = self.get_html()
        json_data = html_to_json(html, include_unique_selectors)
        return json.dumps(json_data, ensure_ascii=False, indent=4)

    def query(self, selector: str, key: Optional[str] = None) -> "BaseScraper":
        self.query_handler.add_query(selector, key)
        return self

    def extract(self, extraction: Dict[str, str]) -> "BaseScraper":
        self.query_handler.set_extraction(extraction)
        return self

    def limit(self, limit: int) -> "BaseScraper":
        self.query_handler.set_limit(limit)
        return self

    def get_data(self) -> List[Any]:
        html = self.get_html()
        return self.query_handler.execute(html)

    def __str__(self) -> str:
        return str(self.get_data())

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(data={self.get_data()})"