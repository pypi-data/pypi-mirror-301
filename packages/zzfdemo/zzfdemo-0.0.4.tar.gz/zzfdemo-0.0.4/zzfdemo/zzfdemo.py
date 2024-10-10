"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps,GeoJSON
import json
class Map(ipyleaflet.Map):
    """这是一个继承自ipyleaflet.Map的类，用于快速创建地图对象；

    Args:
        ipyleaflet (Map): ipyleaflet.Map的子类，用于创建地图对象；
    """
    def __init__(self,center=[34.32, 108.55],zoom=4, **kwargs):
        """初始化地图对象；

        Args:
            center (list, optional): 设置地图中心点. 默认为[34.32, 108.55].
            zoom (int, optional): 设置地图缩放级别. 默认为4.
        """
        super().__init__(center = center,zoom = zoom ,**kwargs)
        self.add_control(ipyleaflet.LayersControl())
    
    def add_tile_layer(self,url,name , **kwargs):
        """添加瓦片图层；

        Args:
            url (str): 瓦片图层的url地址；
            name (str): 瓦片图层的名称；
        """
        layer = ipyleaflet.TileLayer(url = url,name = name ,**kwargs)
        self.add_layer(layer)

    def add_basemap(self,name = "OpenTopoMap"):
        """添加底图，支持的底图主要是ipyelaflet.basemaps中的底图；
        ipyleaflet.basemaps中的底图查看https://ipyleaflet.readthedocs.io/en/latest/map_and_basemaps/basemaps.html；

        Args:
            name (str,optional): ipyleaflet.basemaps中的底图名称
        """
        if isinstance(name,str):
            url = eval(f'basemaps.{name}').build_url()
            self.add_tile_layer(url,name)
        else:
            self.add_layer(name)

    def add_geojson(self,fileName,name = 'geojson',**kwargs):
        """添加json格式的矢量数据；

        Args:
            fileName (str): json格式的矢量数据文件路径；
            name (str, optional): 矢量数据的名称. 默认为'geojson'.
        """
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
        """添加shapefile格式的矢量数据；

        Args:
            fileName (str): shapefile格式的矢量数据文件路径；
            name (str, optional): 矢量数据的名称. 默认为'shapefile'.
        """
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
    
      