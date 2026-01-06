# Charger Station 


#### Project Overview
This project is a data-driven application for analytics of charger station in sweden.
This project include data collection, processing and structure data into a unified data modele, as well as the development of an orchestration data pipeline. The processed data is visualized in an interactive dashboard.

#### How to get the API-key
- start with going to Nobil's website
- send a request for an API-key (will take around 1-3 working days before getting the API-key)
- When you have your API-key, create a .env-file and put your key in a variable

#### How to run
- Install uv 
- Install dependencies
- Setup a Snowflake account
- Extract data to database
- Transform and testing the data
- Run dashboard

***To install dependencies:***
```
uv add
```

***Dependencies:***
``` "dagster-webserver>=1.12.3",
    "dagster>=1.12.3",
    "dagster-dbt>=0.28.3",
    "dagster-dlt>=0.28.3",
    "dbt-core>=1.10.15",
    "dbt-duckdb>=1.10.0",
    "dlt[duckdb,snowflake]>=1.18.2",
    "duckdb>=1.4.2",
    "ipykernel>=7.1.0",
    "pandas>=2.2.2",
    "python-dotenv>=1.0.1",
    "streamlit>=1.52.2",
    "plotly-express>=0.4.1",
    "dbt-snowflake>=1.11.0",
    "matplotlib>=3.10.8",
```

#### Setup Snowflake
- Create account on Snowflake, download snowflake-extension in Visual studio code. Sign in with your account on Snowflake in Visual studio code 
- Create 3 different user in a new file under worksheet (user: extract_data, transform_data, present_data) 
- Create credentials in a .dlt/secrets.toml in the data_extract folder (make sure your .toml file is in .gitignore)
```
[destination.snowflake.credentials]
database = "your created databse" 
username = "extract_data" 
password = "<password for extract_data>" # please set me up!
host = "<account identifier>" # please set me up!  
warehouse = "<your created warehouse>" 
role = "dlt_role" 
```


In profiles.yml for DBT
```
dbt_snowflake:
  target: dev
  outputs:
    dev:
      type: snowflake
      account: <your account name> # fill in this field
      user: transform_data
      password: <your password for transform_data> # fill in this field
      role: dbt_role
      database: <your created database>
      warehouse: <your created warehouse>
      schema: staging
      client_session_keep_alive: False
```

#### Extract and load data

**How to run DLT**

This project you need to run 2 DLT script before orchestration. Navigate to src/data_extract, run this:

***Extract data dump (only need to run once)*** 
```
uv run extract_data_dump.py
```

***Extract trafikanalys*** 
```
uv run dlt_trafikanalys.py
``` 

#### Data transformation
Before orchestration, navigate to src/data_transform and run:
```
uv run dbt deps
```

#### Orchestration
To automate data pipeline for ingestion and transformation with Dagster orchestration. Add .dlt to the orchestration folder: orchestration/.dlt/secrets.toml
```
uv run dagster dev -f definition.py
```

#### Streamlit
Visualisation for the transformed data with an ineractive dashboard. 
- In your .env-file:
```
SNOWFLAKE_USER="present_data"
SNOWFLAKE_PASSWORD= "<password for present_data>" # please set me up
SNOWFLAKE_ACCOUNT="<account identifier>"
SNOWFLAKE_WAREHOUSE="<your warehouse>"
SNOWFLAKE_DATABASE="<your database>"
SNOWFLAKE_SCHEMA="marts"
SNOWFLAKE_ROLE="streamlit_role"
``` 

run in terminal:
```
uv run stramlit run main.py
```


#### Docker
The purpose with docker compose is to keep the dagster script running without using UI. It is not a necessity for the pipeline to work, rather it allows data engineer team to work with the same code without being restricted to one machine.

> **Note:** need to manually activate jobs in UI first time

