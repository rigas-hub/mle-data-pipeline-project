"""Clean downloaded data by appropriate column renaming and 
removing entries with needed missing values"""

import pandas as pd

def rename_snake_case_normalize_datetime(rides_df: pd.DataFrame) -> pd.DataFrame:

    rides_df = rides_df.copy()

    rides_df = rides_df.rename(columns={"VendorID": "vendor_id"})

    rides_df["pickup_date"] = rides_df["lpep_pickup_datetime"].dt.normalize()
    rides_df = rides_df.drop(columns=["lpep_pickup_datetime"])

    rides_df["dropoff_date"] = rides_df["lpep_dropoff_datetime"].dt.normalize()
    rides_df = rides_df.drop(columns=["lpep_dropoff_datetime"])

    rides_df = rides_df.rename(columns={"RatecodeID": "ratecode_id"})

    rides_df = rides_df.rename(columns={"PULocationID": "pickup_location_id"})

    rides_df = rides_df.rename(columns={"DOLocationID": "dropoff_location_id"})

    return rides_df


def remove_entries_with_zero_passenger(rides_df: pd.DataFrame) -> pd.DataFrame:

    rides_df = rides_df.copy()

    rides_df = rides_df[rides_df["passenger_count"] != 0].reset_index(drop=True)

    return rides_df


def remove_entries_with_missing_passenger_count(rides_df: pd.DataFrame) -> pd.DataFrame:

    rides_df = rides_df.copy()

    rides_df = rides_df.dropna(subset=["passenger_count"]).reset_index(drop=True)

    return rides_df


def define_total_amount_per_passenger_count(rides_df: pd.DataFrame) -> pd.DataFrame:

    rides_df = rides_df.copy()

    rides_df["total_amount_per_passenger"] = rides_df["total_amount"] / rides_df["passenger_count"]

    return rides_df


def main(rides_df: pd.DataFrame) -> pd.DataFrame:
    rides_df = rename_snake_case_normalize_datetime(rides_df)
    rides_df = remove_entries_with_zero_passenger(rides_df)
    rides_df = remove_entries_with_missing_passenger_count(rides_df)
    rides_df = define_total_amount_per_passenger_count(rides_df)

    return rides_df


if __name__ == "__main__":
    pass