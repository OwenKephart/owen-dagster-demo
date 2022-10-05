import os
import json

from dagster import repository, load_assets_from_package_module, file_relative_path, with_resources

from assets_dbt_python.assets import population, forecasting


from dagster_snowflake import build_snowflake_io_manager
from dagster_snowflake_pandas import SnowflakePandasTypeHandler

from dagster_dbt import load_assets_from_dbt_project, dbt_cli_resource

snowflake_io_manager = build_snowflake_io_manager([SnowflakePandasTypeHandler()])

DBT_PROJECT_DIR = file_relative_path(__file__, "../dbt_project")


@repository
def my_repository():
    population_assets = load_assets_from_package_module(
        population,
        group_name="population",
        key_prefix="owen",
    )
    dbt_assets = load_assets_from_dbt_project(
        project_dir=DBT_PROJECT_DIR, profiles_dir=DBT_PROJECT_DIR
    )
    forecasting_assets = load_assets_from_package_module(
        forecasting,
        group_name="forecasting",
    )

    all_assets = population_assets + dbt_assets + forecasting_assets
    return [
        with_resources(
            all_assets,
            {
                "dbt": dbt_cli_resource.configured(
                    {"profiles_dir": DBT_PROJECT_DIR, "project_dir": DBT_PROJECT_DIR}
                ),
                "io_manager": snowflake_io_manager.configured(
                    {
                        "account": os.getenv("SNOWFLAKE_ACCOUNT", ""),
                        "user": os.getenv("SNOWFLAKE_USER", ""),
                        "password": os.getenv("SNOWFLAKE_PASSWORD", ""),
                        "warehouse": os.getenv("SNOWFLAKE_WAREHOUSE", ""),
                        "database": "SANDBOX",
                    }
                ),
            },
        )
    ]
