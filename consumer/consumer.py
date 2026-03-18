from pyspark.sql import SparkSession
from pyspark.sql.types import StructField, StructType, StringType, TimestampType, FloatType
from pyspark.sql.functions import from_json, col
import os 

#diirectory where spark will store its checkpoint data. crucial in streaming to enable fault tolerance
checkpoint_dir = '/tmp/checkpoint/kafka_to_postgres'
if not os.path.exists(checkpoint_dir):
    os.makedirs(checkpoint_dir)


postgres_config ={
    "url":"jdbc:postgresql://postgres:5432/stock_data",
    "user":"admin",
    "password":"admin",
    "dbtable":"stocks",
    "driver":"org.postgresql.Driver"
}


#The schmea/struct matching the now data coming from Kafka
kafka_data_schema = StructType([
    StructField("date", StringType()),
    StructField("high", StringType()),
    StructField("low", StringType()),
    StructField("open", StringType()),
    StructField("close", StringType()),
    StructField("symbol", StringType()) 
])

#initiaizing spark application with sparksession
spark = (SparkSession.builder
         .appName('KafkaSparkStreaming')
         .getOrCreate())

#reading from Kafka as a stream
df = (spark.readStream.format("kafka")
    .option("kafka.bootstrap.servers", "kafka:9092")
    .option("subscribe", "stock_analysis")
    .option("startingOffsets", "latest") #read only new incoming messages 
    .option("failOnDataLoss", "false") #if kafka deletes old messages(retention), spark wont crash
    .load() #start reading the kafka topic as a stream
)

parsed_df = df.selectExpr(
    "CAST(value AS STRING)") \
    .select(from_json(col("value"), kafka_data_schema).alias("data")).select("data.*")


#casting and selecting final columns
processed_df = parsed_df.select(
    col("date").cast(TimestampType()).alias("date"),
    col("high").alias("high"),
    col("low").alias("low"),
    col("open").alias("open"),
    col("close").alias("close"),
    col("symbol").alias("symbol"),
)
#Display results to the terminal (console output)
# query = processed_df.writeStream \
#     .outputMode("append") \
#     .format("console") \
#     .option("truncate", "false") \
#     .option("checkpointLocation", checkpoint_dir) \
#     .start()


def write_to_postgres(batch_df, batch_id):
    """
    Writes a microbatch dataframe to postgres using JDBC in 'append' mode
    """
    batch_df.write \
        .format('jdbc') \
        .mode('append') \
        .options(**postgres_config) \
        .save()

#Stream Data to Postgres using foreachBatch
query = (
    processed_df.writeStream
    .foreachBatch(write_to_postgres) #use foreachBatch for JDBC sinks
    .option("checkpointLocation", checkpoint_dir) #directory where spark will store its
    .OutputMode('append')
    .start()
)
#wait for a manual termination of the  pipeline
query.awaitTermination()


