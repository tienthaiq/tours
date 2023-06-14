CREATE EXTERNAL CATALOG sakila
PROPERTIES (
    "type"="jdbc",
    "user"="root",
    "password"="M!Secr3t",
    "jdbc_uri"="jdbc:mysql://starrocks-ext-mysql:3306",
    "driver_url"="https://repo1.maven.org/maven2/mysql/mysql-connector-java/8.0.28/mysql-connector-java-8.0.28.jar",
    "driver_class"="com.mysql.cj.jdbc.Driver"
);