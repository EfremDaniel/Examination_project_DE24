from dotenv import load_dotenv
import os
from datetime import date
import datetime


load_dotenv()

API_KEY_NOBIL = os.getenv("API_KEY_NOBIL")



x = datetime.datetime.now()
DATE_NOW = date(x.year, x.month, x.day).isoformat()