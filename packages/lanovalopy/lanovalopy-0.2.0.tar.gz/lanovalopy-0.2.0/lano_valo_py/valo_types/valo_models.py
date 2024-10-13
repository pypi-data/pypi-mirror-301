from typing import Dict, Optional, Any
from pydantic import BaseModel

from .valo_enums import (
    CCRegions,
    FeaturedItemsVersion,
    LeaderboardEpisodes,
    RawTypes,
    Regions,
    MMRVersions,
    LeaderboardVersions,
    Locales,
    Modes,
    Maps,
    Episodes,
)

class FetchOptionsModel(BaseModel):
    url: str
    type: str = "GET"
    body: Optional[Dict[str, Any]] = None
    rtype: Optional[str] = None


class AccountFetchOptionsModel(BaseModel):
    name: str
    tag: str
    force: Optional[bool] = None


class AccountFetchByPUUIDOptionsModel(BaseModel):
    puuid: str
    force: Optional[bool] = None


class GetMMRByPUUIDFetchOptionsModel(BaseModel):
    version: MMRVersions
    region: Regions
    puuid: str
    filter: Optional[Episodes] = None


class GetMMRHistoryByPUUIDFetchOptionsModel(BaseModel):
    region: Regions
    puuid: str


class GetMatchesByPUUIDFetchOptionsModel(BaseModel):
    region: Regions
    puuid: str
    filter: Optional[Modes] = None
    map: Optional[Maps] = None
    size: Optional[int] = None


class GetContentFetchOptionsModel(BaseModel):
    locale: Optional[Locales] = None


class GetLeaderboardOptionsModel(BaseModel):
    start: Optional[str] = None
    end: Optional[str] = None
    version: LeaderboardVersions
    region: Regions
    name: Optional[str] = None
    tag: Optional[str] = None
    puuid: Optional[str] = None
    season: Optional[LeaderboardEpisodes] = None


class GetMatchesFetchOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str
    filter: Optional[Modes] = None
    map: Optional[Maps] = None
    size: Optional[int] = None


class GetMatchFetchOptionsModel(BaseModel):
    match_id: str


class GetMMRHistoryFetchOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str


class GetLifetimeMMRHistoryFetchOptionsModel(BaseModel):
    region: Regions
    name: str
    tag: str
    page: Optional[int] = None
    size: Optional[int] = None


class GetMMRFetchOptionsModel(BaseModel):
    version: MMRVersions
    region: Regions
    name: str
    tag: str
    filter: Optional[Episodes] = None


class GetRawFetchOptionsModel(BaseModel):
    type: RawTypes
    uuid: str
    region: Regions
    queries: str


class GetStatusFetchOptionsModel(BaseModel):
    region: Regions


class GetVersionFetchOptionsModel(BaseModel):
    region: Regions


class GetWebsiteFetchOptionsModel(BaseModel):
    country_code: CCRegions
    filter: Optional[str] = None


class GetCrosshairFetchOptionsModel(BaseModel):
    code: str
    size: Optional[int] = None


class GetFeaturedItemsFetchOptionsModel(BaseModel):
    version: FeaturedItemsVersion