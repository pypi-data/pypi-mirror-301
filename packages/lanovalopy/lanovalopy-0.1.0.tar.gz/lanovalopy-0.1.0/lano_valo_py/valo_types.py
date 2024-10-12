from pydantic import BaseModel
from typing import Literal, Optional, Dict, Any

Episodes = Literal[
    "e1a1",
    "e1a2",
    "e1a3",
    "e2a1",
    "e2a2",
    "e2a3",
    "e3a1",
    "e3a2",
    "e3a3",
    "e4a1",
    "e4a2",
    "e4a3",
    "e5a1",
    "e5a2",
    "e5a3",
]

LeaderboardEpisodes = Literal[
    "e2a1",
    "e2a2",
    "e2a3",
    "e3a1",
    "e3a2",
    "e3a3",
    "e4a1",
    "e4a2",
    "e4a3",
    "e5a1",
    "e5a2",
    "e5a3",
]

Modes = Literal[
    "escalation",
    "spikerush",
    "deathmatch",
    "competitive",
    "unrated",
    "replication",
    "custom",
    "newmap",
    "snowball",
]

Maps = Literal[
    "ascent", "split", "fracture", "bind", "breeze", "icebox", "haven", "pearl"
]

CCRegions = Literal[
    "en-gb",
    "en-us",
    "es-es",
    "es-mx",
    "fr-fr",
    "it-it",
    "ja-jp",
    "ko-kr",
    "pt-br",
    "ru-ru",
    "tr-tr",
    "vi-vn",
]

Locales = Literal[
    "ar-AE",
    "de-DE",
    "en-GB",
    "en-US",
    "es-ES",
    "es-MX",
    "fr-FR",
    "id-ID",
    "it-IT",
    "ja-JP",
    "ko-KR",
    "pl-PL",
    "pt-BR",
    "ru-RU",
    "th-TH",
    "tr-TR",
    "vi-VN",
    "zn-CN",
    "zn-TW",
]

RawTypes = Literal["competitiveupdates", "mmr", "matchdetails", "matchhistory"]

MMRVersions = Literal["v1", "v2"]
FeaturedItemsVersion = Literal["v1", "v2"]
LeaderboardVersions = Literal["v1", "v2"]

Regions = Literal["eu", "na", "kr", "ap", "latam", "br"]


# Define API Response Models
class RateLimit(BaseModel):
    used: int
    remaining: int
    reset: int


class ErrorObject(BaseModel):
    message: str


class APIResponse(BaseModel):
    status: int
    data: Optional[Dict[str, Any]] = None
    ratelimits: RateLimit
    error: Optional[ErrorObject] = None


# Define Fetch Options Models
class AccountFetchOptions(BaseModel):
    name: str
    tag: str
    force: Optional[bool] = None


class AccountFetchByPUUIDOptions(BaseModel):
    puuid: str
    force: Optional[bool] = None


class GetMMRByPUUIDFetchOptions(BaseModel):
    version: MMRVersions
    region: Regions
    puuid: str
    filter: Optional[Episodes] = None


class GetMMRHistoryByPUUIDFetchOptions(BaseModel):
    region: Regions
    puuid: str


class GetMatchesByPUUIDFetchOptions(BaseModel):
    region: Regions
    puuid: str
    filter: Optional[Modes] = None
    map: Optional[Maps] = None
    size: Optional[int] = None


class GetContentFetchOptions(BaseModel):
    locale: Optional[Locales] = None


class GetLeaderboardOptions(BaseModel):
    version: LeaderboardVersions
    region: Regions
    name: Optional[str] = None
    tag: Optional[str] = None
    puuid: Optional[str] = None
    season: Optional[LeaderboardEpisodes] = None


class GetMatchesFetchOptions(BaseModel):
    region: Regions
    name: str
    tag: str
    filter: Optional[Modes] = None
    map: Optional[Maps] = None
    size: Optional[int] = None


class GetMatchFetchOptions(BaseModel):
    match_id: str


class GetMMRHistoryFetchOptions(BaseModel):
    region: Regions
    name: str
    tag: str


class GetLifetimeMMRHistoryFetchOptions(BaseModel):
    region: Regions
    name: str
    tag: str
    page: Optional[int] = None
    size: Optional[int] = None


class GetMMRFetchOptions(BaseModel):
    version: MMRVersions
    region: Regions
    name: str
    tag: str
    filter: Optional[Episodes] = None


class GetRawFetchOptions(BaseModel):
    type: RawTypes
    uuid: str
    region: Regions
    queries: str


class GetStatusFetchOptions(BaseModel):
    region: Regions


class GetVersionFetchOptions(BaseModel):
    region: Regions


class GetWebsiteFetchOptions(BaseModel):
    country_code: CCRegions
    filter: Optional[str] = None


class GetCrosshairFetchOptions(BaseModel):
    code: str
    size: Optional[int] = None


class GetFeaturedItemsFetchOptions(BaseModel):
    version: FeaturedItemsVersion
