from pathlib import Path
from typing import Any, Optional, Union

from ..model import EHentaiResponse
from ..utils import read_file
from .base import BaseSearchEngine


class EHentai(BaseSearchEngine):
    """API client for the EHentai image search engine.

    Used for performing reverse image searches using EHentai service.

    Attributes:
        base_url: The base URL for EHentai searches.
        is_ex: If True, search on exhentai.org; otherwise, use e-hentai.org.
        covers: A flag to search only for covers.
        similar: A flag to enable similarity scanning.
        exp: A flag to include results from expunged galleries.
    """

    def __init__(
        self,
        is_ex: bool = False,
        covers: bool = False,
        similar: bool = True,
        exp: bool = False,
        **request_kwargs: Any,
    ):
        """Initializes an EHentai API client with specified configurations.

        Args:
            base_url: The base URL for EHentai searches.
            is_ex: If True, search on exhentai.org; otherwise, use e-hentai.org.
            covers: If True, search only for covers; otherwise, False.
            similar: If True, enable similarity scanning; otherwise, False.
            exp: If True, include results from expunged galleries; otherwise, False.
            **request_kwargs: Additional arguments for network requests.
        """
        base_url = "https://upld.exhentai.org" if is_ex else "https://upld.e-hentai.org"
        super().__init__(base_url, **request_kwargs)
        self.is_ex = is_ex
        self.covers = covers
        self.similar = similar
        self.exp = exp

    async def search(
        self,
        url: Optional[str] = None,
        file: Union[str, bytes, Path, None] = None,
        **kwargs: Any,
    ) -> EHentaiResponse:
        """Performs a reverse image search on EHentai.

        Supports searching by image URL or by uploading an image file.

        Requires either 'url' or 'file' to be provided.

        Args:
            url: URL of the image to search.
            file: Local image file (path or bytes) to search.

        Returns:
            EHentaiResponse: Contains search results and additional information.

        Raises:
            ValueError: If neither 'url' nor 'file' is provided.

        Note:
            Searching on exhentai.org requires logged-in status via cookies in `EHentai.request_kwargs`.
        """
        await super().search(url, file, **kwargs)

        endpoint = "upld/image_lookup.php" if self.is_ex else "image_lookup.php"
        data: dict[str, Any] = {"f_sfile": "File Search"}

        if url:
            files: dict[str, Any] = {"sfile": await self.download(url)}
        else:
            files = {"sfile": read_file(file)}

        if self.covers:
            data["fs_covers"] = "on"
        if self.similar:
            data["fs_similar"] = "on"
        if self.exp:
            data["fs_exp"] = "on"

        resp = await self._make_request(
            method="post",
            endpoint=endpoint,
            data=data,
            files=files,
        )

        return EHentaiResponse(resp.text, resp.url)
