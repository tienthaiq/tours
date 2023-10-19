# Create Hudi merge-on-read table
# Read from PostgreSQL

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit, to_timestamp

TABLE_PATH = "s3a://datalake/dvdrental/actor__mor"


def read_table() -> DataFrame:
    return spark.read.format("hudi").load(TABLE_PATH)


def update_table(dataframe: DataFrame, options: dict = None):
    options = options or {}
    dataframe.write.format("hudi") \
        .options(**options) \
        .mode("append") \
        .save(TABLE_PATH)


spark = SparkSession.builder.getOrCreate()

df = (
    spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://postgres:5432/dvdrental")
    .option("dbtable", "public.actor")
    .option("user", "postgres")
    .option("password", "M!Secr3t")
    .load()
)

print(f"Read: {df.count()} records from PostgreSQL")

(
    df.write.format("hudi")
    .options(**{
        "hoodie.table.name": "actor",
        "hoodie.datasource.write.table.type": "MERGE_ON_READ",
        "hoodie.datasource.write.recordkey.field": "actor_id",
        "hoodie.datasource.write.precombine.field": "last_update",
    })
    .mode("overwrite")
    .save(TABLE_PATH)
)

spark.read.format("hudi").load(TABLE_PATH).show(n=10, truncate=False)
write_options = {
    "hoodie.datasource.write.table.type": "MERGE_ON_READ",
}

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
read_table() \
    .filter("actor_id > 1000") \
    .show(n=100, truncate=False)

# Update record actor_id = 1001
update_df = read_table() \
    .filter("actor_id = 1001") \
    .withColumn("first_name", lit("newFoo"))
update_table(update_df, write_options)

print("Show updated records")
read_table() \
    .filter("actor_id > 1000") \
    .show(n=100, truncate=False)

# Delete record actor_id = 1002
delete_df = read_table().filter("actor_id = 1002")

update_table(
    delete_df,
    options={
        "hoodie.datasource.write.table.type": "MERGE_ON_READ",
        "hoodie.datasource.write.operation": "delete",
    }
)
print("Show remaining records")
read_table() \
    .filter("actor_id > 1000") \
    .show(n=100, truncate=False)

print("Total records: ", read_table().count())
