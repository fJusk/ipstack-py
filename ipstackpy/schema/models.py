from pydantic import BaseModel

from typing import Iterable


class Language(BaseModel):
    code: str
    name: str
    native: str


class Location(BaseModel):
    geoname_id: int
    capital: str
    languages: Iterable[Language]
    country_flag: str
    country_flag_emoji: str
    country_flag_emoji_unicode: str
    calling_code: str
    is_eu: bool


class TimeZone(BaseModel):
    id: str
    current_time: str
    gmt_offset: int
    code: str
    is_daylight_saving: bool


class Currency(BaseModel):
    code: str
    name: str
    plural: str
    symbol: str
    symbol_native: str


class Connection(BaseModel):
    asn: int
    isp: str


class Security(BaseModel):
    is_proxy: str
    proxy_type: str
    is_crawler: bool
    crawler_name: str
    crawler_type: str
    is_tor: bool
    threat_level: str
    threat_types: str


class StandardResponse(BaseModel):
    ip: str
    hostname: str
    type: str
    continent_code: str
    continent_name: str
    country_code: str
    country_name: str
    region_code: str
    region_name: str
    city: str
    zip: int
    latitude: float
    longitude: float
    
    location: Location = None
    time_zone: TimeZone = None
    currency: Currency = None
    connection: Connection = None
    security: Security = None


