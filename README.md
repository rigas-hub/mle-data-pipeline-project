# Data Pipeline Project

Use this repository as a **template** for your data pipeline project. You will build a pipeline that takes raw NYC taxi trip records and turns them into a processed result. The project is open-ended: the brief sets the goal, and the structure, tools, and implementation choices are yours to make. Create pull requests in your own copy even if you are working alone, and use them to track your progress.

## Learning Objectives

By the end of this repository, you should be able to:

- Write a script that downloads a public dataset into a local staging directory.
- Build a pipeline that reads staged Parquet files and aggregates them into daily metrics.
- Separate a pipeline into distinct extract, transform, and load stages.
- Explain the difference between ETL and ELT, and justify which one your pipeline uses.
- Orchestrate a pipeline with Prefect (stretch goal).

## Project Brief

IIn this project you are going to build a data pipeline that processes the Green Taxi Trips portion of the NYC Taxi Trip dataset (https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page).

1. Write a script that downloads the data for the first three months of 2025 and stores it in a local staging directory.
2. Write an ETL or ELT pipeline that reads the locally staged files, processes the data, and calculates revenue per day.

Bonus task, if you have time:

1. Use Prefect for workflow orchestration.

How to approach it

Step 1: Extract (brief task 1) · Revisit: data ingestion
- List what the download needs: host, file name per month, months, target folder
- Build each file's link from those pieces
- Request each file and save it to your staging directory
- Decide what happens when you run it again

Step 2: Explore · Revisit: data quality
- Load one file into a notebook (notebooks to experiment only) 
- Find the columns you need: when the trip happened and what was paid
- Check them: data types, missing values, value ranges for dates and amounts
- Note what needs cleaning before you can add up revenue per day

Step 3: Transform and load (brief task 2) · Revisit: ETL vs. ELT, dbt
- Choose ETL or ELT: transform in Python before loading, or load raw data and transform in SQL
- Read the staged files
- Clean based on what you found in Step 2
- Group by day and sum the revenue
- Write the result to your output location
- Compare row counts before and after cleaning

Step 4: Orchestrate (bonus) · Revisit: Prefect
- Get the plain pipeline running end to end first
- Turn each stage into a task and the whole run into a flow
- Add retries where things can fail

Suggested folder structure

```text
<your-repo>/
├── data/
│   ├── raw/                  # Step 1: staged downloads, never edited
│   └── processed/            # Step 3: your daily revenue output
├── notebooks/                # Step 2: exploration only (not part of the pipeline)
├── src/
│   └── <package-name>/
│       ├── <stage modules>   # Steps 1 + 3: one per stage, e.g. extract / transform / load
│       ├── <entry point>     # Step 3: runs the stages in order
│       └── <flow>            # Step 4: the Prefect version
├── tests/                    # Step 3: at least one test for your transform
└── README.md                 # how to run it + answers to the review questions
```


(Notebooks are only for experimenting and exploring the data. The pipeline itself lives in src/ and runs without them.)

## Learning Path

### Additional Folders and Files

| File / Folder | Description |
|---|---|
| [**solution**](solution/) | A complete local ETL implementation with its own README, scripts, package, and tests. |
| [**pyproject.toml**](pyproject.toml) | Project configuration and dependencies. |
| [**uv.lock**](uv.lock) | Dependency lock file. |

## Setup

Use [uv](https://docs.astral.sh/uv/getting-started/installation/) 0.13.5 or newer
and Python 3.13.17 or a newer 3.13 patch release, as defined in
[`.python-version`](.python-version).

> [!NOTE]
> Throughout these steps, text in angle brackets like `<repo-name>` is a **placeholder**. Replace it, including the `< >` brackets, with your own value. For example, `cd <repo-name>` becomes `cd mle-data-pipeline-project`.

### 1. Create the Repository from the Template

Click **Use this template** on GitHub.

When creating the repository:

- Set yourself as the **Owner**
- Choose a repository name
- Disable **Include all branches**
- Click **Create repository**

> [!IMPORTANT]
> If you are working in pairs or groups, only **one person** should complete this step.

---

### 2. Add Collaborators (Pairs/Groups Only)

If working with teammates:

1. Open the repository on GitHub
2. Go to **Settings → Collaborators**
3. Add your teammates as collaborators
4. Share the repository link with your team

Teammates should accept the invitation before continuing.

---

### 3. Clone the Repository

Copy the SSH URL from the **Code** button on GitHub, then run:

```bash
git clone <copied-ssh-url>
```

The copied SSH URL will look like `git@github.com:<your-username>/<repo-name>.git`.

---

### 4. Move into the Project Folder and Install Dependencies

This installs all dependencies and creates a virtual environment in `.venv/`.

```bash
cd <repo-name>
uv sync
```

---

### 5. Open the Repository in VS Code

> [!NOTE]
> Make sure you open VS Code from the project root so it automatically detects the environment created by `uv sync`.

Launch VS Code in the project root folder:

```bash
code .
```

If you create a notebook to explore the data, select the Python environment created by `uv sync` as the kernel.

## Reference Solution

This repository includes a complete local reference implementation in [solution/](solution/).
Use it to compare implementation choices and expected outputs. It is one way to solve the project, not the required structure for yours.

See [solution/README.md](solution/README.md) for how to run it and how its files fit together.

## Answer the Following Questions

1. What are the steps you took to complete the project?
2. What challenges did you face?
3. What would you do differently if you had more time?


## New how-to's

Download the local Parquet file for the first three months of 2025:

```bash
uv run python src/data_ingestion.py --year 2025 --months 1 --months 2 --months 3 --output-dir data/raw
```

For setting up the local PostgreSQL database in Docker, into which the data will be loaded, the following steps are needed:

- Make sure Docker Desktop is running before you execute any Docker commands.

- Create a Docker network:
```bash
docker network create ny-taxi
```

- Create a local data directory for ensuring that the database contents survive container restarts:
```bash
mkdir -p db-data
```

- Start PostgreSQL:
```bash
docker run -d \
  --name ny-taxi-db \
  --network ny-taxi \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=postgres \
  -e POSTGRES_DB=ny_taxi \
  -v "$(pwd)/db-data:/var/lib/postgresql/data" \
  -p 5432:5432 \
  postgres:17
```

- Verify that the container is running:
```bash
docker ps --filter "name=ny-taxi-db"
```

Prefect is used for the pipeline orchestration. Use one terminal to start it:
```bash
uv run prefect server start
```

Use another terminal to point Prefect at that server:
```bash
uv run prefect config set PREFECT_API_URL=http://127.0.0.1:4200/api
```

The pipeline uses a Prefect block named ny-taxi-connector and this can be created or overwritten safely by:
```bash
uv run python src/create_sqlalchemy_block.py
```

The pipeline, which extracts the raw data, transforms it, loads it into a PostgreSQL database and makes useful queries, can run now as follows:
```bash
uv run python src/etl_pipeline.py 
```

Finally, the report based on those queries can be read:
```bash
uv run python src/revenue_report.py 
```

...

Run the tranformation tests:
```bash
uv run python -m pytest -q .\tests\test_data_preperation.py
```

The code can be formatted with the help of the linter Ruff:
```bash
uv run ruff check src tests
```

Don't forget to answer the project questions, list the files used and possibly their purspose and in the very end reform this README to make it proper for the final project submission. 