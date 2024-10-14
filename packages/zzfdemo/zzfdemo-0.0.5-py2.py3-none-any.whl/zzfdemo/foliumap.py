import folium
from ipyleaflet import basemaps,GeoJSON,WidgetControl
import ipywidgets as widgets
class Map(folium.Map):
    def __init__(self, center=[34.32, 108.55],zoom=4, **kwargs):
        super().__init__(location=center, zoom_start=zoom, **kwargs)


    def add_raster(self , data ,name ,zoom_to_layer = True,**kwargs):
        """在Map中添加栅格数据；

        Args:
            data (str): 栅格数据；
            name (str): 栅格数据的名称；
        """
        try:
            from localtileserver import TileClient, get_folium_tile_layer
        except:
            raise ImportError("请下载localtileserver包")
        
        client = TileClient(data)
        layer = get_folium_tile_layer(client,name = name,**kwargs)
        layer.add_to(self)
        # self.add_layer(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom

