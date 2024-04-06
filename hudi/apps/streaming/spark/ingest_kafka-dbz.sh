#!/bin/bash
name=hudi-apps-ingest-kafka-dbz

docker container stop $name
docker container rm $name
docker run --rm -it --name $name \
    -v "./../../../config/spark-defaults.conf:/opt/spark/conf/spark-defaults.conf:ro" \
    -v "./../../../config/log4j2.properties:/opt/spark/conf/log4j2.properties:ro" \
    -v "./kafka-source.properties:/app/hudi/conf/kafka-source.properties:ro" \
    -p "4040:4040" \
    --network trunk-network \
    tientq/spark:3.4.1 \
        spark-submit \
            --class org.apache.hudi.utilities.streamer.HoodieStreamer \
            /opt/spark/jars/hudi-utilities-bundle_2.12-0.14.0.jar \
            --props "file:///app/hudi/conf/kafka-source.properties" \
            --continuous \
            --schemaprovider-class "org.apache.hudi.utilities.schema.SchemaRegistryProvider" \
            --source-class "org.apache.hudi.utilities.sources.debezium.PostgresDebeziumSource#PostgresDebeziumSource" \
            --table-type MERGE_ON_READ \
            --target-base-path "s3a://datalake/dvdrental/actor_cdc_spark" \
            --target-table "actor_cdc_spark"
