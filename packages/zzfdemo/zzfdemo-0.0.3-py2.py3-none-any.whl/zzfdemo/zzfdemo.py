"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps,GeoJSON
import json
class Map(ipyleaflet.Map):
    
    def __init__(self,center=[34.32, 108.55],zoom=4, **kwargs):
        super().__init__(center = center,zoom = zoom ,**kwargs)
        self.add_control(ipyleaflet.LayersControl())
    
    def add_tile_layer(self,url,name , **kwargs):
        layer = ipyleaflet.TileLayer(url = url,name = name ,**kwargs)
        self.add_layer(layer)

    def add_basemap(self,name):
        if isinstance(name,str):
            url = eval(f'basemaps.{name}').build_url()
            self.add_tile_layer(url,name)
        else:
            self.add_layer(name)

    def add_geojson(self,fileName,name = 'geojson',**kwargs):
        if isinstance(fileName,str):
            with open(f'{fileName}') as f:
                data = json.load(f)

        if "style" not in kwargs:
            kwargs["style"] = {
                'opacity': 1, 'dashArray': '9', 'fillOpacity': 0.1, 'weight': 1
            }
        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {
                'color': 'red', 'dashArray': '0', 'fillOpacity': 0.5
            }
        layer = GeoJSON(data = data,name = name ,**kwargs)
        self.add(layer)


    def add_shapefile(self,fileName,name = 'shapefile',**kwargs):
        import shapefile
    

        if isinstance(fileName,str):
            with shapefile.Reader(fileName) as shp:
                data = shp.__geo_interface__

        if "style" not in kwargs:
            kwargs["style"] = {
                'opacity': 1, 'dashArray': '9', 'fillOpacity': 0.1, 'weight': 1
            }
        if "hover_style" not in kwargs:
            kwargs["hover_style"] = {
                'color': 'red', 'dashArray': '0', 'fillOpacity': 0.5
            }
        layer = GeoJSON(data = data,name = name ,**kwargs)
        self.add(layer)
    