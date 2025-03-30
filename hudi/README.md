## Apache Hudi playground

#### 1. Basic Spark applications

* Create & read copy-on-write (COW) table
* Insert, update & delete records in COW table
* Incremetally read COW table
* CDC read COW table
* CRIUD + incremental read on merge-on-read (MOR) table
* Time travel query
* Read-optimized query on MOR table # TODO

#### 2. Feature dive

* Timeline
  * Commit archive
* Index
* Metadata table
* Query
  * Read
    * Snapshot (COW & MOR)
    * Optimized (MOR)
    * Incremental (COW & MOR)
    * Incremental CDC (COW)
  * Write
    * Insert
    * Upsert
    * Bulk insert
    * Insert overwrite
    * Delete
    * Insert overwrite
    * Delete partition
* Schema evolution
  * Type change
  * Add column
  * Rename column
  * Delete column
  * Complex changes (maybe incompatible)
* Key Generation
* Concurrency
  * MVCC
  * OCC
* Record payload

### 3. Streaming

#### 3.1 Spark structured streaming
#### 3.2 Flink

### 4. External integration

* Hive metastore
* Trino
* Datahub
* Prometheus
* S3A

### 5. Services

* Bootstrapping
* Compaction
* Clustering
  * Sorting
  * Space-filling curves
    * Zorder
    * Hilbert curve
* Metadata indexing
* Cleaning
* Transformer
* Rollback
* Marker
* Disaster recovery
* Exporter
* Validator
* Notification

### 6. Use cases

* Streaming data lake
  * INSERT intensive
  * UPDATE/DELETE intensive
  * History preserve
    * Soft delete
    * Schema change handling
      * Best-effort change handle
      * Incompatible changes & recovery
      * Change notification
* Streaming data warehouse
  * Flink
  * Monitoring
