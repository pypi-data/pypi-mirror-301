from typing import Any, Dict, List, NewType, Optional, Union

from pydantic import BaseModel

BinaryData = NewType("BinaryData", bytes)


class RateLimit(BaseModel):
    used: int
    remaining: int
    reset: int


class ErrorObject(BaseModel):
    message: str


class APIResponseModel(BaseModel):
    status: int
    data: Optional[Dict[str, Any]] | Optional[List[Dict[str, Any]]] = None
    ratelimits: Optional[RateLimit] = None
    error: Optional[ErrorObject] = None
    url: Optional[str] = None


class AccountCardResponseModelV1(BaseModel):
    small: str
    large: str
    wide: str
    id: str


class AccountResponseModelV1(BaseModel):
    puuid: str
    region: str
    account_level: int
    name: str
    tag: str
    card: AccountCardResponseModelV1
    last_update: str
    last_update_raw: int

    class Config:
        extra = "ignore"

    def __str__(self):
        fields = "\n".join(
            f"{key}={value!r}" for key, value in self.model_dump().items()
        )
        return f"{self.__class__.__name__}(\n{fields}\n)"


class ActRankWinsModel(BaseModel):
    patched_tier: str
    tier: int


class SeasonDataModel(BaseModel):
    error: Optional[Union[bool, str]] = None
    wins: Optional[int] = None
    number_of_games: Optional[int] = None
    final_rank: Optional[int] = None
    final_rank_patched: Optional[str] = None
    act_rank_wins: Optional[List[ActRankWinsModel]] = None
    old: Optional[bool] = None


class ImagesModel(BaseModel):
    small: str
    large: str
    triangle_down: str
    triangle_up: str


class CurrentDataModel(BaseModel):
    currenttier: Optional[int]
    currenttierpatched: Optional[str]
    images: ImagesModel
    ranking_in_tier: Optional[int]
    mmr_change_to_last_game: Optional[int]
    elo: Optional[int]
    old: bool


class HighestRankModel(BaseModel):
    old: bool
    tier: Optional[int]
    patched_tier: str
    season: Optional[str]


class MMRResponseModel(BaseModel):
    name: str
    tag: str
    current_data: Optional[CurrentDataModel] = None
    highest_rank: Optional[HighestRankModel] = None
    by_season: Optional[Dict[str, SeasonDataModel]] = None

    def __str__(self):
        fields = "\n".join(
            f"{key}={value!r}" for key, value in self.model_dump().items()
        )
        return f"{self.__class__.__name__}(\n{fields}\n)"


class ImagesModel(BaseModel):
    small: str
    large: str
    triangle_down: str
    triangle_up: str


class MapModel(BaseModel):
    name: str
    id: str


class MatchDataModel(BaseModel):
    currenttier: int
    currenttier_patched: str
    images: ImagesModel
    match_id: str
    map: MapModel
    season_id: str
    ranking_in_tier: int
    mmr_change_to_last_game: int
    elo: int
    date: str
    date_raw: int


class MMRHistoryByPuuidResponseModelV1(BaseModel):
    status: Optional[int] = None
    name: str
    tag: str
    data: List[MatchDataModel]


class CommunityNewsResponseModel(BaseModel):
    banner_url: str
    category: str
    date: str
    external_link: Optional[str]
    title: str
    url: str


class BuildGameInfoResponseModel(BaseModel):
    region: str
    branch: str
    build_date: str
    build_ver: str
    last_checked: str
    version: int
    version_for_api: str


class RewardModel(BaseModel):
    ItemTypeID: str
    ItemID: str
    Quantity: int


class OfferModel(BaseModel):
    OfferID: str
    IsDirectPurchase: bool
    StartDate: str
    Cost: Dict[str, int]
    Rewards: List[RewardModel]


class OfferUpgradeCurrencyModel(BaseModel):
    OfferID: str
    StorefrontItemID: str
    Offer: OfferModel
    DiscountedPercent: float


class StoreOffersResponseModelV1(BaseModel):
    Offers: List[OfferModel]
    UpgradeCurrencyOffers: Optional[List[OfferUpgradeCurrencyModel]]


class ContentTierModel(BaseModel):
    name: str
    dev_name: str
    icon: str


class StoreOffersResponseModelV2(BaseModel):
    offer_id: str
    cost: int
    name: str
    icon: Optional[str]
    type: str
    skin_id: str
    content_tier: Optional[ContentTierModel]


# store featured


class ItemResponseModel(BaseModel):
    ItemTypeID: str
    ItemID: str
    Amount: int


