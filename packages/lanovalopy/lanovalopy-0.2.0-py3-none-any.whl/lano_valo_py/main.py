import aiohttp
from typing import List, Optional, Dict, Any
from urllib.parse import urlencode, quote

from lano_valo_py.valo_types import (
    APIResponseModel,
    RateLimit,
    ErrorObject,
    FetchOptionsModel,
)
from lano_valo_py.valo_types.valo_models import (
    AccountFetchByPUUIDOptionsModel,
    AccountFetchOptionsModel,
    GetContentFetchOptionsModel,
    GetCrosshairFetchOptionsModel,
    GetFeaturedItemsFetchOptionsModel,
    GetLeaderboardOptionsModel,
    GetLifetimeMMRHistoryFetchOptionsModel,
    GetMMRByPUUIDFetchOptionsModel,
    GetMMRFetchOptionsModel,
    GetMMRHistoryByPUUIDFetchOptionsModel,
    GetMMRHistoryFetchOptionsModel,
    GetMatchFetchOptionsModel,
    GetMatchesByPUUIDFetchOptionsModel,
    GetMatchesFetchOptionsModel,
    GetRawFetchOptionsModel,
    GetStatusFetchOptionsModel,
    GetVersionFetchOptionsModel,
    GetWebsiteFetchOptionsModel,
)


