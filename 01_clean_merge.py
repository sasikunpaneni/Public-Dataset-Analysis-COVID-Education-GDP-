
"""
01_clean_merge.py
Loads raw CSVs, cleans & merges to master_facts and helper tables.
"""
import os
import pandas as pd

BASE = os.path.dirname(os.path.dirname(__file__))
RAW = os.path.join(BASE, "data", "raw")
PROC = os.path.join(BASE, "data", "processed")

OWID_FILE = os.path.join(RAW, "owid-covid-data.csv")
GDP_FILE  = os.path.join(RAW, "gdp_per_capita.csv")
EDU_FILE  = os.path.join(RAW, "education_index.csv")
INCOME_FILE = os.path.join(RAW, "country_income_groups.csv")  # optional

def export(df, name):
    path = os.path.join(PROC, name)
    df.to_csv(path, index=False)
    print(f"Saved: {path} rows={len(df)}")

def main():
    # Load OWID
    owid_cols = ["iso_code","location","date","continent","new_cases","new_deaths","population"]
    covid = pd.read_csv(OWID_FILE, usecols=owid_cols, parse_dates=["date"])
    covid = covid[~covid["iso_code"].str.startswith("OWID")]
    covid["new_cases"] = covid["new_cases"].fillna(0)
    covid["new_deaths"] = covid["new_deaths"].fillna(0)
    covid["country"] = covid["location"].astype(str).str.strip()
    covid["year"] = covid["date"].dt.year
    covid["month"] = covid["date"].dt.to_period("M").astype(str)

    # Load GDP & Education
    gdp = pd.read_csv(GDP_FILE)
    gdp.columns = [c.strip().lower() for c in gdp.columns]
    edu = pd.read_csv(EDU_FILE)
    edu.columns = [c.strip().lower() for c in edu.columns]

    # Optional income groups
    if os.path.exists(INCOME_FILE):
        inc = pd.read_csv(INCOME_FILE)
        inc.columns = [c.strip().lower() for c in inc.columns]
    else:
        inc = pd.DataFrame(columns=["country","income_group"])

    # Annualize COVID
    covid_year = (covid.groupby(["country","continent","year"], as_index=False)
                  .agg(new_cases_year=("new_cases","sum"),
                       new_deaths_year=("new_deaths","sum"),
                       population=("population","max")))

    master = (covid_year
              .merge(gdp, on=["country","year"], how="left")
              .merge(edu, on=["country","year"], how="left"))
    if not inc.empty:
        master = master.merge(inc, on="country", how="left")

    master["cases_per_100k"] = (master["new_cases_year"]/master["population"]*1e5).round(3)
    master["deaths_per_100k"] = (master["new_deaths_year"]/master["population"]*1e5).round(3)

    export(master, "master_facts.csv")

    covid_continent_month = (covid.groupby(["continent","month"], as_index=False)
                             .agg(new_cases=("new_cases","sum"),
                                  new_deaths=("new_deaths","sum")))
    export(covid_continent_month, "covid_by_continent_month.csv")

    country_attributes = (master.sort_values(["country","year"]).groupby("country", as_index=False)
                          .agg(continent=("continent","first"),
                               latest_year=("year","max"),
                               income_group=("income_group","first")))
    export(country_attributes, "country_attributes.csv")

if __name__ == "__main__":
    main()
