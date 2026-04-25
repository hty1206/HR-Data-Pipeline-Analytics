import os
import urllib.parse
from sqlalchemy import create_engine, text
from dotenv import load_dotenv

load_dotenv()

def run_silver_transformation():

    user = os.getenv("DB_USER")
    pw = urllib.parse.quote_plus(os.getenv("DB_PASSWORD"))
    host = os.getenv("DB_HOST")
    db = os.getenv("DB_NAME")
    
    engine = create_engine(f"mysql+pymysql://{user}:{pw}@{host}:4000/{db}?ssl_verify_cert=false")

    sql_path = "sql/silver/02_transform_hr_silver.sql"
    
    with engine.begin() as conn:
        with open(sql_path, "r", encoding="utf-8") as f:
            commands = f.read().split(';')
            for cmd in commands:
                if cmd.strip():
                    conn.execute(text(cmd))
    
    print("✅ 同步完成！")

if __name__ == "__main__":
    run_silver_transformation()