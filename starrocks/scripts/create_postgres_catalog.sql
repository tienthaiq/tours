CREATE EXTERNAL CATALOG dvdrental
PROPERTIES
(
    "type"="jdbc",
    "user"="postgres",
    "password"="M!Secr3t",
    "jdbc_uri"="jdbc:postgresql://starrocks-ext-postgres:5432/dvdrental",
    "driver_url"="https://repo1.maven.org/maven2/org/postgresql/postgresql/42.3.3/postgresql-42.3.3.jar",
    "driver_class"="org.postgresql.Driver"
);