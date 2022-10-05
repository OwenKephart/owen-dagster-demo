import pandas as pd
from dagster import asset, DailyPartitionsDefinition


daily_partitions = DailyPartitionsDefinition(start_date="2022-06-01")


@asset(compute_kind="feature_tool")
def weekly_feature(weekly_pop_rollup) -> None:
    """A feature for our model"""
    pass


@asset(compute_kind="feature_tool")
def summary_feature(population_summary) -> None:
    """A feature for our model"""
    pass


@asset(partitions_def=daily_partitions, compute_kind="ml_tool")
def population_forecast_model(weekly_feature, summary_feature) -> None:
    """Trained ML model for forecasting population"""
    pass


@asset(partitions_def=daily_partitions, compute_kind="ml_tool")
def forecasted_population(population_forecast_model) -> None:
    """Table containing forecasted population data"""
    pass
