create user dbt with encrypted password 'M!Secr3t';

-- Grant read on raw data
\connect dvdrental;
grant usage on schema public to dbt;
grant select on all tables in schema public to dbt;

grant create on database dvdrental to dbt;
