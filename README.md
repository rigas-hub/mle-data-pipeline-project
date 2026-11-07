# NYC Green Taxi Data Pipeline

![Python](https://img.shields.io/badge/Python-3.13-3776AB?logo=python&logoColor=white)
![Pandas](https://img.shields.io/badge/Pandas-150458?logo=pandas&logoColor=white)
![Polars](https://img.shields.io/badge/Polars-CD792C?logo=polars&logoColor=white)
![DuckDB](https://img.shields.io/badge/DuckDB-FFF000?logo=duckdb&logoColor=black)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-4169E1?logo=postgresql&logoColor=white)
![Prefect](https://img.shields.io/badge/Prefect-024DFD?logo=prefect&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-2496ED?logo=docker&logoColor=white)

I built this project to explore, process, and report on NYC Green Taxi trip data. I started by exploring the Parquet files with Polars and DuckDB, then compared ETL and ELT approaches. I chose ETL: transform the data in Python, load it into PostgreSQL, and query it for a daily report. Prefect orchestrates the pipeline.

## What the pipeline does

1. Downloads a monthly Green Taxi Parquet file from the NYC Taxi & Limousine Commission dataset.
2. Cleans the data in Python: renames selected columns, derives pickup and drop-off dates, removes rows with missing or zero passenger counts, and calculates fare per passenger.
3. Loads the transformed records into a local PostgreSQL table.
4. Queries the table for daily ride counts and average revenue per passenger, then saves the report to `data/output/revenue_report.parquet`.

The current Prefect entry point runs January 2025. The download script accepts a year and month, so it can also be run separately for another month.

## Project files

| Path | Purpose |
|---|---|
| `src/data_download.py` | Downloads a monthly Green Taxi Parquet file into `data/raw`. |
| `src/data_cleaning.py` | Cleans and prepares trip data for loading. |
| `src/etl_pipeline.py` | Orchestrates extraction, transformation, PostgreSQL loading, and report generation with Prefect. |
| `src/create_sqlalchemy_block.py` | Creates the Prefect PostgreSQL connection block. |
| `src/revenue_report.py` | Reads and prints the generated Parquet report. |
| `tests/` | Tests the data download and preparation functions. |
| `notebooks/` | Notebooks used to explore the data and compare ETL and ELT approaches. |
| `docker-compose.yaml` | Defines the local PostgreSQL service used by the pipeline. |
| `pyproject.toml` and `uv.lock` | Project metadata, dependencies, and locked dependency versions. |
| `solution/` | Separate reference implementation provided with the project template. |

## Run it locally

### Prerequisites

- Python 3.13.17 or newer in the 3.13 series
- [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 or newer
- Docker

Install the project dependencies:

```bash
uv sync
```

### Start PostgreSQL

Make sure Docker Desktop is running. If you are switching from the previous `docker run` setup, remove its container first; this keeps the database files in `db-data`:

```bash
docker rm -f ny-taxi-db
```

If you are switching from the previous Compose setup, stop it with `docker compose down` before continuing. Its Docker-managed `postgres_data` volume is separate from the new `db-data` folder and is not automatically copied or reused.

Start PostgreSQL from the repository root:

```bash
docker compose up -d
```

On the first run, Docker downloads the PostgreSQL 17 image. Compose starts the container as `ny-taxi-db` and creates its network. The database is available at `localhost:5432` with database `ny_taxi`, username `postgres`, and password `postgres`. These credentials are for local development only. Database files are stored in `db-data` in the repository.

Check that the container is running and its health check has passed:

```bash
docker compose ps
```

The container must stay running while you execute the pipeline.

In a terminal, start the Prefect server:

```bash
uv run prefect server start
```

While the server is running, open the [Prefect dashboard](http://127.0.0.1:4200) in your browser. After starting the pipeline, use the dashboard to inspect the flow run, task states, and logs.

In another terminal, configure Prefect and create the database connector block:

```bash
uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
uv run python src/create_sqlalchemy_block.py
```

Run the pipeline and print the generated report:

```bash
uv run python src/etl_pipeline.py
uv run python src/revenue_report.py
```

The report is written to `data/output/revenue_report.parquet`. The pipeline downloads January 2025 data into `data/raw` if it is not already present.

To download a different month separately:

```bash
uv run python src/data_download.py --year 2025 --month 2 --output-dir data/raw
```

Stop the Prefect server with `Ctrl+C`. Stop PostgreSQL when finished:

```bash
docker compose down
```

This removes the container and its Compose network but leaves the database files in `db-data`. Delete that directory only if you also want to permanently remove the local database contents.

## Tests and linting

```bash
uv run python -m pytest -q tests
uv run ruff check src tests
```

## What I learned

The biggest challenge was connecting the pieces into one reliable workflow: exploring the data, deciding how to transform it, setting up PostgreSQL, writing useful queries, and orchestrating the steps. Working through the project made database setup and pipeline behavior much more concrete, especially because database work was new to me.

Given more time, I would make the pipeline easier to extend and improve its reporting and orchestration. This project was a useful first end-to-end implementation, and there is room to build on it.

## Future improvements (7 November 2026)

- Make the reporting period configurable, so the pipeline can process a selected month or range instead of only January 2025.
- Strengthen data quality checks by excluding negative or implausible `total_amount` values and trips whose pickup dates fall outside the requested period.
- Expand the tests to cover these validation rules and verify report results for different input periods.
