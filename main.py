import pandas as pd
import folium
from folium.plugins import MarkerCluster
from folium.plugins import MousePosition
from folium.features import DivIcon
from folium.plugins import HeatMap

import webbrowser

df = pd.read_csv("AB_US_2020.csv").head(1000)
df[['latitude', 'longitude']] = df[['latitude', 'longitude']].astype(float)
print('')

class LatLngPopup(MacroElement):
    """
    When one clicks on a Map that contains a LatLngPopup,
    a popup is shown that displays the latitude and longitude of the pointer.
    """
    _template = Template(u"""
            {% macro script(this, kwargs) %}
                var {{this.get_name()}} = L.popup();
                function latLngPop(e) {
                    {{this.get_name()}}
                        .setLatLng(e.latlng)
                        .setContent("Latitude: " + e.latlng.lat.toFixed(4) +
                                    "<br>Longitude: " + e.latlng.lng.toFixed(4))
                        .openOn({{this._parent.get_name()}});
                    parent.document.getElementById("id_lng").value = e.latlng.lng.toFixed(4); # add this
                    parent.document.getElementById("id_lat").value = e.latlng.lat.toFixed(4); # add this
                    }
                {{this._parent.get_name()}}.on('click', latLngPop);
            {% endmacro %}
            """)  # noqa

    def __init__(self):
        super(LatLngPopup, self).__init__()
        self._name = 'LatLngPopup'

# columnsNames = list(df.columns.values)
# countOfNull = []
# persentOfNull = []
# allValues = df['id'].size
#
# for column in columnsNames:
#     tdf = df[column]
#     counNull = tdf.isnull().sum().sum()
#     countOfNull.append(counNull)
#     persentOfNull.append(counNull / allValues * 100)
#
# df1 = pd.DataFrame({'Column_name': columnsNames, 'Number_of_null': countOfNull, 'Persent_of_null': persentOfNull})
# df1 = df1[df1['Number_of_null'] != 0]

# heat_data = [[row['latitude'], row['longitude']] for index, row in df.iterrows()]

world_map = folium.Map(location=[0, 0], zoom_start=6, tiles='Stamen Toner')

latitude = df['latitude']
longitude = df['longitude']
price = df['price']

for latitude, longitude, price in zip(latitude, longitude, price):
    folium.CircleMarker(location=[latitude, longitude],
                        radius=10,
                        popup=str(price) + "$",
                        fill_color='red',
                        color='black',
                        icon=folium.Icon(color='gray')).add_to(world_map)

# HeatMap(heat_data).add_to(world_map)

# saint_petersburg = folium.map.FeatureGroup()

# style the feature group
# saint_petersburg.add_child(
#     folium.features.CircleMarker(
#         [59.938732, 30.316229], radius = 5,    # широта и долгота Санкт-Петербурга
#         color = 'red', fill_color = 'Red'
#     )
# )

# add the feature group to the map
# world_map.add_child(saint_petersburg)

# label the Marker (пометить маркер)
# folium.Marker([59.938732, 30.316229],
# popup = 'Санкт-Петербург, в разговорной речи - Пи́тер, сокр.- СПб').add_to(world_map)


# formatter = "function(num) {return L.Util.formatNum(num, 5);};"
# mouse_position = MousePosition(
#     position='topright',
#     separator=' Long: ',
#     empty_string='NaN',
#     lng_first=False,
#     num_digits=20,
#     prefix='Lat:',
#     lat_formatter=formatter,
#     lng_formatter=formatter,
# )
#
# world_map.add_child(mouse_position)


world_map.save(r'E:\Загрузки 2.0\AirBnbProject\example.html')
webbrowser.open(r'E:\Загрузки 2.0\AirBnbProject\example.html')
