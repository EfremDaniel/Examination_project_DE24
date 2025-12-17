import dlt 
from pathlib import Path
import pandas as pd



db_path = str(Path(__file__).parents[1] /"data_warehouse/data.duckdb")


def transform_excel_json(file, sheet_name):

    df = pd.read_excel(path/file, sheet_name= sheet_name)

    df = df.reset_index().rename({"index": "id"}, axis=1)
    df["id"] = df["id"].apply(lambda x: x+1)

    data = df.to_dict(orient= "records")

    return data

@dlt.resource(write_disposition="replace", name= "trafikanalys")  
def load_trafikanalys(file, sheet_name):
    
    batch = transform_excel_json(file= file, sheet_name= sheet_name)
    
    for raw in batch:
        yield raw
        

def run_pipeline(file, sheet_name):
    
    pipeline = dlt.pipeline(
        pipeline_name= "trafikanalys",
        destination= dlt.destinations.duckdb(db_path),
        dataset_name= "staging"
    )
        
    info = pipeline.run(data= [load_trafikanalys(file=file, sheet_name= sheet_name)])
    
    return info


if __name__=="__main__":
    
    path = Path(__file__).parents[1] /"data"
    path_to_file = path/"trafikanalys.xlsx"
    
    sheet_name = "Data"
    
    run_pipeline(file=path_to_file, sheet_name= sheet_name)
    
