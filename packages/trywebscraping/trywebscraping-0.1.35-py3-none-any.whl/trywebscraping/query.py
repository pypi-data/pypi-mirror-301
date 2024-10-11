from typing import List, Dict, Any, Optional
from bs4 import BeautifulSoup


class Query:
    def __init__(self):
        self.queries: List[Dict[str, Any]] = []
        self.current_query: Dict[str, Any] = {}

    def add_query(self, selector: str, key: Optional[str] = None) -> None:
        if self.current_query:
            self.queries.append(self.current_query)

        self.current_query = {
            "selector": selector,
            "extraction": None,
            "limit": None,
            "key": key,
        }

    def set_extraction(self, extraction: Dict[str, str]) -> None:
        self.current_query["extraction"] = extraction

    def set_limit(self, limit: int) -> None:
        self.current_query["limit"] = limit

    def execute(self, html: str) -> List[List[Dict[str, Any]]]:
        soup = BeautifulSoup(html, "lxml")

        merged_results: List[List[Dict[str, Any]]] = []

        if self.current_query:
            self.queries.append(self.current_query)

        for query in self.queries:
            selector = query.get("selector")
            extraction = query.get("extraction")
            limit = query.get("limit")
            key = query.get("key")

            elements = soup.select(selector)

            if extraction:
                extracted = [self._extract_data(el, extraction) for el in elements]
            else:
                extracted = [{"text": el.text.strip()} for el in elements]

            if limit:
                extracted = extracted[:limit]

            if key:
                found = False

                for result in merged_results:
                    if result and result[0].get("key") == key:
                        for i, item in enumerate(extracted):
                            if i < len(result):
                                result[i].update(item)
                            else:
                                result.append(item)

                        found = True

                        break
                if not found:
                    merged_results.append([{"key": key, **item} for item in extracted])

            else:
                merged_results.append(extracted)

        for result in merged_results:
            if result and result[0].get("key") == key:
                for item in result:
                    item.pop("key", None)

        return merged_results

    def _extract_data(self, element, extraction: Dict[str, str]) -> Dict[str, str]:
        result = {}

        for key, selector in extraction.items():
            if "@" in selector:
                selector, attr = selector.split("@")
                selected = element.select_one(selector)
                result[key] = selected[attr] if selected else ""
            else:
                selected = element.select_one(selector)
                result[key] = selected.text.strip() if selected else ""

        return result