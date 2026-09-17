from __future__ import annotations

from pathlib import Path

import pytest

from kenya_data import EntityNotFoundError, Kenya


def test_counties_list_returns_real_counties(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    counties = kenya.counties.list()
    assert len(counties) > 0
    assert all(c.name for c in counties)


def test_counties_get_by_name_case_insensitive(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    county = kenya.counties.get("nakuru")
    assert county.name.lower() == "nakuru"


def test_counties_get_unknown_raises(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    with pytest.raises(EntityNotFoundError):
        kenya.counties.get("Not A Real County")


def test_constituencies_in_county(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    constituencies = kenya.constituencies.in_county("Nakuru")
    assert len(constituencies) > 0
    assert all(c.county_id == kenya.counties.get("Nakuru").id for c in constituencies)


def test_wards_in_constituency(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    constituency = kenya.constituencies.list()[0]
    wards = kenya.wards.in_constituency(constituency.code)
    assert all(w.constituency_id == constituency.id for w in wards)


def test_wards_in_county_traverses_hierarchy(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    wards = kenya.wards.in_county("Nakuru")
    assert len(wards) > 0


def test_dataset_metadata_present(test_db_path: Path) -> None:
    kenya = Kenya(db_path=test_db_path)
    assert kenya.dataset.version
    assert kenya.dataset.updated_at


def test_missing_database_raises_file_not_found(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        Kenya(db_path=tmp_path / "does-not-exist.db")
