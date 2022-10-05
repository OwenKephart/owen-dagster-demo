import os

from dagster import (
    repository,
    load_assets_from_package_module,
    file_relative_path,
    with_resources,
    define_asset_job,
    ScheduleDefinition,
)

from assets_dbt_python.assets import population, forecasting


@repository
def my_repository():
    []
