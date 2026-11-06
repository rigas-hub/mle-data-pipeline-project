"""Download NYC taxi Parquet files to a local folder."""

from pathlib import Path
from urllib.request import urlretrieve

import click

BASE_URL = "https://d37ci6vzurychx.cloudfront.net/trip-data"
DATASET = "green"


def build_filename(year, month):
    return f"{DATASET}_tripdata_{year}-{month:02d}.parquet"


def validate_month(month):
    # A small validation step keeps the error message clear before any download starts.
    if month < 1 or month > 12:
        raise ValueError("Month must be between 1 and 12.")


def download_file(year, month, output_dir, overwrite):
    filename = build_filename(year, month)
    url = f"{BASE_URL}/{filename}"
    destination = output_dir / filename

    # Reuse local files by default so the beginner workflow stays fast.
    if destination.exists() and not overwrite:
        print(f"Skipping download: {destination} already exists.")
        return destination

    output_dir.mkdir(parents=True, exist_ok=True)
    print(f"Downloading {url}")
    urlretrieve(url, destination)
    print(f"Saved {destination}")
    return destination


def extract_data(year: int, month: int, output_dir: Path, overwrite: bool) -> str:

    validate_month(month)
    output_dir = Path(output_dir)
    destination = download_file(
        year=year, month=month, output_dir=output_dir, overwrite=overwrite
    )

    return destination


@click.command()
@click.option(
    "--year",
    default=2025,
    type=int,
    show_default=True,
    help="Dataset year to download.",
)
@click.option(
    "--months",
    multiple=True,
    type=int,
    help="Month number to download. Repeat the option, " \
    "for example --months 1 --months 2.",
)
@click.option(
    "--output-dir",
    default=Path("data/raw"),
    type=click.Path(path_type=Path),
    show_default=True,
    help="Directory where the Parquet files should be saved.",
)
@click.option(
    "--overwrite",
    is_flag=True,
    help="Download again even if a local file already exists.",
)
def main(year: int, months: tuple[int, ...], output_dir: Path, overwrite: bool) -> None:
    extract_data(year, months, output_dir, overwrite)


if __name__ == "__main__":
    main()
