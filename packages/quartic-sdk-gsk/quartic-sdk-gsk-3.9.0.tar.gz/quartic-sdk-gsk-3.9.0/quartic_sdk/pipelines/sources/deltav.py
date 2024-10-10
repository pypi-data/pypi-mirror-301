from quartic_sdk.pipelines.sources.base_source import SourceApp
from quartic_sdk.pipelines.connector_app import CONNECTOR_CLASS, get_truststore_password
from pydantic import BaseModel
import os
import json
import time

class DeltavConfig(BaseModel):
    USERNAME: str
    PASSWORD: str
    HOST: str
    PORT: str
    DBNAME: str
    UPDATE_COLUMN: str
    QUERY: str
    TIMESTAMP_COLUMNS: list




class Deltav(SourceApp):
    connector_class: str = CONNECTOR_CLASS.DeltaV.value
    connector_config: DeltavConfig
    topic_to_push_to: str = None
    last_processed_value: str = ''
    timestamp_file: str = ''
    

    def process_records(self, spark, batch_df):
        if batch_df.empty:
            return
        max_timestamp = batch_df[self.connector_config.UPDATE_COLUMN].max()
        self.last_processed_value = max_timestamp.strftime('%Y-%m-%d %X') if max_timestamp else self.last_processed_value

        # Write the last processed timestamp to the file
        with open(self.timestamp_file, "w+") as f:
            f.write(self.last_processed_value)

        if self.transformation:
            batch_df = self.transformation(batch_df)
        
        if self.connector_config.TIMESTAMP_COLUMNS:
            for column in self.connector_config.TIMESTAMP_COLUMNS:
                batch_df[column] = batch_df[column].astype('int64')//1e9
        self.write_data(spark, batch_df)
        
    
    def get_last_processed_timestamp(self):
        if os.path.exists(self.timestamp_file):
            with open(self.timestamp_file, "r") as f:
                return f.read().strip()
        return "2021-01-01 00:00:00"  


    def start(self, id, kafka_topics, source=[]):
        self.id = id
        self.topic_to_push_to = kafka_topics[0]
        checkpoint_dir = f'/app/data/checkpoints/connector{self.id}'
        if not os.path.exists(checkpoint_dir):
            os.makedirs(checkpoint_dir)
        self.timestamp_file = os.path.join(checkpoint_dir, "last_processed_timestamp.txt")
        self.last_processed_value = self.get_last_processed_timestamp()
        from pyspark.sql import SparkSession

        spark = SparkSession.builder \
            .appName(f"SourceConnector_{self.id}") \
            .getOrCreate()
        mssql_url = f"jdbc:sqlserver://{self.connector_config.HOST}:{self.connector_config.PORT};databaseName={self.connector_config.DBNAME};user={self.connector_config.USERNAME};password={self.connector_config.PASSWORD}"
        properties = {
            "driver": "com.microsoft.sqlserver.jdbc.SQLServerDriver"
        }
        while True:
            batchDF = spark.read \
                .format("jdbc") \
                .option("url", mssql_url) \
                .option("dbtable", f"({self.connector_config.QUERY} WHERE {self.connector_config.UPDATE_COLUMN} > '{self.last_processed_value}') AS temp_table") \
                .options(**properties) \
                .load()
            if not batchDF.isEmpty():
                self.process_records(spark, batchDF.toPandas())
            time.sleep(30)

