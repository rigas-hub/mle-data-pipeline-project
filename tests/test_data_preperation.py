import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_frame_equal

from src.data_cleaning import (
    define_total_amount_per_passenger_count,
    remove_entries_with_missing_passenger_count,
    remove_entries_with_zero_passenger,
    rename_snake_case_normalize_datetime,
)


@pytest.mark.parametrize(
    "input_frame, expected_result",
    [
        (
            pd.DataFrame(
                {
                    "VendorID": [2],
                    "lpep_pickup_datetime": pd.to_datetime(["2025-01-01 00:03:01"]),
                    "lpep_dropoff_datetime": pd.to_datetime(["2025-01-01 00:17:12"]),
                    "RatecodeID": [1.0],
                    "PULocationID": [75],
                    "DOLocationID": [235],
                    "passenger_count": [1.0],
                    "total_amount": [34.00],
                }
            ),
            pd.DataFrame(
                {
                    "vendor_id": [2],
                    "ratecode_id": [1.0],
                    "pickup_location_id": [75],
                    "dropoff_location_id": [235],
                    "passenger_count": [1.0],
                    "total_amount": [34.00],
                    "pickup_date": pd.to_datetime(["2025-01-01"]),
                    "dropoff_date": pd.to_datetime(["2025-01-01"]),
                }
            ),
        )
    ],
)
def test_rename_snake_case_normalize_datetime(input_frame, expected_result):
    output_frame = rename_snake_case_normalize_datetime(input_frame)
    assert_frame_equal(output_frame, expected_result)
    assert isinstance(output_frame, pd.DataFrame)


@pytest.mark.parametrize(
    "input_frame, expected_result",
    [
        (
            pd.DataFrame(
                {
                    "VendorID": [2, 1, 2],
                    "lpep_pickup_datetime": pd.to_datetime(
                        [
                            "2025-01-01 00:03:01",
                            "2025-01-01 01:03:01",
                            "2025-01-01 02:03:01",
                        ]
                    ),
                    "lpep_dropoff_datetime": pd.to_datetime(
                        [
                            "2025-01-01 00:17:12",
                            "2025-01-01 01:17:12",
                            "2025-01-01 02:17:12",
                        ]
                    ),
                    "RatecodeID": [1.0, 1.0, 1.0],
                    "PULocationID": [75, 76, 77],
                    "DOLocationID": [235, 236, 237],
                    "passenger_count": [0.0, 1.0, 0.0],
                    "total_amount": [34.00, 35.00, 36.00],
                }
            ),
            pd.DataFrame(
                {
                    "VendorID": [1],
                    "lpep_pickup_datetime": pd.to_datetime(["2025-01-01 01:03:01"]),
                    "lpep_dropoff_datetime": pd.to_datetime(["2025-01-01 01:17:12"]),
                    "RatecodeID": [1.0],
                    "PULocationID": [76],
                    "DOLocationID": [236],
                    "passenger_count": [1.0],
                    "total_amount": [35.00],
                },
            ),
        )
    ],
)
def test_remove_entries_with_zero_passenger(input_frame, expected_result):
    output_frame = remove_entries_with_zero_passenger(input_frame)
    assert_frame_equal(output_frame, expected_result)
    assert isinstance(output_frame, pd.DataFrame)


@pytest.mark.parametrize(
    "input_frame, expected_result",
    [
        (
            pd.DataFrame(
                {
                    "VendorID": [2, 1, 2],
                    "lpep_pickup_datetime": pd.to_datetime(
                        [
                            "2025-01-01 00:03:01",
                            "2025-01-01 01:03:01",
                            "2025-01-01 02:03:01",
                        ]
                    ),
                    "lpep_dropoff_datetime": pd.to_datetime(
                        [
                            "2025-01-01 00:17:12",
                            "2025-01-01 01:17:12",
                            "2025-01-01 02:17:12",
                        ]
                    ),
                    "RatecodeID": [1.0, 1.0, 1.0],
                    "PULocationID": [75, 76, 77],
                    "DOLocationID": [235, 236, 237],
                    "passenger_count": [np.nan, 1.0, np.nan],
                    "total_amount": [34.00, 35.00, 36.00],
                }
            ),
            pd.DataFrame(
                {
                    "VendorID": [1],
                    "lpep_pickup_datetime": pd.to_datetime(["2025-01-01 01:03:01"]),
                    "lpep_dropoff_datetime": pd.to_datetime(["2025-01-01 01:17:12"]),
                    "RatecodeID": [1.0],
                    "PULocationID": [76],
                    "DOLocationID": [236],
                    "passenger_count": [1.0],
                    "total_amount": [35.00],
                },
            ),
        )
    ],
)
def test_remove_entries_with_missing_passenger_count(input_frame, expected_result):
    output_frame = remove_entries_with_missing_passenger_count(input_frame)
    assert_frame_equal(output_frame, expected_result)
    assert isinstance(output_frame, pd.DataFrame)


@pytest.mark.parametrize(
    "input_frame, expected_result",
    [
        (
            pd.DataFrame(
                {
                    "VendorID": [2],
                    "lpep_pickup_datetime": pd.to_datetime(["2025-01-01 00:03:01"]),
                    "lpep_dropoff_datetime": pd.to_datetime(["2025-01-01 00:17:12"]),
                    "RatecodeID": [1.0],
                    "PULocationID": [75],
                    "DOLocationID": [235],
                    "passenger_count": [2.0],
                    "total_amount": [34.00],
                }
            ),
            pd.DataFrame(
                {
                    "VendorID": [2],
                    "lpep_pickup_datetime": pd.to_datetime(["2025-01-01 00:03:01"]),
                    "lpep_dropoff_datetime": pd.to_datetime(["2025-01-01 00:17:12"]),
                    "RatecodeID": [1.0],
                    "PULocationID": [75],
                    "DOLocationID": [235],
                    "passenger_count": [2.0],
                    "total_amount": [34.00],
                    "total_amount_per_passenger": [17.00],
                }
            ),
        )
    ],
)
def test_rename_define_total_amount_per_passenger_count(input_frame, expected_result):
    output_frame = define_total_amount_per_passenger_count(input_frame)
    assert_frame_equal(output_frame, expected_result)
    assert isinstance(output_frame, pd.DataFrame)
