"""Read a daily revenue report from a local Parquet file."""

from pathlib import Path

import pandas as pd


def read_daily_revenue_report(report_filepath: str | Path) -> pd.DataFrame:
    """Read a daily revenue report from a Parquet file."""
    return pd.read_parquet(report_filepath)


if __name__ == "__main__":
    report = read_daily_revenue_report(Path("data/output/revenue_report.parquet"))
    print(
        report.to_string(
            index=False,
            formatters={"daily revenue ($)": "${:,.2f}".format},
        )
    )