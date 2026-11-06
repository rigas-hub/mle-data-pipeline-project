from pathlib import Path
from time import time
from typing import cast

import pandas as pd
from prefect import flow, task
from prefect_sqlalchemy import SqlAlchemyConnector
from sqlalchemy import text

from data_cleaning import main as data_transform
from data_ingestion import extract_data

PIPE_ROOT = Path(__file__).resolve().parent
REPO_ROOT = PIPE_ROOT.parents[2]


@task(name="Extract Task", retries=3, retry_delay_seconds=60, log_prints=True)
def extract(year, month, output_dir, overwrite) -> tuple[str, pd.DataFrame]:
    """This function downloads the parquet files for green NYC taxis for specific
      year and month in the given folder with the option to overwrite possibly 
      existing ones."""
    
    destination = extract_data(
        year=year, month=month, output_dir=output_dir, overwrite=overwrite
    )
    rides_df = pd.read_parquet(destination)
    print(f"Extraction of dataframe: {rides_df.shape}")

    return destination, rides_df


@task(name="Transform Task", retries=3, retry_delay_seconds=60, log_prints=True)
def transform(rides_df: pd.DataFrame) -> pd.DataFrame:
    """This function transforms the taxi data..."""
    print(f"Before transformation: {rides_df.shape}")
    rides_df = data_transform(rides_df)
    print(f"After transformation: {rides_df.shape}")

    return rides_df


@task(name="Load Task", retries=3, retry_delay_seconds=60, log_prints=True)
def load(rides_df: pd.DataFrame, file_path: str, table_name: str):
    """This function loads the transformed data into a PostgreSQL database."""
    del file_path
    database_block = cast(
        SqlAlchemyConnector, SqlAlchemyConnector.load("ny-taxi-connector")
    )
    with database_block.get_connection(begin=True) as engine:
        rides_df.head(n=0).to_sql(
            name=table_name, con=engine, if_exists="replace", index=False
        )

        chunksize = 10000

        for batch in range(0, len(rides_df), chunksize):
            start_time = time()
            batch_df = rides_df[batch : batch + chunksize]
            batch_df.to_sql(f"{table_name}", engine, if_exists="append", index=False)
            end_time = time()
            print("Batch time: ", end_time - start_time)

        print("Finished writing to database!")

        row_count_df = pd.read_sql(
            text(f"SELECT COUNT(*) AS row_count FROM {table_name}"),
            engine,
        )

        loaded_row_count = int(row_count_df.loc[0, "row_count"])
        assert loaded_row_count == rides_df.shape[0], (
            f"Row count mismatch: Parquet has {rides_df.shape[0]:,} \
            rows but PostgreSQL has {loaded_row_count:,}."
        )


@flow(name="Green Taxi NYC Data Flow")
def main_flow(month: int):
    parquet_file, raw_data = extract(
        year=2025, month=month, output_dir="data/raw", overwrite=False
    )
    transformed_data = transform(raw_data)
    load(transformed_data, parquet_file, "green")


if __name__ == "__main__":
    main_flow(month=1)