class BundleItemResponseModel(BaseModel):
    Item: ItemResponseModel
    BasePrice: float
    CurrencyID: str
    DiscountPercent: float
    DiscountedPrice: float
    IsPromoItem: bool


class BundleResponseModel(BaseModel):
    ID: str
    DataAssetID: str
    CurrencyID: str
    Items: List[BundleItemResponseModel]
    DurationRemainingInSeconds: int


class FeaturedBundleModel(BaseModel):
    Bundle: BundleResponseModel
    Bundles: List[BundleResponseModel]
    BundleRemainingDurationInSeconds: int


class FeaturedBundleResponseModelV1(BaseModel):
    FeaturedBundle: FeaturedBundleModel


class BundleResponseItemModelV2(BaseModel):
    uuid: str
    name: str
    image: Optional[str]
    type: str
    amount: int
    discount_percent: float
    base_price: float
    discounted_price: float
    promo_item: bool


class BundleResponseModelV2(BaseModel):
    bundle_uuid: str
    seconds_remaining: int
    bundle_price: int
    whole_sale_only: bool
    expires_at: str
    items: List[BundleResponseItemModelV2]


# status response


class TranslationResponseModel(BaseModel):
    content: str
    locale: str


class UpdateStatusResponseModel(BaseModel):
    created_at: str
    updated_at: str
    publish: bool
    id: int
    translations: List[TranslationResponseModel]
    publish_locations: List[str]
    author: str


class StatusTitleResponseModel(BaseModel):
    content: str
    locale: str


class StatusMaintenanceResponseModel(BaseModel):
    created_at: str
    archive_at: str
    updates: List[UpdateStatusResponseModel]
    platforms: List[str]
    updated_at: str
    id: int
    titles: List[StatusTitleResponseModel]
    maintenance_status: str
    incident_severity: str


class StatusIncidentResponseModel(BaseModel):
    created_at: str
    archive_at: str
    updates: List[UpdateStatusResponseModel]
    platforms: List[str]
    updated_at: str
    id: int
    titles: List[StatusTitleResponseModel]
    maintenance_status: str
    incident_severity: str


class StatusDataResponseModel(BaseModel):
    maintenances: Optional[List[StatusMaintenanceResponseModel]]
    incidents: Optional[List[StatusIncidentResponseModel]]


# content response


class ContnentLocalizedNamesResponseModel(BaseModel):
    ar_AE: Optional[str] = None
    de_DE: Optional[str] = None
    en_GB: Optional[str] = None
    en_US: Optional[str] = None
    es_ES: Optional[str] = None
    es_MX: Optional[str] = None
    fr_FR: Optional[str] = None
    id_ID: Optional[str] = None
    it_IT: Optional[str] = None
    ja_JP: Optional[str] = None
    ko_KR: Optional[str] = None
    pl_PL: Optional[str] = None
    pt_BR: Optional[str] = None
    ru_RU: Optional[str] = None
    th_TH: Optional[str] = None
    tr_TR: Optional[str] = None
    vi_VN: Optional[str] = None
    zn_CN: Optional[str] = None
    zn_TW: Optional[str] = None


class CharacterContentResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentMapResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentChromaResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentSkinResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentSkinLevelResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentEquipResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentGameModeResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentSprayResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentSprayLeveResonselModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentCharmResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentCharmLeveResonsellModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContetnPlayerCardResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentPlayerTitleResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    assetName: Optional[str] = None
    assetPath: Optional[str] = None


class ContentActResponseModel(BaseModel):
    name: str
    localizedNames: Optional[List[ContnentLocalizedNamesResponseModel]]
    id: str
    isActive: bool


class ContentResponseModel(BaseModel):
    version: str
    characters: List[ContnentLocalizedNamesResponseModel]
    maps: List[MapModel]
    chromas: List[ContentCharmResponseModel]
    skins: List[ContentSkinResponseModel]
    skinLevels: List[ContentSkinLevelResponseModel]
    equips: List[ContentEquipResponseModel]
    gameModes: List[ContentGameModeResponseModel]
    sprays: List[ContentSprayResponseModel]
    sprayLevels: List[ContentSprayLeveResonselModel]
    charms: List[ContentCharmResponseModel]
    charmLevels: List[ContentCharmLeveResonsellModel]
    playerCards: List[ContetnPlayerCardResponseModel]
    playerTitles: List[ContentPlayerTitleResponseModel]
    acts: List[ContentActResponseModel]


# leaderboard


