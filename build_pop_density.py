"""
Build data/pop_density.csv by joining:
  - 2025_Gaz_counties_national.txt  (FIPS, land area in sq mi)
  - co-est2025-pop.csv              (2025 population estimates)
Output columns: fips, county_name, state_abbr, pop_2025, land_sqmi, pop_density
"""

import pandas as pd

STATE_ABBR = {
    "Alabama": "AL", "Alaska": "AK", "Arizona": "AZ", "Arkansas": "AR",
    "California": "CA", "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE",
    "District of Columbia": "DC", "Florida": "FL", "Georgia": "GA", "Hawaii": "HI",
    "Idaho": "ID", "Illinois": "IL", "Indiana": "IN", "Iowa": "IA",
    "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA", "Maine": "ME",
    "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI", "Minnesota": "MN",
    "Mississippi": "MS", "Missouri": "MO", "Montana": "MT", "Nebraska": "NE",
    "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ", "New Mexico": "NM",
    "New York": "NY", "North Carolina": "NC", "North Dakota": "ND", "Ohio": "OH",
    "Oklahoma": "OK", "Oregon": "OR", "Pennsylvania": "PA", "Rhode Island": "RI",
    "South Carolina": "SC", "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX",
    "Utah": "UT", "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
    "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
    "Puerto Rico": "PR",
}

# --- Gazetteer -----------------------------------------------------------------
gaz = pd.read_csv(
    "2025_Gaz_counties_national.txt",
    sep="|",
    dtype={"GEOID": str},
    usecols=["USPS", "GEOID", "NAME", "ALAND_SQMI"],
)
gaz["fips"] = gaz["GEOID"].str.zfill(5)
gaz = gaz.rename(columns={"USPS": "state_abbr", "NAME": "county_name", "ALAND_SQMI": "land_sqmi"})

# --- Population estimates ------------------------------------------------------
pop_raw = pd.read_csv("co-est2025-pop.csv", header=None, skiprows=4, skipfooter=5,
                      engine="python")
# Columns: geographic_area, base_2020, 2020, 2021, 2022, 2023, 2024, 2025
pop_raw.columns = ["geo", "base_2020", "pop_2020", "pop_2021",
                   "pop_2022", "pop_2023", "pop_2024", "pop_2025"]

# Drop summary rows (no leading dot) and the US total
pop = pop_raw[pop_raw["geo"].str.startswith(".")].copy()
pop["geo"] = pop["geo"].str.lstrip(".")   # e.g. "Autauga County, Alabama"

# Split "County Name, State Name"
pop[["county_name", "state_name"]] = pop["geo"].str.rsplit(",", n=1, expand=True)
pop["county_name"] = pop["county_name"].str.strip()
pop["state_name"]  = pop["state_name"].str.strip()
pop["state_abbr"]  = pop["state_name"].map(STATE_ABBR)

# Clean population: remove commas, cast to int
pop["pop_2025"] = pop["pop_2025"].astype(str).str.replace(",", "").str.strip()
pop["pop_2025"] = pd.to_numeric(pop["pop_2025"], errors="coerce")

pop = pop[["county_name", "state_abbr", "state_name", "pop_2025"]].dropna(subset=["state_abbr"])

# --- Join on (county_name, state_abbr) -----------------------------------------
merged = gaz.merge(pop, on=["county_name", "state_abbr"], how="inner")

# --- Population density --------------------------------------------------------
merged["pop_density"] = merged["pop_2025"] / merged["land_sqmi"]

# --- Save ----------------------------------------------------------------------
out = merged[["fips", "county_name", "state_abbr", "state_name",
              "pop_2025", "land_sqmi", "pop_density"]].sort_values("fips")
out.to_csv("data/pop_density.csv", index=False)

print(f"Wrote data/pop_density.csv — {len(out):,} counties")
print(out.describe()[["pop_2025", "land_sqmi", "pop_density"]].round(2))

# Warn about unmatched rows
unmatched_gaz = len(gaz) - len(merged)
unmatched_pop = len(pop) - len(merged)
if unmatched_gaz or unmatched_pop:
    print(f"\nUnmatched — gazetteer: {unmatched_gaz}  |  population: {unmatched_pop}")
