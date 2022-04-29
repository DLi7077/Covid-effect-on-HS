# https://plotly.com/python/mapbox-county-choropleth/
import plotly.express as px
import json

boroughLocations = json.load(open('Borough Boundaries.geojson'))

from attenVSgraduation import totalData

for year in range(2017, 2022):
  df = totalData.loc[totalData['year']==year]
  
  # map annual graduation
  gradFig = px.choropleth_mapbox(
    df,
    geojson=boroughLocations,
    locations= 'Borough',
    featureidkey="properties.boro_name",
    color= 'graduation_rate',
    color_continuous_scale='GnBu',
    range_color=(.69, .90),
    mapbox_style="carto-positron",
    zoom=9.7, center = {"lat": 40.7128, "lon": -74.0060},
    title=f'{year} Average Graduation Rate'
  )
  # gradFig.show()
  
  # map annual attendance rate
  attFig = px.choropleth_mapbox(
    df,
    geojson=boroughLocations,
    locations= 'Borough',
    featureidkey="properties.boro_name",
    color= 'attendance_rate',
    color_continuous_scale='GnBu',
    range_color=(.84, .91),
    mapbox_style="carto-positron",
    zoom=9.7, center = {"lat": 40.7128, "lon": -74.0060},
    title=f'{year} Average Attendance Rate'
  )
  # attFig.show()