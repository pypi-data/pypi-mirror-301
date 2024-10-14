from typing import Any, Dict, List, Optional
from urllib.parse import quote, urlencode

import aiohttp

from lano_valo_py.valo_types import (
    AccountResponseModelV1,
    APIResponseModel,
    BinaryData,
    BuildGameInfoResponseModel,
    BundleResponseModelV2,
    CommunityNewsResponseModel,
    ContentResponseModel,
    ErrorObject,
    FeaturedBundleResponseModelV1,
    FeaturedItemsVersion,
    FetchOptionsModel,
    LeaderboardDataResponseModelV2,
    LeaderboardDataResponseModelV3,
    LeaderboardVersions,
    MatchResponseModel,
    MMRHistoryByPuuidResponseModelV1,
    MMRResponseModel,
    RateLimit,
    StatusDataResponseModel,
    StoreOffersResponseModelV1,
    StoreOffersResponseModelV2,
)
from lano_valo_py.valo_types.valo_models import (
    AccountFetchByPUUIDOptionsModel,
    AccountFetchOptionsModel,
    GetContentFetchOptionsModel,
    GetCrosshairFetchOptionsModel,
    GetFeaturedItemsFetchOptionsModel,
    GetLeaderboardOptionsModel,
    GetLifetimeMMRHistoryFetchOptionsModel,
    GetMatchesByPUUIDFetchOptionsModel,
    GetMatchesFetchOptionsModel,
    GetMatchFetchOptionsModel,
    GetMMRByPUUIDFetchOptionsModel,
    GetMMRFetchOptionsModel,
    GetMMRHistoryByPUUIDFetchOptionsModel,
    GetMMRHistoryFetchOptionsModel,
    GetRawFetchOptionsModel,
    GetStatusFetchOptionsModel,
    GetStoreOffersFetchOptionsModel,
    GetVersionFetchOptionsModel,
    GetWebsiteFetchOptionsModel,
)


