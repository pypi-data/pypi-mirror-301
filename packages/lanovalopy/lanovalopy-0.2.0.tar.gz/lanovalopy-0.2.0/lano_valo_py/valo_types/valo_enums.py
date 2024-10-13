from enum import Enum


class Episodes(str, Enum):
    e1a1 = 'e1a1'
    e1a2 = 'e1a2'
    e1a3 = 'e1a3'
    e2a1 = 'e2a1'
    e2a2 = 'e2a2'
    e2a3 = 'e2a3'
    e3a1 = 'e3a1'
    e3a2 = 'e3a2'
    e3a3 = 'e3a3'
    e4a1 = 'e4a1'
    e4a2 = 'e4a2'
    e4a3 = 'e4a3'
    e5a1 = 'e5a1'
    e5a2 = 'e5a2'
    e5a3 = 'e5a3'


class LeaderboardEpisodes(str, Enum):
    e2a1 = 'e2a1'
    e2a2 = 'e2a2'
    e2a3 = 'e2a3'
    e3a1 = 'e3a1'
    e3a2 = 'e3a2'
    e3a3 = 'e3a3'
    e4a1 = 'e4a1'
    e4a2 = 'e4a2'
    e4a3 = 'e4a3'
    e5a1 = 'e5a1'
    e5a2 = 'e5a2'
    e5a3 = 'e5a3'


class Modes(str, Enum):
    escalation = 'escalation'
    spikerush = 'spikerush'
    deathmatch = 'deathmatch'
    competitive = 'competitive'
    unrated = 'unrated'
    replication = 'replication'
    custom = 'custom'
    newmap = 'newmap'
    snowball = 'snowball'


class Maps(str, Enum):
    ascent = 'ascent'
    split = 'split'
    fracture = 'fracture'
    bind = 'bind'
    breeze = 'breeze'
    icebox = 'icebox'
    haven = 'haven'
    pearl = 'pearl'


class CCRegions(str, Enum):
    en_gb = 'en-gb'
    en_us = 'en-us'
    es_es = 'es-es'
    es_mx = 'es-mx'
    fr_fr = 'fr-fr'
    it_it = 'it-it'
    ja_jp = 'ja-jp'
    ko_kr = 'ko-kr'
    pt_br = 'pt-br'
    ru_ru = 'ru-ru'
    tr_tr = 'tr-tr'
    vi_vn = 'vi-vn'


class Locales(str, Enum):
    ar_AE = 'ar-AE'
    de_DE = 'de-DE'
    en_GB = 'en-GB'
    en_US = 'en-US'
    es_ES = 'es-ES'
    es_MX = 'es-MX'
    fr_FR = 'fr-FR'
    id_ID = 'id-ID'
    it_IT = 'it-IT'
    ja_JP = 'ja-JP'
    ko_KR = 'ko-KR'
    pl_PL = 'pl-PL'
    pt_BR = 'pt-BR'
    ru_RU = 'ru-RU'
    th_TH = 'th-TH'
    tr_TR = 'tr-TR'
    vi_VN = 'vi-VN'
    zn_CN = 'zn-CN'
    zn_TW = 'zn-TW'


class RawTypes(str, Enum):
    competitiveupdates = 'competitiveupdates'
    mmr = 'mmr'
    matchdetails = 'matchdetails'
    matchhistory = 'matchhistory'


class MMRVersions(str, Enum):
    v1 = 'v1'
    v2 = 'v2'


class FeaturedItemsVersion(str, Enum):
    v1 = 'v1'
    v2 = 'v2'


class LeaderboardVersions(str, Enum):
    v1 = 'v1'
    v2 = 'v2'


class Regions(str, Enum):
    eu = 'eu'
    na = 'na'
    kr = 'kr'
    ap = 'ap'
    latam = 'latam'
    br = 'br'