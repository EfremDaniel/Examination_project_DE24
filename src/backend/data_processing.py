import duckdb
from pathlib import Path

PATH_DUCKDB = Path(__file__).parents[1] / "data_warehouse" / "data.duckdb"


def query_analytics(query):
    
    with duckdb.connect(PATH_DUCKDB, read_only=True)  as conn:
        df = conn.execute(query).fetchdf()
        return df

  
