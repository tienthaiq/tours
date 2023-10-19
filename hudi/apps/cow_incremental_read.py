# Query COW table incrementally

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit, to_timestamp

TABLE_PATH = "s3a://datalake/dvdrental/actor_2"

spark = SparkSession.builder.getOrCreate()

spark.read.format("hudi").load(TABLE_PATH).createOrReplaceTempView("actor")
commits = list(map(
    lambda row: row[0],
    spark.sql("SELECT DISTINCT(_hoodie_commit_time) AS commitTime FROM actor ORDER BY commitTime").limit(10).collect()
))
start_time = commits[-2]

spark.read.format("hudi") \
    .options(**{
        "hoodie.datasource.query.type": "incremental",
        "hoodie.datasource.read.begin.instanttime": start_time,
    }) \
    .load(TABLE_PATH) \
    .show(n=10000, truncate=False)
