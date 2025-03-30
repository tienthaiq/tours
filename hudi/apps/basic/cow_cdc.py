# Query CDC table

from pyspark.sql import SparkSession, DataFrame
from pyspark.sql.functions import lit, to_timestamp

TABLE_PATH = "s3a://datalake/dvdrental/actor_2"

spark = SparkSession.builder.getOrCreate()

# Get commit start time to ignore the first commit of bulk write
spark.read.format("hudi").load(TABLE_PATH).createOrReplaceTempView("actor")
commits = list(map(
    lambda row: row[0],
    spark.sql("SELECT DISTINCT(_hoodie_commit_time) AS commitTime FROM actor ORDER BY commitTime").limit(10).collect()
))
start_time = str(int(commits[1]) - 1)

spark.read.format("hudi"). \
    options(**{
        "hoodie.datasource.query.incremental.format": "cdc",
        "hoodie.datasource.query.type": "incremental",
        "hoodie.datasource.read.begin.instanttime": start_time,
    }). \
    load(TABLE_PATH) \
    .show(1000, False)

# It shows all changes
# |op |ts_ms            |before                                                                                        |after                                                                                           |
# +---+-----------------+----------------------------------------------------------------------------------------------+------------------------------------------------------------------------------------------------+
# |i  |20231015160652257|null                                                                                          |{"actor_id": 1003, "first_name": "foo3", "last_name": "bar4", "last_update": 1672617600000000}  |
# |i  |20231015160652257|null                                                                                          |{"actor_id": 1002, "first_name": "foo2", "last_name": "bar2", "last_update": 1672531200000000}  |
# |i  |20231015160652257|null                                                                                          |{"actor_id": 1001, "first_name": "foo1", "last_name": "bar1", "last_update": 1672531200000000}  |
# |u  |20231015160654886|{"actor_id": 1001, "first_name": "foo1", "last_name": "bar1", "last_update": 1672531200000000}|{"actor_id": 1001, "first_name": "newFoo", "last_name": "bar1", "last_update": 1672531200000000}|
# |d  |20231015160656714|{"actor_id": 1002, "first_name": "foo2", "last_name": "bar2", "last_update": 1672531200000000}|null   