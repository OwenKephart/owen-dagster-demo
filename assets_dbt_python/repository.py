import json
from dagster import repository, load_assets_from_package_module, file_relative_path, with_resources
from dagster_dbt import load_assets_from_dbt_manifest, dbt_cli_resource

from assets_dbt_python.assets import forecasting, population

DBT_PROJECT_DIR = file_relative_path(__file__, "../dbt_project")
DBT_PROFILES_DIR = file_relative_path(__file__, "../dbt_project/config")


@repository
def my_repository():
    all_assets = (
        load_assets_from_package_module(
            population,
            group_name="population",
        )
        + load_assets_from_dbt_manifest(
            json.load(open(DBT_PROJECT_DIR + "/target/manifest.json")),
        )
        + load_assets_from_package_module(
            forecasting,
            group_name="forecasting",
        )
    )

    return [
        with_resources(
            all_assets,
            resource_defs={
                "dbt": dbt_cli_resource.configured(
                    {"project_dir": DBT_PROJECT_DIR, "profiles_dir": DBT_PROFILES_DIR}
                )
            },
        )
    ]
