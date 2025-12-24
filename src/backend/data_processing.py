import os 
from pathlib import Path
from dotenv import load_dotenv
import snowflake.connector
import pandas as pd

PATH_DUCKDB = Path(__file__).parents[1] / "data_warehouse" / "data.duckdb"


def query_analytics(mart):
    
    load_dotenv()

    with snowflake.connector.connect(
        user=os.getenv("SNOWFLAKE_USER"),
        password=os.getenv("SNOWFLAKE_PASSWORD"),
        account=os.getenv("SNOWFLAKE_ACCOUNT"),
        warehouse=os.getenv("SNOWFLAKE_WAREHOUSE"),
        database=os.getenv("SNOWFLAKE_DATABASE"),
        schema=os.getenv("SNOWFLAKE_SCHEMA"),
        role=os.getenv("SNOWFLAKE_ROLE") )as conn:
        
        if mart == 'nr_charger':
            query = 'SELECT * FROM marts.nr_charger;'
        else:
            query = 'SELECT * FROM marts.infrastructur;'
         
        cur = conn.cursor()   
        data =cur.execute(query)
        
        df = data.fetch_pandas_all()
        
        return df
        
        
        

  
