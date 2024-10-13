from typing import Any

from pyquery import PyQuery

from ..utils import parse_html
from .base import BaseSearchItem, BaseSearchResponse


class EHentaiItem(BaseSearchItem):
    """Represents a single e-hentai gallery item.

    Holds details of a gallery from an e-hentai reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        thumbnail: URL of the gallery's thumbnail.
        url: URL of the gallery.
        title: Title of the gallery.
        type: Category of the gallery.
        date: Date when the gallery was posted.
        tags: List of tags associated with the gallery.
    """

    def __init__(self, data: PyQuery, **kwargs: Any):
        """Initializes an EHentaiItem with data from a search result.

        Args:
            data: A PyQuery instance containing the search result item's data.
        """
        super().__init__(data, **kwargs)

    def _parse_data(self, data: PyQuery, **kwargs) -> None:
        """Parse search result data."""
        self.type: str = ""
        self.date: str = ""
        self.tags: list[str] = []
        self._arrange(data)

    def _arrange(self, data: PyQuery) -> None:
        """Organize gallery data.

        Extracts and sets the gallery's title, URL, thumbnail, type, date and tags.

        Args:
            data: A PyQuery instance containing the gallery's data.
        """
        glink = data.find(".glink")
        self.title = glink.text()
        if glink.parent("div"):
            self.url = glink.parent("div").parent("a").attr("href")
        else:
            self.url = glink.parent("a").attr("href")
        thumbnail = (
            data.find(".glthumb img")
            or data.find(".gl1e img")
            or data.find(".gl3t img")
        )
        self.thumbnail = thumbnail.attr("data-src") or thumbnail.attr("src")
        _type = data.find(".cs") or data.find(".cn")
        self.type = _type.eq(0).text()
        self.date = data.find("[id^='posted']").eq(0).text()
        self.tags = [
            i.attr("title") for i in data.find("div[class=gt],div[class=gtl]").items()
        ]


class EHentaiResponse(BaseSearchResponse):
    """Encapsulates an e-hentai reverse image search response.

    Contains the complete response from an e-hentai reverse image search operation.

    Attributes:
        origin: The raw response data.
        raw: List of EHentaiItem instances for each gallery item.
        url: URL to the search result page.
    """

    def __init__(self, resp_data: str, resp_url: str, **kwargs: Any):
        """Initializes with the response text and URL.

        Args:
            resp_text: The text of the response.
            resp_url: URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: str, **kwargs: Any) -> None:
        """Parse search response data."""
        data = parse_html(resp_data)
        self.origin: PyQuery = data
        if "No unfiltered results" in resp_data:
            self.raw = []
        elif tr_items := data.find(".itg").children("tr").items():
            self.raw = [EHentaiItem(i) for i in tr_items if i.children("td")]
        else:
            gl1t_items = data.find(".itg").children(".gl1t").items()
            self.raw = [EHentaiItem(i) for i in gl1t_items]
