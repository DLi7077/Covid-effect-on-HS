# https://plotly.com/python/choropleth-maps/
import plotly.express as px

from attenVSgraduation import totalData
geojson = 'Borough Boundaries.geojson'
print(geojson["features"][0]["properties"])

