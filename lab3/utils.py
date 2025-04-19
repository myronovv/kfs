import pandas as pd
import mysql.connector

def load_db():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='2505',
        database='weather_data'
    )
    query = "SELECT * FROM weather"
    df = pd.read_sql(query, con=connection)
    connection.close()
    return df

def preprocess_data(df):
    df['last_updated'] = pd.to_datetime(df['last_updated'])
    df['month'] = df['last_updated'].dt.month
    df['day'] = df['last_updated'].dt.day
    df = df.dropna(subset=['air_quality_pm2_5'])
    df['label'] = (df['air_quality_pm2_5'] < 25).astype(int)
    return df