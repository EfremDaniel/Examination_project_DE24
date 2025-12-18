import dlt
import requests
import sys
from constants.utils import API_KEY_NOBIL, DATE_NOW

dlt.config["load.truncate_staging_dataset"] = True


_catched_data = None


def _get_url():
    params = {
        "apikey": API_KEY_NOBIL,
        "countrycode": "SWE",
        "format": "json",
        "file": "false",
        "fromdate": DATE_NOW,
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
        print("Svar kunde inte tolkas som JSON.")
        print(r.text[:800])
        sys.exit(1)

    if not data:
        print("Ingen data returnerad.")
        sys.exit(0)

    return data


def _get_catched_data():
    global _catched_data
    if _catched_data is None:
        _catched_data = _get_url()
    return _catched_data



@dlt.resource(table_name="csmd",write_disposition="replace")
def csmd_data():
    data = _get_catched_data()
   
    stations = data.get("chargerstations", [])

    if not stations:
        return

    for station in stations:
        yield station["csmd"]


@dlt.resource(table_name="status_online", write_disposition="replace")
def status_online_data():
    
    data = _get_catched_data()
    
    stations = data.get("chargerstations", [])

    if not stations:
        return

    for station in stations:
        station_id = station["csmd"].get("id")
        update_date = station["csmd"].get("Updated")
        st_dict = station.get("attr", {}).get("st", {})

        for key, attr in st_dict.items():
            yield {
                "station_id": station_id,
                "updated_date": update_date,
                "attr_key": key,
                "attrtypeid": attr.get("attrtypeid"),
                "attrname": attr.get("attrname"),
                "attrvalid": attr.get("attrvalid"),
                "trans": attr.get("trans"),
                "attrval": attr.get("attrval"),
            }


@dlt.resource(table_name="connector", write_disposition="replace")
def connector_data():
    data = _get_catched_data()
    stations = data.get("chargerstations", [])

    if not stations:
        return

    for station in stations:
        station_id = station["csmd"].get("id")
        update_date = station["csmd"].get("Updated")
        conn_dict = station.get("attr", {}).get("conn", {})

        for connector_nr, attributes in conn_dict.items():
            for _, attr in attributes.items():
                yield {
                    "station_id": station_id,
                    "updated_date": update_date,
                    "connector_nr": connector_nr,
                    "attrtypeid": attr.get("attrtypeid"),
                    "attrname": attr.get("attrname"),
                    "attrvalid": attr.get("attrvalid"),
                    "trans": attr.get("trans"),
                    "attrval": attr.get("attrval"),
                }


@dlt.source
def nobil_source():
    return [
        csmd_data(),
        status_online_data(),
        connector_data(),
    ]

