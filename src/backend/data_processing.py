import duckdb
from pathlib import Path


PATH_DUCKDB = Path(__file__).parents[1] / "data_warehouse" / "data.duckdb"


def query_analytics(mart):
    
    with duckdb.connect(PATH_DUCKDB, read_only=True) as conn:
        
        if mart == 'nr_charger':
            query = 'SELECT * FROM marts.nr_charger;'
        else:
            query = 'SELECT * FROM marts.infrastructur;'
            
        curser = conn.execute(query=query)
        
        df = curser.fetchdf()
        
        return df
        
        
        

  