class LanoValoPy:
    BASE_URL = "https://api.henrikdev.xyz/valorant"

    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.headers = {"User-Agent": "unofficial-valorant-api/python/1.0"}
        if self.token:
            self.headers["Authorization"] = self.token

    async def _parse_body(self, body: Any) -> Any:
        if "errors" in body:
            return body["errors"]
        return body["data"] if body.get("status") else body

    async def _parse_response(
        self, response: aiohttp.ClientResponse, url: str
    ) -> APIResponseModel:
        try:
            data = await response.json()
        except aiohttp.ContentTypeError:
            data = await response.text()

        ratelimits = None
        if "x-ratelimit-limit" in response.headers:
            ratelimits = RateLimit(
                used=int(response.headers.get("x-ratelimit-limit", 0)),
                remaining=int(response.headers.get("x-ratelimit-remaining", 0)),
                reset=int(response.headers.get("x-ratelimit-reset", 0)),
            )

        error = None
        if not response.ok:
            api_response = APIResponseModel(
                status=response.status,
                data=None,
                ratelimits=ratelimits,
                error=None,
                url=url,
            )
            try:
                error = ErrorObject(message=data.get("errors", "Unknown error")[0].get("message", "Unknown error"))
                api_response.error = error
                return api_response
                 
            except AttributeError:
                error = ErrorObject(message=str(data))
                api_response.error = error
                return api_response
        
        api_response = APIResponseModel(
            status=response.status,
            data=None
            if "application/json" not in response.headers.get("Content-Type", "")
            else await self._parse_body(data),
            ratelimits=ratelimits,
            error=error,
            url=url,
        )
        return api_response

    def _validate(self, input_data: Dict[str, Any], required_fields: List[str] = None):
        required_fields = required_fields or []
        
        for key, value in input_data.items():
            if key in required_fields and value is None:
                raise ValueError(f"Missing required parameter: {key}")

    def _query(self, input_data: Dict[str, Any]) -> Optional[str]:
        query_params = {
            k: ('true' if v is True else 'false' if v is False else v)
            for k, v in input_data.items() if v is not None
        }
        return urlencode(query_params) if query_params else None

    async def _fetch(self, fetch_options: FetchOptionsModel) -> APIResponseModel:
        method = fetch_options.type.upper()
        url = fetch_options.url
        headers = self.headers.copy()

        if fetch_options.type == "POST" and fetch_options.body:
            json_data = fetch_options.body
        else:
            json_data = None

        try:
            async with aiohttp.ClientSession() as session:
                async with session.request(
                    method,
                    url,
                    headers=headers,
                    json=json_data,
                    params=None if not fetch_options.rtype else fetch_options.rtype,
                ) as response:
                    return await self._parse_response(response, url)
        except aiohttp.ClientError as e:
            return APIResponseModel(
                status=500,
                data=None,
                ratelimits=None,
                error=ErrorObject(message=str(e)),
                url=fetch_options.url,
            )

    async def get_account(self, options: AccountFetchOptionsModel) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"force": options.force})
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/v1/account/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_account_by_puuid(
        self, options: AccountFetchByPUUIDOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"force": options.force})
        url = f"{self.BASE_URL}/v1/by-puuid/account/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_mmr_by_puuid(
        self, options: GetMMRByPUUIDFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"filter": options.filter})
        url = f"{self.BASE_URL}/{options.version}/by-puuid/mmr/{options.region}/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_mmr_history_by_puuid(
        self, options: GetMMRHistoryByPUUIDFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        url = (
            f"{self.BASE_URL}/v1/by-puuid/mmr-history/{options.region}/{options.puuid}"
        )
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_matches_by_puuid(
        self, options: GetMatchesByPUUIDFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query(
            {"filter": options.filter, "map": options.map, "size": options.size}
        )
        url = f"{self.BASE_URL}/v3/by-puuid/matches/{options.region}/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_content(
        self, options: GetContentFetchOptionsModel
    ) -> APIResponseModel:
        query = self._query({"locale": options.locale})
        url = f"{self.BASE_URL}/v1/content"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_leaderboard(
        self, options: GetLeaderboardOptionsModel
    ) -> APIResponseModel:
        if options.name and options.tag and options.puuid:
            raise ValueError(
                "Too many parameters: You can't search for name/tag and puuid at the same time, please decide between name/tag and puuid"
            )
        self._validate({"version": options.version, "region": options.region})
        query = self._query(
            {
                "start": options.start,
                "end": options.end,
                "name": options.name,
                "tag": options.tag,
                "puuid": options.puuid,
                "season": options.season,
            }
        )
        url = f"{self.BASE_URL}/{options.version}/leaderboard/{options.region}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_matches(
        self, options: GetMatchesFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query(
            {"filter": options.filter, "map": options.map, "size": options.size}
        )
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = (
            f"{self.BASE_URL}/v3/matches/{options.region}/{encoded_name}/{encoded_tag}"
        )
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_match(self, options: GetMatchFetchOptionsModel) -> APIResponseModel:
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v2/match/{options.match_id}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_mmr_history(
        self, options: GetMMRHistoryFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/v1/mmr-history/{options.region}/{encoded_name}/{encoded_tag}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_lifetime_mmr_history(
        self, options: GetLifetimeMMRHistoryFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"page": options.page, "size": options.size})
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/v1/lifetime/mmr-history/{options.region}/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_mmr(self, options: GetMMRFetchOptionsModel) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"filter": options.filter})
        encoded_region = quote(options.region)
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/mmr/{encoded_region}/{options.name}/{options.tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_raw_data(self, options: GetRawFetchOptionsModel) -> APIResponseModel:
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v1/raw"
        fetch_options = FetchOptionsModel(
            url=url, type="POST", body=options.model_dump()
        )
        return await self._fetch(fetch_options)

    async def get_status(self, options: GetStatusFetchOptionsModel) -> APIResponseModel:
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v1/status/{options.region}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_featured_items(
        self, options: GetFeaturedItemsFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/{options.version}/store-featured"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_offers(self) -> APIResponseModel:
        url = f"{self.BASE_URL}/v1/store-offers"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_version(
        self, options: GetVersionFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v1/version/{options.region}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_website(
        self, options: GetWebsiteFetchOptionsModel
    ) -> APIResponseModel:
        self._validate({"country_code": options.country_code})
        query = self._query({"filter": options.filter})
        url = f"{self.BASE_URL}/v1/website/{options.country_code}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        return await self._fetch(fetch_options)

    async def get_crosshair(
        self, options: GetCrosshairFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        query = self._query({"id": options.code, "size": options.size})
        url = f"{self.BASE_URL}/v1/crosshair/generate"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url, rtype="arraybuffer")
        return await self._fetch(fetch_options)
