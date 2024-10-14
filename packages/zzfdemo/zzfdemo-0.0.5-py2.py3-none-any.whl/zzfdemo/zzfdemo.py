"""Main module."""

import ipyleaflet
from ipyleaflet import basemaps,GeoJSON,WidgetControl
import json
import ipywidgets as widgets
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
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True
        super().__init__(center = center,zoom = zoom ,**kwargs)
        self.add_control(ipyleaflet.LayersControl())
        # self.add_basemap()
    
    def set_center(self,center=[34.32, 108.55],zoom = 4):
        """设置地图的中心点和缩放级别；

        Args:
            center (list, optional): 设置地图中心点. 默认为[34.32, 108.55].
            zoom (int, optional): 设置地图缩放级别. 默认为4.
        """
        self.center = center
        self.zoom = zoom

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

    def add_image(self , url , bounds , name = 'image',**kwargs):
        """在Map中添加图片；

        Args:
            url (str): 图片的url地址；
            bounds (list): 图片的经纬度范围；
            name (str, optional): 图片的名称. 默认为'image'.
        """
        layer = ipyleaflet.ImageOverlay(url = url,bounds = bounds,name = name ,**kwargs)
        self.add_layer(layer)

    
    def add_raster(self , data ,name ,zoom_to_layer = True,**kwargs):
        """在Map中添加栅格数据；

        Args:
            data (str): 栅格数据；
            name (str): 栅格数据的名称；
        """
        try:
            from localtileserver import TileClient, get_leaflet_tile_layer, examples
        except:
            raise ImportError("请下载localtileserver包")
        
        client = TileClient(data)
        layer = get_leaflet_tile_layer(client,name = name,**kwargs)
        self.add_layer(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom


    def add_zoom_slider(self, position='topright', **kwargs):
        """
        添加缩放滑块。

        Args:
            position (str, optional): 缩放滑块的位置. 默认为'topright'.
        """
        from ipywidgets import IntSlider, jslink
        from ipyleaflet import WidgetControl

        # 检查是否已经存在缩放滑块
        if not hasattr(self, '_zoom_slider_added') or not self._zoom_slider_added:
            # 创建缩放滑块
            zoom_slider = IntSlider(description='Zoom:', min=0, max=17, value=4)
            jslink((zoom_slider, 'value'), (self, 'zoom'))

            # 创建并添加滑块控件
            widget_control1 = WidgetControl(widget=zoom_slider, position=position)
            self.add(widget_control1)

            # 标记滑块已添加
            self._zoom_slider_added = True

    def add_widget(self,widget,position = 'topright'):
        """添加控件；

        Args:
            widget (Widget): 控件；
            position (str, optional): 控件的位置. 默认为'topright'.
        """
        from ipyleaflet import WidgetControl
        widget_control = WidgetControl(widget=widget, position=position)
        self.add(widget_control)

    def add_opacity_slider(self, layer_index=-1, description="Opacity", position="topright"):
        """添加透明度滑块；

        Args:
            layer_index (int, optional): 图层的索引. 默认为-1.
            description (str, optional): 滑块的描述. 默认为"Opacity".
            position (str, optional): 滑块的位置. 默认为"topright".
        """
        import ipywidgets as widgets
        layer = self.layers[layer_index]
        opacity_slider = widgets.FloatSlider(
            description=description,
            min=0,
            max=1,
            value=layer.opacity,
            style={"description_width": "initial"},
        )
        def update_opacity(change):
            layer.opacity = change["new"]

        opacity_slider.observe(update_opacity, "value")

        control = ipyleaflet.WidgetControl(widget=opacity_slider, position=position)
        self.add(control)

    def add_basemap_gui(self, basemaps=None, position="topright"):
        """向地图添加一个底图GUI

        Args:
            position (str, optional): The position of the basemap GUI. Defaults to "topright".
        """
        
        basemap_selector = widgets.Dropdown(
            options=[
                "OpenStreetMap",
                "OpenTopoMap",
                "Esri.WorldImagery",
                "Esri.NatGeoWorldMap",
            ],
            description="Basemap",
        )

        def update_basemap(change):
            self.add_basemap(change["new"])

        basemap_selector.observe(update_basemap, "value")

        control = ipyleaflet.WidgetControl(widget=basemap_selector, position=position)
        self.add(control)


    def add_toolbar(self, position='topright'):
        """添加工具栏。

        Args:
            position (str, optional): 工具栏的位置. 默认为'topright'.
        """
        padding = "0px 0px 0px 5px"  # 上、右、下、左的内边距

        # 创建工具栏按钮
        toolbar_button = widgets.ToggleButton(
            value=False,  # 初始状态为未选中
            tooltip="Toolbar",  # 鼠标悬停时显示的提示
            icon="wrench",  # 按钮图标
            layout=widgets.Layout(width="28px", height="28px", padding=padding),  # 按钮布局
        )

        # 创建关闭按钮
        close_button = widgets.ToggleButton(
            value=False,  # 初始状态为未选中
            tooltip="Close the tool",  # 鼠标悬停时显示的提示
            icon="times",  # 按钮图标
            button_style="primary",  # 按钮样式
            layout=widgets.Layout(height="28px", width="28px", padding=padding),  # 按钮布局
        )

        rows = 2  # 网格的行数
        cols = 2  # 网格的列数
        # 创建网格布局
        grid = widgets.GridspecLayout(rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px"))
        icons = ["folder-open", "map", "info", "question"]  # 按钮图标列表

        # 填充网格布局
        for i in range(rows):
            for j in range(cols):
                # 使用正确的索引
                if i * cols + j < len(icons):
                    grid[i, j] = widgets.Button(
                        description="",  # 按钮描述
                        button_style="primary",  # 按钮样式
                        icon=icons[i * cols + j],  # 按钮图标
                        layout=widgets.Layout(width="28px", padding="0px"),  # 按钮布局
                    )

        # 创建工具栏容器
        toolbar = widgets.VBox([toolbar_button])

        # 定义工具栏按钮点击事件处理函数
        def toolbar_click(change):
            if change["new"]:  # 如果按钮被选中
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]  # 显示关闭按钮和网格
                close_button.value = False  # 重置关闭按钮的值
            else:
                toolbar.children = [toolbar_button]  # 只显示工具栏按钮

        # 监听工具栏按钮的值变化
        toolbar_button.observe(toolbar_click, "value")

        # 定义关闭按钮点击事件处理函数
        def close_click(change):
            if change["new"]:  # 如果按钮被选中
                close_button.value = False  # 重置关闭按钮的值
                toolbar_button.value = False # 重置工具栏按钮的值
                toolbar.children = [toolbar_button]  # 只显示工具栏按钮

        # 监听关闭按钮的值变化
        close_button.observe(close_click, "value")

        # 创建并添加工具栏控件
        toolbar_ctrl = WidgetControl(widget=toolbar, position=position)
        self.add_control(toolbar_ctrl)

        output = widgets.Output()
        output_ctrl = WidgetControl(widget=output, position="bottomright")
        self.add_control(output_ctrl)
        def toolbar_children_click(change):
                with output:
                    output.clear_output()
                    print(f"Button clicked {change.icon}!")
        for child in grid.children:
            child.on_click(toolbar_children_click)

