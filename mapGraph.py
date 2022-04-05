"""
https://medium.com/geekculture/three-ways-to-plot-choropleth-map-using-python-f53799a3e623
https://geopandas.org/en/stable/gallery/polygon_plotting_with_folium.html
https://python-visualization.github.io/folium/modules.html
"""
import folium
import covidData as covid

casesin2020= covid.BoroDatabyYear(2020)
print(casesin2020)

boro_geo ='Borough Boundaries.geojson'


map =folium.Map(location= [40.7831, -73.9712],zoom_start=10)
Area= folium.Choropleth(
  geo_data=boro_geo,
  data= casesin2020,
  columns=['boro_name',"Cases"],
  key_on="features.properties.boro_name",
  fill_color="BuGn",
  fill_opacity=.1,
  line_opacity=1,
  # threshold_scale= [0,20,50,70,1000000],
  highlight=True
).add_to(map)

map.save(outfile= 'boroughs.html')

# thasnia
# tasnia