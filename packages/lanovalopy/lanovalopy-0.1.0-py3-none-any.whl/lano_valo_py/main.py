import aiohttp
from pydantic import BaseModel
from typing import Optional, Dict, Any
from .valo_types import Regions, Maps, MMRVersions, LeaderboardVersions, Episodes


class APIResponse(BaseModel):
    status: int
    data: Optional[Dict] = None
    ratelimits: Optional[Dict] = None
    error: Optional[Dict] = None
    url: Optional[str] = None


class LanoValoPy:
    BASE_URL = "https://api.henrikdev.xyz/valorant"

    def __init__(self, token: Optional[str] = None):
        self.token = token

    async def _fetch(
        self,
        url: str,
        method: str = "GET",
        body: Optional[Dict] = None,
        rtype: str = "json",
    ) -> APIResponse:
        headers = {
            "User-Agent": "unofficial-valorant-api/python",
            "Authorization": self.token if self.token else "",
        }

        async with aiohttp.ClientSession() as session:
            async with session.request(
                method, url, json=body, headers=headers
            ) as response:
                try:
                    data = (
                        await response.json()
                        if rtype == "json"
                        else await response.read()
                    )
                    ratelimits = {
                        "used": response.headers.get("x-ratelimit-limit", 0),
                        "remaining": response.headers.get("x-ratelimit-remaining", 0),
                        "reset": response.headers.get("x-ratelimit-reset", 0),
                    }
                    return APIResponse(
                        status=response.status,
                        data=data,
                        ratelimits=ratelimits,
                        url=url,
                        error=None if response.ok else data,
                    )
                except Exception as e:
                    return APIResponse(
                        status=response.status,
                        error={"message": str(e)},
                        url=url,
                    )

    def _validate(self, input_data: Dict[str, Any]):
        for key, value in input_data.items():
            if value is None:
                raise ValueError(f"Missing parameter: {key}")

    def _query(self, input_data: Dict[str, Any]) -> str:
        return "&".join(
            [f"{key}={value}" for key, value in input_data.items() if value is not None]
        )

    async def get_account(
        self, name: str, tag: str, force: Optional[bool] = None
    ) -> APIResponse:
        self._validate({"name": name, "tag": tag})
        query = self._query({"force": force})
        url = f"{self.BASE_URL}/v1/account/{name}/{tag}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_account_by_puuid(
        self, puuid: str, force: Optional[bool] = None
    ) -> APIResponse:
        self._validate({"puuid": puuid})
        query = self._query({"force": force})
        url = (
            f"{self.BASE_URL}/v1/by-puuid/account/{puuid}{f'?{query}' if query else ''}"
        )
        return await self._fetch(url)

    async def get_mmr(
        self,
        version: MMRVersions,
        region: Regions,
        name: str,
        tag: str,
        filter: Optional[str] = None,
    ) -> APIResponse:
        self._validate({"version": version, "region": region, "name": name, "tag": tag})
        query = self._query({"filter": filter})
        url = f"{self.BASE_URL}/{version}/mmr/{region}/{name}/{tag}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_mmr_by_puuid(
        self,
        version: MMRVersions,
        region: Regions,
        puuid: str,
        filter: Optional[str] = None,
    ) -> APIResponse:
        self._validate({"version": version, "region": region, "puuid": puuid})
        query = self._query({"filter": filter})
        url = f"{self.BASE_URL}/{version}/by-puuid/mmr/{region}/{puuid}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_mmr_history_by_puuid(
        self, region: Regions, puuid: str
    ) -> APIResponse:
        self._validate({"region": region, "puuid": puuid})
        url = f"{self.BASE_URL}/v1/by-puuid/mmr-history/{region}/{puuid}"
        return await self._fetch(url)

    async def get_matches_by_puuid(
        self,
        region: str,
        puuid: str,
        filter: Optional[str] = None,
        map: Optional[Maps] = None,
        size: Optional[int] = None,
    ) -> APIResponse:
        self._validate({"region": region, "puuid": puuid})
        query = self._query({"filter": filter, "map": map, "size": size})
        url = f"{self.BASE_URL}/v3/by-puuid/matches/{region}/{puuid}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_content(self, locale: Optional[str] = None) -> APIResponse:
        query = self._query({"locale": locale})
        url = f"{self.BASE_URL}/v1/content{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_leaderboard(
        self,
        version: LeaderboardVersions,
        region: Regions,
        start: Optional[int] = None,
        end: Optional[int] = None,
        name: Optional[str] = None,
        tag: Optional[str] = None,
        puuid: Optional[str] = None,
        season: Optional[Episodes] = None,
    ) -> APIResponse:
        if name and tag and puuid:
            raise ValueError(
                "Too many parameters: You can't search for name/tag and puuid at the same time, please decide between name/tag and puuid"
            )
        self._validate({"version": version, "region": region})
        query = self._query(
            {
                "start": start,
                "end": end,
                "name": name,
                "tag": tag,
                "puuid": puuid,
                "season": season,
            }
        )
        url = f"{self.BASE_URL}/{version}/leaderboard/{region}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_matches(
        self,
        region: str,
        name: str,
        tag: str,
        filter: Optional[str] = None,
        map: Optional[str] = None,
        size: Optional[int] = None,
    ) -> APIResponse:
        self._validate({"region": region, "name": name, "tag": tag})
        query = self._query({"filter": filter, "map": map, "size": size})
        url = f"{self.BASE_URL}/v3/matches/{region}/{name}/{tag}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_match(self, match_id: str) -> APIResponse:
        self._validate({"match_id": match_id})
        url = f"{self.BASE_URL}/v2/match/{match_id}"
        return await self._fetch(url)

    async def get_mmr_history(self, region: str, name: str, tag: str) -> APIResponse:
        self._validate({"region": region, "name": name, "tag": tag})
        url = f"{self.BASE_URL}/v1/mmr-history/{region}/{name}/{tag}"
        return await self._fetch(url)

    async def get_lifetime_mmr_history(
        self,
        region: str,
        name: str,
        tag: str,
        page: Optional[int] = None,
        size: Optional[int] = None,
    ) -> APIResponse:
        self._validate({"region": region, "name": name, "tag": tag})
        query = self._query({"page": page, "size": size})
        url = f"{self.BASE_URL}/v1/lifetime/mmr-history/{region}/{name}/{tag}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_raw_data(
        self, type: str, value: str, region: str, queries: Dict[str, Any]
    ) -> APIResponse:
        self._validate(
            {"type": type, "value": value, "region": region, "queries": queries}
        )
        url = f"{self.BASE_URL}/v1/raw"
        return await self._fetch(
            url,
            method="POST",
            body={"type": type, "value": value, "region": region, "queries": queries},
        )

    async def get_status(self, region: str) -> APIResponse:
        self._validate({"region": region})
        url = f"{self.BASE_URL}/v1/status/{region}"
        return await self._fetch(url)

    async def get_featured_items(self, version: str) -> APIResponse:
        self._validate({"version": version})
        url = f"{self.BASE_URL}/{version}/store-featured"
        return await self._fetch(url)

    async def get_offers(self) -> APIResponse:
        return await self._fetch(f"{self.BASE_URL}/v1/store-offers")

    async def get_version(self, region: Regions) -> APIResponse:
        self._validate({"region": region})
        url = f"{self.BASE_URL}/v1/version/{region}"
        return await self._fetch(url)

    async def get_website(
        self, country_code: str, filter: Optional[str] = None
    ) -> APIResponse:
        self._validate({"country_code": country_code})
        query = self._query({"filter": filter})
        url = f"{self.BASE_URL}/v1/website/{country_code}{f'?{query}' if query else ''}"
        return await self._fetch(url)

    async def get_crosshair(self, code: str, size: Optional[int] = None) -> APIResponse:
        self._validate({"code": code})
        query = self._query({"id": code, "size": size})
        url = f"{self.BASE_URL}/v1/crosshair/generate/{code}{f'?{query}' if query else ''}"
        return await self._fetch(url, rtype="arraybuffer")
