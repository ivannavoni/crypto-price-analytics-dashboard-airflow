import requests
from datetime import datetime
import psycopg2
import pandas as pd

def extract_data():
    """Extract cryptocurrency prices from Binance API"""
    url = 'https://api.binance.com/api/v3/ticker/price'
    response = requests.get(url)
    data = response.json()
    
    cryptos = ['BTCUSDT', 'ETHUSDT', 'BNBUSDT', 'SOLUSDT', 'ADAUSDT']
    filtered_data = []

    for item in data:
        if item['symbol'] in cryptos:
            filtered_data.append({
                "symbol": item['symbol'],
                "price": float(item['price']),
                "time": datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S")
            })

    return filtered_data

def transform_data(data):
    """Validate that all prices are positive"""
    validated_data = []
    for record in data:
        if record['price'] > 0:
            validated_data.append(record)
    return validated_data

def export_postgre_and_excel(data):
    """Load data to PostgreSQL and generate Excel report"""
    connection = psycopg2.connect(
        host="db_crypto",
        database="postgres",
        user="postgres",
        password="password",
        port="5432"
    )

    with connection.cursor() as cursor:
        for record in data:
            # Insert data, skip duplicates based on unique constraint
            cursor.execute("""
                INSERT INTO crypto_prices (symbol, price, time)
                VALUES (%s, %s, %s)
                ON CONFLICT ON CONSTRAINT unique_symbol_time DO NOTHING
            """, (record["symbol"], record["price"], record["time"]))

    connection.commit()

    # Generate daily Excel report
    query = """
        SELECT * FROM crypto_prices
        WHERE time::date = CURRENT_DATE
    """
    df = pd.read_sql(query, connection)
    df.to_excel('/opt/airflow/scripts/daily_prices_report.xlsx', index=False)
    
    connection.close()

def run_etl():
    """Execute the complete ETL pipeline"""
    raw_data = extract_data()
    print(f"Extracted {len(raw_data)} records")
    
    clean_data = transform_data(raw_data)
    print(f"Transformed {len(clean_data)} records")

    export_postgre_and_excel(clean_data)
    print("ETL completed!")

if __name__ == "__main__":
    run_etl()