class LeaderboardPlayerResponseModelV3(BaseModel):
    card: str
    title: str
    is_banned: bool
    is_anonymized: bool
    puuid: Optional[str] = None
    name: str
    tag: str
    updated_at: str


class LeaderboardDataResponseModelV3(BaseModel):
    updated_at: str
    thresholds: Optional[List[dict]]
    players: Optional[List[LeaderboardPlayerResponseModelV3]]


# v2
class LeaderboardPlayerResponseModelV2(BaseModel):
    PlayerCardID: str
    TitleID: str
    IsBanned: bool
    IsAnonymized: bool
    puuid: Optional[str] = None
    gameName: str
    tagLine: str
    leaderboardRank: int
    rankedRating: int
    numberOfWins: int
    competitiveTier: int


class LeaderboardDataResponseModelV2(BaseModel):
    last_update: int
    next_update: int
    total_players: int
    radiant_threshold: int
    immortal_3_threshold: int
    immortal_2_threshold: int
    immortal_1_threshold: int
    players: List[LeaderboardPlayerResponseModelV2]


# --- Metadata models ---
class MatchOSModel(BaseModel):
    name: str
    version: str


class MatchPlatformModel(BaseModel):
    type: str
    os: MatchOSModel


class MatchSessionPlaytimeModel(BaseModel):
    minutes: int
    seconds: int
    milliseconds: int


class MatchAssetsCardModel(BaseModel):
    small: str
    large: str
    wide: str


class MatchAssetsAgentModel(BaseModel):
    small: str
    full: str
    bust: str
    killfeed: str


class MatchAssetsModel(BaseModel):
    card: MatchAssetsCardModel
    agent: MatchAssetsAgentModel


class MatchFriendlyFireModel(BaseModel):
    incoming: int
    outgoing: int


class MatchBehaviourModel(BaseModel):
    afk_rounds: int
    friendly_fire: MatchFriendlyFireModel
    rounds_in_spawn: int


class MatchAbilityCastsModel(BaseModel):
    c_cast: int
    q_cast: int
    e_cast: int
    x_cast: int


class MatchStatsModel(BaseModel):
    score: int
    kills: int
    deaths: int
    assists: int
    bodyshots: int
    headshots: int
    legshots: int


class MatchEconomySpentModel(BaseModel):
    overall: float
    average: float


class MatchEconomyLoadoutValueModel(BaseModel):
    overall: float
    average: float


class MatchEconomyModel(BaseModel):
    spent: MatchEconomySpentModel
    loadout_value: MatchEconomyLoadoutValueModel


class MatchPlayerModel(BaseModel):
    puuid: Optional[str] = None
    name: str
    tag: str
    team: str
    level: int
    character: str
    currenttier: int
    currenttier_patched: str
    player_card: str
    player_title: str
    party_id: str
    session_playtime: MatchSessionPlaytimeModel
    assets: MatchAssetsModel
    behaviour: Optional[MatchBehaviourModel] = None
    platform: MatchPlatformModel
    ability_casts: MatchAbilityCastsModel
    stats: MatchStatsModel
    economy: MatchEconomyModel
    damage_made: int
    damage_received: int


# --- Team Models ---
class MatchTeamModel(BaseModel):
    has_won: bool
    rounds_won: int
    rounds_lost: int


# --- Main Models ---


class MachPremierInfoModel(BaseModel):
    tournament_id: Optional[str]
    matchup_id: Optional[str]


class MatchMetadataModel(BaseModel):
    map: str
    game_version: str
    game_length: int
    game_start: int
    game_start_patched: str
    rounds_played: int
    mode: str
    mode_id: str
    queue: str
    season_id: str
    platform: str
    matchid: str
    premier_info: Optional[MachPremierInfoModel]
    region: str
    cluster: str


class MatchPlayersModel(BaseModel):
    all_players: List[MatchPlayerModel]
    red: List[MatchPlayerModel]
    blue: List[MatchPlayerModel]


class MatchObserversModel(BaseModel):
    puuid: str
    name: str
    tag: str
    platform: MatchPlatformModel
    session_playtime: MatchSessionPlaytimeModel
    team: str
    level: int
    player_card: str
    player_title: str
    party_id: str


class MatchCoachesModel(BaseModel):
    puuid: str
    team: str


class MatchTeamsModel(BaseModel):
    red: MatchTeamModel
    blue: MatchTeamModel


class MatchResponseModel(BaseModel):
    metadata: MatchMetadataModel
    players: MatchPlayersModel
    observers: List[MatchObserversModel]
    coaches: List[MatchCoachesModel]
    teams: MatchTeamsModel
