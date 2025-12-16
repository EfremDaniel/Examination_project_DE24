import requests
from constants.utils import API_KEY_NOBIL
import sys
import dlt
from pathlib import Path


path_duckdb = str(Path(__file__).parents[1] / "data_warehouse/data.duckdb")

_catched_data = None


def _get_url():

    params = {
        "apikey": API_KEY_NOBIL,
        "countrycode": "SWE",
        "format": "json",
        "file": "false",
    }

    url = "https://nobil.no/api/server/datadump.php"

    r = requests.get(url=url, params=params)
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


def _get_catched_data():
    global _catched_data
    if _catched_data is None:
        _catched_data = _get_url()
    return _catched_data


@dlt.resource(write_disposition="replace", name= "csmd_table_dump")
def csmd_data():

    data = _get_catched_data()

    batch = data.get("chargerstations", [])
    print(f"DEBUG: antal stationer i chargerstations: {len(batch)= }")

    if not batch:
        print("DEBUG: No data - stopping processe")
        return

    print("DEBUG: Start yield for pipeline")
    for station in batch:
        yield station["csmd"]


@dlt.resource(write_disposition="replace", name="status_online_table_dump")
def status_online_data():

    data = _get_catched_data()

    batch = data.get("chargerstations", [])
    print(f"DEBUG: antal stationer i chargerstations: {len(batch)= }")

    if not batch:
        print("DEBUG: No data - stopping processe")
        return

    print("Start yield for pipeline")
    for station in batch:

        station_id = station["csmd"].get("id")
        update_date = station["csmd"]["Updated"]
        st_dict = station["attr"]["st"]
        
        
        for key, attr in st_dict.items():

            yield {
                "station_id": station_id,
                "updated_date": update_date,
                "attr_key": key,
                "attrtypeid": attr.get("attrtypeid"),
                "attrname": attr.get("attrname"),
                'attrvalid': attr.get("attrvalid"),
                'trans': attr.get("trans"),
                'attrval': attr.get("attrval")
            }
        
@dlt.resource(write_disposition="replace", name="connector_table_dump")
def connector_data():

    data = _get_catched_data()

    batch = data.get("chargerstations", [])
    print(f"DEBUG: antal stationer i chargerstations: {len(batch)= }")

    if not batch:
        print("DEBUG: No data - stopping processe")
        return

    print("Start yield for pipeline")
    for station in batch:
      
        station_id = station["csmd"].get("id")
        update_date = station["csmd"]["Updated"]
        data_conn = station["attr"]["conn"]
        
        for connector in data_conn.keys():
            
            data_attribute = station["attr"]["conn"][connector]
            for key in data_attribute.keys():
                yield {
                    "station_id": station_id,
                    "updated_date": update_date,
                    "connector_nr": connector,
                    "attrtypeid": data_conn[connector][key].get("attrtypeid"),
                    "attrname": data_conn[connector][key].get("attrname"),
                    "attrvalid": data_conn[connector][key].get("attrvalid"),
                    "trans": data_conn[connector][key].get("trans"),
                    "attrval": data_conn[connector][key].get("attrval")
                }

def run_pipeline():
    pipeline = dlt.pipeline(
        pipeline_name="charger_station",
        destination=dlt.destinations.duckdb(path_duckdb),
        dataset_name="staging",
    )
    
    info = pipeline.run(data=[csmd_data(), status_online_data(), connector_data()])

    return info

if __name__ == "__main__":

    run_pipeline()
