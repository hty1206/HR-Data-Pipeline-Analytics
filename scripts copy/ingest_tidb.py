import os
import pandas as pd
import urllib.parse
from sqlalchemy import create_engine
from dotenv import load_dotenv


load_dotenv()
df = pd.read_csv("data/HRDataset_raw.csv")

user = os.getenv("DB_USER")
password = os.getenv("DB_PASSWORD")
host = os.getenv("DB_HOST")
db = os.getenv("DB_NAME")

safe_password = urllib.parse.quote_plus(password)
connection_string = f"mysql+pymysql://{user}:{safe_password}@{host}:4000/{db}?ssl_verify_cert=false&ssl_verify_identity=false"
engine = create_engine(connection_string)

try:
    df.to_sql('hr_raw_data', con=engine, if_exists='replace', index=False)
    print("✅ 數據成功匯入！")
except Exception as e:
    print(f"❌ 匯入失敗: {e}")