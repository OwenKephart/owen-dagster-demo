from dagster import asset
import pandas as pd


@asset
def country_population(context) -> pd.DataFrame:
    df = pd.read_html(
        "https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)"
    )[0]
    df.columns = ["country", "region", "subregion", "pop_2018", "pop_2019", "pct_change"]
    context.add_output_metadata({"num_rows": len(df)})
    return df


@asset
def continent_population(country_population: pd.DataFrame) -> pd.DataFrame:
    return country_population.groupby("region").sum()
