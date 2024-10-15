from quartic_sdk.pipelines.sources.base_source import SourceApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS, get_truststore_password
from pydantic import BaseModel
import os
import json
import time
import pyodbc
from datetime import datetime
import pytz
import pandas as pd
from typing import Any

class DeltavConfig(BaseModel):
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: str
    DBNAME: str




class Deltav(SourceApp):
    connector_class: str = CONNECTOR_CLASS.DeltaV.value
    connector_config: DeltavConfig
    topic_to_push_to: str = None
    last_processed_value: str = ''
    timestamp_file: str = ''
    tz: Any = None
    last_seen_file: str = ''
    conn: Any = None

    def process_records(self, spark,batch_df):
        if batch_df.empty:
            return
        latest = pytz.utc.localize(datetime.utcnow(), is_dst=None).astimezone(self.tz).strftime("%Y-%m-%d %X")
        on_df = batch_df[batch_df['endtime']>latest]

        self.last_processed_value = on_df['endtime'].min()


        # Write the last processed timestamp to the file
        with open(self.timestamp_file, "w+") as f:
            f.write(self.last_processed_value)

        if self.transformation:
            batch_df = self.transformation(batch_df)
        
        if self.timestamp_columns:
            for column in self.timestamp_columns:
                batch_df[column] = batch_df[column].astype('int64')//1e6        

        self.write_data(spark, batch_df)
        
    
    def get_last_processed_timestamp(self):
        if os.path.exists(self.timestamp_file):
            with open(self.timestamp_file, "r") as f:
                return f.read().strip()
            
        return pytz.utc.localize(datetime.utcnow(), is_dst=None).astimezone(self.tz).strftime("%Y-%m-%d %X") 

    def get_last_seen(self):
        try:
            with open(self.last_seen_file, 'r') as file:
                json_data = json.load(file)
                return json_data
        except Exception as e:
            print(e)
            return {}
    def write_last_seen(self, data):
        with open(self.last_seen_file, 'w+') as file:
            json.dump(data, file)
    
    def get_write_data(self, batch_df):

        last_seen = self.get_last_seen()
        data = []
        
        for _, row in batch_df.iterrows():
            recipe = row['recipe']
            up = row['unitprocedure']
            op = row['operation']
            phase = row['phase']
            hash = f"{str(recipe)}_{str(up)}_{str(op)}_{str(phase)}"
            if hash in last_seen and last_seen[hash] == [row['starttime'], row['endtime']]:
                continue 
            last_seen[hash] = [row['starttime'], row['endtime']]
            data.append((row['uniqueid'], row.to_json()))
        self.write_last_seen(last_seen)
        return data


    def start(self, id, kafka_topics, source=[]):
        self.id = id
        self.tz = pytz.timezone("US/Eastern")
        self.topic_to_push_to = kafka_topics[0]
        self.timestamp_columns = ["starttime", "endtime"]
        checkpoint_dir = f'/app/data/checkpoints/connector{self.id}'
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        self.timestamp_file = os.path.join(checkpoint_dir, "last_processed_timestamp.txt")
        self.last_seen_file = os.path.join(checkpoint_dir, "last_seen.json")
        self.last_processed_value = self.get_last_processed_timestamp()
        conn_str = f'DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={self.connector_config.HOST};DATABASE={self.connector_config.DBNAME};UID={self.connector_config.USERNAME};PWD={self.connector_config.PASSWORD};Encrypt=yes;TrustServerCertificate=yes'
        self.conn = pyodbc.connect(conn_str)
        from pyspark.sql import SparkSession
        spark = SparkSession.builder \
            .appName(f"SourceConnector_{self.id}") \
            .getOrCreate()
        while(True):
            query = f"SELECT t2.description AS recipe, t1.unitprocedure, t1.operation, t1.phase, t1.unit, t1.uniqueid, t1.starttime, t1.endtime FROM batchrecipeview AS t1 LEFT JOIN batchview AS t2 ON t1.uniqueid = t2.uniqueid WHERE t1.starttime >= '{self.last_processed_value}' ORDER BY t1.endtime DESC;"
            df = pd.read_sql(query, self.conn)
            self.process_records(spark, df )
            time.sleep(30)

