# Simple write Spark application with insert, update & delete

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit, to_timestamp

SOURCE_PATH = "s3a://datalake/dvdrental/actor"
SINK_PATH = "s3a://datalake/dvdrental/actor_2"


def read_table(path: str) -> DataFrame:
    return spark.read.format("hudi").load(path)


def update_table(dataframe: DataFrame, options: dict = None):
    options = options or {}
    dataframe.write.format("hudi") \
        .options(**options) \
        .mode("append") \
        .save(SINK_PATH)


spark = SparkSession.builder.getOrCreate()

write_options = {
    "hoodie.table.name": "actor",
    "hoodie.datasource.write.recordkey.field": "actor_id",
    "hoodie.datasource.write.precombine.field": "last_update",
    "hoodie.table.cdc.enabled": "true",
}

# Clone table
input_df = read_table(SOURCE_PATH)
# Create table with 1 record
input_df.limit(1) \
    .write.format("hudi") \
    .options(**write_options) \
    .mode("overwrite") \
    .save(SINK_PATH)
# Then upsert the rest
update_table(input_df, write_options)

# Inserted new records
# There are two records with actor_id = 1003, but only one with bigger last_update remains
columns = ["actor_id", "first_name", "last_name", "last_update"]
data =[(1001, "foo1", "bar1", "2023-01-01"),
       (1002, "foo2", "bar2", "2023-01-01"),
       (1003, "foo3", "bar3", "2023-01-01"),
       (1003, "foo3", "bar4", "2023-01-02")]
inserts = spark.createDataFrame(data) \
    .toDF(*columns) \
    .withColumn("last_update", to_timestamp("last_update", "yyyy-MM-dd"))
update_table(inserts, write_options)

print("Show inserted records")
read_table(SINK_PATH) \
    .filter("actor_id > 1000") \
    .show(n=100, truncate=False)

# Update record actor_id = 1001
update_df = read_table(SINK_PATH) \
    .filter("actor_id = 1001") \
    .withColumn("first_name", lit("newFoo"))
update_table(update_df, write_options)

print("Show updated records")
read_table(SINK_PATH) \
    .filter("actor_id > 1000") \
    .show(n=100, truncate=False)

# Delete record actor_id = 1002
delete_df = read_table(SINK_PATH).filter("actor_id = 1002")

update_table(
    delete_df,
    options={"hoodie.datasource.write.operation": "delete"}
)
print("Show remaining records")
read_table(SINK_PATH) \
    .filter("actor_id > 1000") \
    .show(n=100, truncate=False)