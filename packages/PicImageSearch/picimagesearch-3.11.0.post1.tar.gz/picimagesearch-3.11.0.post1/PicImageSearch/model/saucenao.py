from typing import Any, Optional

from .base import BaseSearchItem, BaseSearchResponse


class SauceNAOItem(BaseSearchItem):
    """Represents a single SauceNAO search result item.

    Holds details of a result from a SauceNAO reverse image search.

    Attributes:
        origin: The raw data of the search result item.
        similarity: Similarity score of the search result to the query image.
        thumbnail: URL of the thumbnail image.
        index_id: Index number of the result source on SauceNAO.
        index_name: Name of the result source index.
        hidden: Indicator of NSFW content; non-zero values indicate hidden content.
        title: Title of the work associated with the image.
        url: Direct URL to the work, when available.
        ext_urls: External URLs for additional information or resources related to the image.
        author: Author/creator/name of the user responsible for the work.
        author_url: URL to the profile or page of the author/creator.
        source: Specific source of the search result.
    """

    def __init__(self, data: dict[str, Any], **kwargs: Any):
        """Initializes a SauceNAOItem with data from a search result.

        Args:
            data: A dictionary containing the search result data.
        """
        super().__init__(data, **kwargs)

    def _parse_data(self, data: dict[str, Any], **kwargs: Any) -> None:
        """Parse search result data."""
        header = data["header"]
        self.similarity = float(header["similarity"])
        self.thumbnail = header["thumbnail"]
        self.index_id = header["index_id"]
        self.index_name = header["index_name"]
        self.hidden = header.get("hidden", 0)
        self.title = self._get_title(data["data"])
        self.url = self._get_url(data["data"])
        self.ext_urls = data["data"].get("ext_urls", [])
        self.author = self._get_author(data["data"])
        self.author_url = self._get_author_url(data["data"])
        self.source = data["data"].get("source", "")

    @staticmethod
    def _get_title(data: dict[str, Any]) -> str:
        """Extracts the title from result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The title of the work as derived from the result data.
        """
        return (
            next(
                (
                    data[i]
                    for i in [
                        "title",
                        "material",
                        "jp_name",
                        "eng_name",
                        "source",
                        "created_at",
                    ]
                    if i in data and data[i]
                ),
                "",
            )
            or ""
        )

    @staticmethod
    def _get_url(data: dict[str, Any]) -> str:
        """Constructs the URL to the work using the result data.

        Args:
            data: A dictionary containing the search result data.

        Returns:
            The URL to the work referenced in the search result.
        """
        if "pixiv_id" in data:
            return f'https://www.pixiv.net/artworks/{data["pixiv_id"]}'
        elif "pawoo_id" in data:
            return f'https://pawoo.net/@{data["pawoo_user_acct"]}/{data["pawoo_id"]}'
        elif "getchu_id" in data:
            return f'https://www.getchu.com/soft.phtml?id={data["getchu_id"]}'
        elif "ext_urls" in data:
            return data["ext_urls"][0]  # type: ignore
        return ""

    @staticmethod
    def _get_author(data: dict[str, Any]) -> str:
        """Extracts the author information from the result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The name of the author or the user handle associated with the work.
        """
        return (
            next(
                (
                    (
                        ", ".join(data[i])
                        if i == "creator" and isinstance(data[i], list)
                        else data[i]
                    )
                    for i in [
                        "author",
                        "member_name",
                        "creator",
                        "twitter_user_handle",
                        "pawoo_user_display_name",
                        "author_name",
                        "user_name",
                        "artist",
                        "company",
                    ]
                    if i in data and data[i]
                ),
                "",
            )
            or ""
        )

    @staticmethod
    def _get_author_url(data: dict[str, Any]) -> str:
        """Constructs the URL to the author's profile or page using the result data.

        Args:
            data: A dictionary containing the parsed data for an individual result.

        Returns:
            The URL to the author's profile or related page.
        """
        if "pixiv_id" in data:
            return f'https://www.pixiv.net/users/{data["member_id"]}'
        elif "seiga_id" in data:
            return f'https://seiga.nicovideo.jp/user/illust/{data["member_id"]}'
        elif "nijie_id" in data:
            return f'https://nijie.info/members.php?id={data["member_id"]}'
        elif "bcy_id" in data:
            return f'https://bcy.net/u/{data["member_id"]}'
        elif "tweet_id" in data:
            return f'https://twitter.com/intent/user?user_id={data["twitter_user_id"]}'
        elif "pawoo_user_acct" in data:
            return f'https://pawoo.net/@{data["pawoo_user_acct"]}'
        return str(data.get("author_url", ""))


class SauceNAOResponse(BaseSearchResponse):
    """Encapsulates a SauceNAO reverse image search response.

    Contains the complete response from a SauceNAO reverse image search operation.

    Attributes:
        status_code: HTTP status code received from SauceNAO.
        raw: List of SauceNAOItem instances for each search result.
        origin: The raw response data.
        short_remaining: Queries remaining under the 30-second rate limit.
        long_remaining: Queries remaining under the daily rate limit.
        user_id: User ID of the SauceNAO API account used for the request, if any.
        account_type: Account type of the SauceNAO API account used for the request, if any.
        short_limit: Maximum queries allowed under the 30-second rate limit.
        long_limit: Maximum queries allowed under the daily rate limit.
        status: Status of the response, indicating success or error types.
        results_requested: Number of results requested in the search query.
        search_depth: Number of database indexes searched by SauceNAO.
        minimum_similarity: Minimum similarity score required for results.
        results_returned: Number of results returned in the search response.
        url: URL to the search result page.
    """

    def __init__(self, resp_data: dict[str, Any], resp_url: str, **kwargs):
        """Initializes with the response data.

        Args:
            resp_data: A dictionary containing the parsed response data from SauceNAO.
            resp_url: URL to the search result page.
        """
        super().__init__(resp_data, resp_url, **kwargs)

    def _parse_response(self, resp_data: dict[str, Any], **kwargs) -> None:
        """Parse search response data."""
        self.status_code: int = resp_data["status_code"]
        header = resp_data["header"]
        results = resp_data.get("results", [])
        self.raw: list[SauceNAOItem] = [SauceNAOItem(i) for i in results]
        self.short_remaining: Optional[int] = header.get("short_remaining")
        self.long_remaining: Optional[int] = header.get("long_remaining")
        self.user_id: Optional[int] = header.get("user_id")
        self.account_type: Optional[int] = header.get("account_type")
        self.short_limit: Optional[str] = header.get("short_limit")
        self.long_limit: Optional[str] = header.get("long_limit")
        self.status: Optional[int] = header.get("status")
        self.results_requested: Optional[int] = header.get("results_requested")
        self.search_depth: Optional[int] = header.get("search_depth")
        self.minimum_similarity: Optional[float] = header.get("minimum_similarity")
        self.results_returned: Optional[int] = header.get("results_returned")
        self.url: str = (
            f"https://saucenao.com/search.php?url="
            f'https://saucenao.com{header.get("query_image_display")}'
        )
