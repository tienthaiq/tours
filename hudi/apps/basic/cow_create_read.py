# Simple read-write Spark application
# Read from PostgreSQL

from pyspark.sql import SparkSession

TABLE_PATH = "s3a://datalake/dvdrental/actor"

spark = SparkSession.builder.getOrCreate()

df = (
    spark.read.format("jdbc")
    .option("url", "jdbc:postgresql://postgres:5432/dvdrental")
    .option("dbtable", "public.actor")
    .option("user", "postgres")
    .option("password", "M!Secr3t")
    .load()
)

print(f"Read: {df.count()} records")

(
    df.write.format("hudi")
    .options(**{
        'hoodie.table.name': "actor",
        # 'hoodie.datasource.write.partitionpath.field': 'city'
    })
    .mode("overwrite")
    .save(TABLE_PATH)
)

spark.read.format("hudi").load(TABLE_PATH).show(n=1000, truncate=False)
