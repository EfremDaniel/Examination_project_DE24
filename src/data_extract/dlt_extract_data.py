import requests
from constans.utils import API_KEY_NOBIL
import sys
import dlt 
from pathlib import Path


path_duckdb = str(Path(__file__).parents[1]/"data_warehouse/data.duckdb")

def _get_url():
    
    params = {
        "apikey": API_KEY_NOBIL,
        "countrycode": "SWE",
        "format": "json",
        "file": "false"
    }
    
    url = "https://nobil.no/api/server/datadump.php"
    
    r = requests.get(url= url, params= params) 
    r.raise_for_status()
    
    if r.status_code != 200:
        print("Fel (body):", r.text[:400])
        sys.exit(1)
 
    try:
        data = r.json()
    except Exception:
        print("Svar kunde inte tolkas som JSON. Rätt svar:")
        print(r.text[:800])
        sys.exit(1)
    
    if not data:
        print("Ingen data returnerad.")
        sys.exit(0)
        
    else:
        return data



@dlt.resource(write_disposition= "replace")
def charge_station_data():
        
    data = _get_url()
    
    batch = data.get("chargerstations", [])
    
    if not batch:
        print("DEBUG: No data - stopping processe")
        
    for station in batch:
        yield station
        
        
def run_pipeline(table_name):
    pipeline= dlt.pipeline(
        pipeline_name= "charger_station",
        destination=dlt.destinations.duckdb(path_duckdb),
        dataset_name= "staging"
    )
    
    
    info = pipeline.run(data= charge_station_data(), table_name=table_name)
    
    return info


if __name__=="__main__":
    
    table_name = "nobil_dump"
    run_pipeline(table_name= table_name)

