import datetime

from airflow.sdk import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from cosmos.airflow.task_group import DbtTaskGroup
from cosmos.config import ProjectConfig, ProfileConfig
from cosmos.profiles import PostgresUserPasswordProfileMapping, DbtProfileConfigVars
from cosmos.operators import DbtDocsS3Operator

dbt_project_config = ProjectConfig(dbt_project_path="/opt/dbt")
dbt_profile_config = ProfileConfig(
    profile_name="airflow_dbt",
    target_name="prod",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id="postgresql_dwh",
        profile_args={
            "schema": "dwh",
        },
        dbt_config_vars=DbtProfileConfigVars(
            send_anonymous_usage_stats=False,
        ),
    )
)

with DAG(
    dag_id="airflow_dbt_daily",
    description="daily",
    schedule=None,
    start_date=datetime.datetime(2025, 3, 29),
    max_active_runs=1,
    catchup=False,
) as dag:
    (
        EmptyOperator(task_id="pre_build")
        >> DbtTaskGroup(
            group_id="build",
            project_config=dbt_project_config,
            profile_config=dbt_profile_config,
            operator_args={
                "install_deps": True,
            }
        )
        >> EmptyOperator(task_id="post_build")
        >> DbtDocsS3Operator(
            task_id="generate_docs",
            project_dir="/opt/dbt",
            profile_config=dbt_profile_config,
            connection_id="minio",
            bucket_name="airflow-dbt",
            folder_dir="dbt/docs",
            install_deps=True,
        )
    )