class LanoValoPy:
    BASE_URL = "https://api.henrikdev.xyz/valorant"

    def __init__(self, token: Optional[str] = None):
        """Initialize the client.

        Args:
            token (str, optional): The token to use for requests. Defaults to None.
        """
        self.token = token
        self.headers = {"User-Agent": "unofficial-valorant-api/python/1.0"}
        if self.token:
            self.headers["Authorization"] = self.token

    async def _parse_body(self, body: Any) -> Any:
        """Parses the body of a response from the API.

        Checks if the response has an "errors" key, and if so, returns it.
        Otherwise, returns the "data" key if the response has a "status" key.
        Otherwise, returns the body as is.

        Args:
            body (Any): The body of the response.

        Returns:
            Any: The parsed body.
        """
        if "errors" in body:
            return body["errors"]
        return body["data"] if body.get("status") else body

    async def _parse_response(
        self, response: aiohttp.ClientResponse, url: str
    ) -> APIResponseModel:
        """Parses a response from the API into an APIResponseModel.

        Attempts to parse the body of the response as JSON and returns it.
        If the response is not 200 OK, returns the response status and an error message.
        If the response is 200 OK, returns the parsed body and the response status.
        """
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
                error = ErrorObject(
                    message=data.get("errors", "Unknown error")[0].get(
                        "message", "Unknown error"
                    )
                )
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
        """
        Validates the input data for required fields.

        Args:
            input_data (Dict[str, Any]): The data to be validated.
            required_fields (List[str], optional): The fields that must be present in input_data. Defaults to None.

        Raises:
            ValueError: If any of the required fields are missing from input_data.
        """
        required_fields = required_fields or []

        for key, value in input_data.items():
            if key in required_fields and value is None:
                raise ValueError(f"Missing required parameter: {key}")

    def _query(self, input_data: Dict[str, Any]) -> Optional[str]:
        """
        Takes a dictionary of query parameters and turns them into a URL query string.

        Args:
            input_data (Dict[str, Any]): The query parameters to be converted into a URL query string.

        Returns:
            Optional[str]: The URL query string, or None if the input_data is empty.
        """
        query_params = {
            k: ("true" if v is True else "false" if v is False else v)
            for k, v in input_data.items()
            if v is not None
        }
        return urlencode(query_params) if query_params else None

    async def _fetch(self, fetch_options: FetchOptionsModel) -> APIResponseModel:
        """
        Performs an asynchronous HTTP request based on the provided FetchOptionsModel.

        Args:
            fetch_options (FetchOptionsModel): The options for the HTTP request.

        Returns:
            APIResponseModel: The response to the HTTP request, or an error response if the request fails.
        """
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
                    if fetch_options.rtype == "arraybuffer":
                        data = await response.read()
                        return data

                    return await self._parse_response(response, url)
        except aiohttp.ClientError as e:
            return APIResponseModel(
                status=500,
                data=None,
                ratelimits=None,
                error=ErrorObject(message=str(e)),
                url=fetch_options.url,
            )

    async def get_account(
        self, options: AccountFetchOptionsModel
    ) -> AccountResponseModelV1:
        """
        Gets the account information for a given name and tag.

        Args:
            options (AccountFetchOptionsModel): The options for the request.

        Returns:
            AccountResponseModelV1: The account information.
        """
        self._validate(options.model_dump())
        query = self._query({"force": options.force})
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/v1/account/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return AccountResponseModelV1(**result.data)

    async def get_account_by_puuid(
        self, options: AccountFetchByPUUIDOptionsModel
    ) -> AccountResponseModelV1:
        """
        Gets the account information for a given puuid.

        Args:
            options (AccountFetchByPUUIDOptionsModel): The options for the request.

        Returns:
            AccountResponseModelV1: The account information.
        """
        self._validate(options.model_dump())
        query = self._query({"force": options.force})
        url = f"{self.BASE_URL}/v1/by-puuid/account/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return AccountResponseModelV1(**result.data)

    async def get_mmr_by_puuid(
        self, options: GetMMRByPUUIDFetchOptionsModel
    ) -> MMRResponseModel:
        """
        Gets the MMR information for a given puuid.

        Args:
            options (GetMMRByPUUIDFetchOptionsModel): The options for the request.

        Returns:
            MMRResponseModel: The MMR information.
        """
        self._validate(options.model_dump())
        query = self._query({"filter": options.filter})
        encoded_region = quote(options.region)
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/by-puuid/mmr/{encoded_region}/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRResponseModel(**result.data)

    async def get_mmr_history_by_puuid(
        self, options: GetMMRHistoryByPUUIDFetchOptionsModel
    ) -> MMRHistoryByPuuidResponseModelV1:
        """
        Gets the MMR history for a given puuid.

        Args:
            options (GetMMRHistoryByPUUIDFetchOptionsModel): The options for the request.

        Returns:
            MMRHistoryByPuuidResponseModelV1: The MMR history.
        """
        self._validate(options.model_dump())
        url = (
            f"{self.BASE_URL}/v1/by-puuid/mmr-history/{options.region}/{options.puuid}"
        )
        print(url)
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRHistoryByPuuidResponseModelV1(**result.data)

    async def get_matches_by_puuid(
        self, options: GetMatchesByPUUIDFetchOptionsModel
    ) -> List[MatchResponseModel]:
        self._validate(options.model_dump())
        query = self._query(
            {"filter": options.filter, "map": options.map, "size": options.size}
        )
        url = f"{self.BASE_URL}/v3/by-puuid/matches/{options.region}/{options.puuid}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [MatchResponseModel(**match) for match in result.data]

    async def get_content(
        self, options: GetContentFetchOptionsModel
    ) -> ContentResponseModel:
        """
        Gets the content for the given locale. This endpoints returns basic contant data like season id's or skins.
        If you need more data, please refer to https://valorant-api.com which also has image data

        Args:
            options (GetContentFetchOptionsModel): The options for the request.

        Returns:
            ContentResponseModel: The content.
        """
        query = self._query({"locale": quote(options.locale)})
        url = f"{self.BASE_URL}/v1/content"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return ContentResponseModel(**result.data)

    async def get_leaderboard(
        self, options: GetLeaderboardOptionsModel
    ) -> LeaderboardDataResponseModelV3 | LeaderboardDataResponseModelV2:
        """
        Gets the leaderboard for the given options.

        Args:
            options (GetLeaderboardOptionsModel): The options for the request.

        Returns:
            LeaderboardDataResponseModelV3 | LeaderboardDataResponseModelV2: The leaderboard data.
        """
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

        encoded_region = quote(options.region)
        encoded_version = quote(options.version)

        url = f"{self.BASE_URL}/{encoded_version}/leaderboard/{encoded_region}"
        if query:
            url += f"?{query}"

        if encoded_version == LeaderboardVersions.v3:
            url += "/pc"

        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match encoded_version:
            case LeaderboardVersions.v3:
                return LeaderboardDataResponseModelV3(**result.data)
            case LeaderboardVersions.v2:
                return LeaderboardDataResponseModelV2(**result.data)
            case _:
                raise ValueError(f"Invalid version: {encoded_version}")

    async def get_matches(
        self, options: GetMatchesFetchOptionsModel
    ) -> List[MatchResponseModel]:
        self._validate(options.model_dump())
        query = self._query(
            {"filter": options.filter, "map": options.map, "size": options.size}
        )
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        encoded_region = quote(options.region)

        url = (
            f"{self.BASE_URL}/v3/matches/{encoded_region}/{encoded_name}/{encoded_tag}"
        )
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [MatchResponseModel(**match) for match in result.data]

    async def get_match(self, options: GetMatchFetchOptionsModel) -> MatchResponseModel:
        """
        Gets the match data for the given match id.

        Args:
            options (GetMatchFetchOptionsModel): The options for the request.

        Returns:
            MatchResponseModel: The match data.
        """
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v2/match/{options.match_id}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MatchResponseModel(**result.data)

    async def get_mmr_history(
        self, options: GetMMRHistoryFetchOptionsModel
    ) -> MMRResponseModel:
        """
        Returns the latest competitive games with RR movement for each game

        Args:
            options (GetMMRHistoryFetchOptionsModel): The options for the request.

        Returns:
            MMRResponseModel: The MMR history.
        """
        self._validate(options.model_dump())
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        encoded_region = quote(options.region)
        url = f"{self.BASE_URL}/v1/mmr-history/{encoded_region}/{encoded_name}/{encoded_tag}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return MMRResponseModel(**result.data)

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

    async def get_mmr(self, options: GetMMRFetchOptionsModel) -> MMRResponseModel:
        """
        Gets the MMR information for a given name and tag.

        Args:
            options (GetMMRFetchOptionsModel): The options for the request.

        Returns:
            MMRResponseModel: The MMR information.
        """
        self._validate(options.model_dump())
        query = self._query({"filter": options.filter})
        encoded_region = quote(options.region)
        encoded_version = quote(options.version)
        encoded_name = quote(options.name)
        encoded_tag = quote(options.tag)
        url = f"{self.BASE_URL}/{encoded_version}/mmr/{encoded_region}/{encoded_name}/{encoded_tag}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        print(result.data)
        return MMRResponseModel(**result.data)

    async def get_raw_data(self, options: GetRawFetchOptionsModel) -> APIResponseModel:
        """
        Make direct requests to the riot server and get the response without additional parsing from us

        Args:
            options (GetRawFetchOptionsModel): The options for the request.

        Returns:
            errors (APIResponseModel): The response from the server.
        """
        self._validate(options.model_dump())
        url = f"{self.BASE_URL}/v1/raw"
        fetch_options = FetchOptionsModel(
            url=url, type="POST", body=options.model_dump()
        )
        return await self._fetch(fetch_options)

    async def get_status(
        self, options: GetStatusFetchOptionsModel
    ) -> StatusDataResponseModel:
        """
        Gets the status server for the given region.

        Args:
            options (GetStatusFetchOptionsModel): The options for the request.

        Returns:
            StatusDataResponseModel: The status server for the given region.
        """
        self._validate(options.model_dump())
        encoded_region = quote(options.region)
        url = f"{self.BASE_URL}/v1/status/{encoded_region}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return StatusDataResponseModel(**result.data)

    async def get_featured_items(
        self, options: GetFeaturedItemsFetchOptionsModel
    ) -> APIResponseModel:
        self._validate(options.model_dump())
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/store-featured"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match encoded_version:
            case FeaturedItemsVersion.v1:
                return FeaturedBundleResponseModelV1(**result.data)
            case FeaturedItemsVersion.v2:
                return [BundleResponseModelV2(**x) for x in result.data]
            case _:
                raise ValueError(f"Invalid version: {encoded_version}")

        return await self._fetch(fetch_options)

    async def get_offers(
        self, options: GetStoreOffersFetchOptionsModel
    ) -> StoreOffersResponseModelV1:
        """
        Gets the store offers.

        Args:
            options (GetStoreOffersFetchOptionsModel): The options for the request.

        Returns:
            StoreOffersResponseModelV1: The store offers.

        Raises:
            ValueError: If the version is invalid.
        """
        self._validate(options.model_dump())
        encoded_version = quote(options.version)
        url = f"{self.BASE_URL}/{encoded_version}/store-offers"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)

        match encoded_version:
            case FeaturedItemsVersion.v1:
                return StoreOffersResponseModelV1(**result.data)
            case FeaturedItemsVersion.v2:
                return [StoreOffersResponseModelV2(**x) for x in result.data]
            case _:
                raise ValueError(f"Invalid version: {encoded_version}")

    async def get_version(
        self, options: GetVersionFetchOptionsModel
    ) -> BuildGameInfoResponseModel:
        """
        Gets the current build version and branch for a given region.

        Args:
            options (GetVersionFetchOptionsModel): The options for the request.

        Returns:
            BuildGameInfoResponseModel: The current build version and branch.
        """
        self._validate(options.model_dump())
        encoded_region = quote(options.region)
        url = f"{self.BASE_URL}/v1/version/{encoded_region}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return BuildGameInfoResponseModel(**result.data)

    async def get_website(
        self, options: GetWebsiteFetchOptionsModel
    ) -> List[CommunityNewsResponseModel]:
        """
        Gets the community news for a given country code and filter.

        Args:
            options (GetWebsiteFetchOptionsModel): The options for the request.

        Returns:
            List[CommunityNewsResponseModel]: The community news.
        """
        self._validate({"country_code": options.country_code})
        query = self._query({"filter": options.filter})
        encoded_country_code = quote(options.country_code)
        url = f"{self.BASE_URL}/v1/website/{encoded_country_code}"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url)
        result = await self._fetch(fetch_options)
        return [CommunityNewsResponseModel(**x) for x in result.data]

    async def get_crosshair(self, options: GetCrosshairFetchOptionsModel) -> BinaryData:
        """
        Gets a crosshair image as a binary response.

        Args:
            options (GetCrosshairFetchOptionsModel): The options for the request.

        Returns:
            BinaryData: The binary response from the server. This binary response is a PNG image.
        """
        self._validate(options.model_dump())
        query = self._query({"id": options.code, "size": options.size})
        url = f"{self.BASE_URL}/v1/crosshair/generate"
        if query:
            url += f"?{query}"
        fetch_options = FetchOptionsModel(url=url, rtype="arraybuffer")
        return await self._fetch(fetch_options)
