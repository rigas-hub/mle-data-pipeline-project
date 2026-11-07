from pathlib import Path
from unittest.mock import Mock

import pytest

from src.data_download import build_filename, download_file, validate_month


def test_build_filename():
    assert build_filename(2025, 1) == "green_tripdata_2025-01.parquet"


def test_validate_month_accepts_valid_month():
    assert validate_month(1) is None


def test_validate_month_rejects_month_below_range():
    with pytest.raises(ValueError, match="Months must be between 1 and 12"):
        validate_month(0)


def test_validate_month_rejects_month_above_range():
    with pytest.raises(ValueError, match="Months must be between 1 and 12"):
        validate_month(13)


def test_download_file(tmp_path, monkeypatch):
    output_dir = tmp_path / "raw"
    urlretrieve = Mock(
        side_effect=lambda url, destination: Path(destination).write_bytes(
            b"parquet data"
        )
    )
    monkeypatch.setattr("src.data_download.urlretrieve", urlretrieve)

    destination = download_file(2025, 1, output_dir, overwrite=False)

    expected_path = output_dir / "green_tripdata_2025-01.parquet"
    assert destination == expected_path
    assert expected_path.read_bytes() == b"parquet data"
    urlretrieve.assert_called_once()


def test_download_file_with_existing_file(tmp_path, monkeypatch):
    output_dir = tmp_path / "raw"
    output_dir.mkdir()
    existing_file = output_dir / "green_tripdata_2025-01.parquet"
    existing_file.write_bytes(b"existing data")

    urlretrieve = Mock()
    monkeypatch.setattr("src.data_download.urlretrieve", urlretrieve)

    destination = download_file(2025, 1, output_dir, overwrite=False)

    assert destination == existing_file
    assert existing_file.read_bytes() == b"existing data"
    urlretrieve.assert_not_called()


def test_download_file_with_overwrite(tmp_path, monkeypatch):
    output_dir = tmp_path / "raw"
    output_dir.mkdir()
    existing_file = output_dir / "green_tripdata_2025-01.parquet"
    existing_file.write_bytes(b"old data")

    urlretrieve = Mock(
        side_effect=lambda url, destination: Path(destination).write_bytes(b"new data")
    )
    monkeypatch.setattr("src.data_download.urlretrieve", urlretrieve)

    destination = download_file(2025, 1, output_dir, overwrite=True)

    assert destination == existing_file
    assert existing_file.read_bytes() == b"new data"
    urlretrieve.assert_called_once()