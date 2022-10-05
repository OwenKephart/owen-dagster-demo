import os

from dagster import (
    repository,
    load_assets_from_package_module,
    file_relative_path,
    with_resources,
    define_asset_job,
    ScheduleDefinition,
)

from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource

from dagster_snowflake import build_snowflake_io_manager
from dagster_snowflake_pandas import SnowflakePandasTypeHandler

from assets_dbt_python.assets import population, forecasting

snowflake_io_manager = build_snowflake_io_manager([SnowflakePandasTypeHandler()])

DBT_PROJECT_DIR = file_relative_path(__file__, "../dbt_project")


@repository
def my_repository():
    population_assets = load_assets_from_package_module(
        population,
        group_name="population",
        key_prefix="owen",
    )
    transformation_assets = load_assets_from_dbt_project(
        project_dir=DBT_PROJECT_DIR,
        profiles_dir=DBT_PROJECT_DIR,
        key_prefix="owen",
    )
    forecasting_assets = load_assets_from_package_module(
        forecasting,
        group_name="forecasting",
    )
    all_assets = population_assets + transformation_assets + forecasting_assets
    return [
        with_resources(
            all_assets,
            resource_defs={
                "io_manager": snowflake_io_manager.configured(
                    {
                        "account": os.getenv("SNOWFLAKE_ACCOUNT", ""),
                        "user": os.getenv("SNOWFLAKE_USER", ""),
                        "password": os.getenv("SNOWFLAKE_PASSWORD", ""),
                        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", ""),
                        "database": "SANDBOX",
                    }
                ),
                "dbt": dbt_cli_resource.configured(
                    {"profiles_dir": DBT_PROJECT_DIR, "project_dir": DBT_PROJECT_DIR}
                ),
            },
        ),
        ScheduleDefinition(
            job=define_asset_job("compute_weekly_feature", selection="*weekly_feature"),
            cron_schedule="@weekly",
        ),
    ]
