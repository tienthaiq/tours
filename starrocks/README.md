# Play with StarRocks
https://www.starrocks.io/

## 1. Deploy on Docker

## 2. Deploy on Kubernetes

### 2.1. Classic StarRocks

### 2.2. Shared-data StarRocks

#### 2.2.1. Dependencies

Docker-based components:

* S3 (Minio)
* MySQL
* Postgres
* Hive metastore

#### 2.2.2. Setup

* K8s:
  * 3 nodes
  * Use TopoLVM for persistent volume
* StarRocks cluster
  * 3 FEs
  * 3 BEs
  * Deploy via Helm chart
