#!/bin/bash

docker container stop hudi-apps
docker container rm hudi-apps
docker run --rm -it --name hudi-apps \
    -v "./apps:/apps" \
    -v "./config/spark-defaults.conf:/opt/spark/conf/spark-defaults.conf:ro" \
    -v "./config/log4j2.properties:/opt/spark/conf/log4j2.properties:ro" \
    -p "4040:4040" \
    --network trunk-network \
    tientq/spark:3.4.1 \
        spark-submit $1
