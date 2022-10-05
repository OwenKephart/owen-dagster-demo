import os
import json

from dagster import repository, load_assets_from_package_module, file_relative_path, with_resources

from assets_dbt_python.assets import population, forecasting


@repository
def my_repository():
    return []
