from pathlib import Path
import dlt 
import json
import os 
path_to_data= Path(__file__).parents[1]/ "data/population.json"

path_duckdb = str(Path(__file__).parents[1]/"data_warehouse/data.duckdb")


def looping():
    with open(path_to_data, "r" ) as file:
        data = json.loads(file.read())
    for d in data["columns"]:
        yield d


def run_pipeline(table_name):
    pipeline= dlt.pipeline(
        pipeline_name= "reading_Json",
        destination=dlt.destinations.duckdb(path_duckdb),
        dataset_name= "staging"
    )
    info = pipeline.run(data=looping(), table_name = table_name) 
    return info

if __name__ == "__main__":
    table_name = "municipalities_population"
    run_pipeline(table_name = table_name)