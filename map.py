from urllib.request import urlopen
import json
with open('gz_2010_us_040_00_5m.json') as response:
    states = json.load(response)

import pandas as pd, csv
df = pd.read_csv("covid19_vaccinations_in_the_united_states.csv", dtype={"State": str}, skiprows=3)
df2 = pd.read_csv("united_states_covid19_cases_and_deaths_by_state.csv", skiprows=3)
df.rename(columns={"State/Territory/Federal Entity":"State"}, inplace=True)
df2.rename(columns={"State/Territory/Federal Entity":"State"}, inplace=True)
df.drop(df.index[5], inplace=True)
df.drop(df.index[9], inplace=True)
df.drop(df.index[17], inplace=True)
df.drop(df.index[25], inplace=True)
df.drop(df.index[52], inplace=True)
df2["Total Cases"][38] += df2["Total Cases"][39]
df2.drop(df2.index[39], inplace=True)
df2.drop(df2.index[44], inplace=True)
df2.drop(df2.index[58], inplace=True)
df["Total Cases"] = [total_case for total_case in df2["Total Cases"]]
df["# Vaccinated/Total Cases"] = [vaccinated/total_case for total_case, vaccinated in zip(df["Total Cases"], df["Total Administered"])]

import plotly.express as px

fig = px.choropleth(df, geojson=states, locations="State", color="# Vaccinated/Total Cases", featureidkey="properties.NAME",
                           color_continuous_scale="Bugn",
                           range_color=(0, 1),
                           scope="usa",
                           labels={"Total Administered" : "Vaccines Administered"},
                           hover_data={"State", "Total Administered"}
                          )
fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})
fig.show()
