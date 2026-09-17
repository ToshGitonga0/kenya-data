"""Lightweight, typed record wrappers returned by the SDK."""
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class County:
    id: int
    code: str
    name: str
    capital: str | None
    status: str


@dataclass(frozen=True)
class Constituency:
    id: int
    code: str
    name: str
    county_id: int
    status: str


@dataclass(frozen=True)
class Ward:
    id: int
    code: str
    name: str
    constituency_id: int
    status: str


@dataclass(frozen=True)
class DatasetInfo:
    version: str
    status: str
    updated_at: str
