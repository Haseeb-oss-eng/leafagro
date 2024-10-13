import ipyleaflet
from ipyleaflet import basemaps, widgetControl, SplitMapControl
import ipywidgets as widgets

class Map(ipyleaflet.Map):
    """This is the map class that inherits from ipyleaflet.Map.

    Args:
        ipyleaflet (Map): The ipyleaflet.Map class.
    """

    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        """initializing the Map

        Args:
            center (list, optional): set the center . Defaults to [20, 0].
            zoom (int, optional): set the zoom. Defaults to 2.
        """
        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_layer_tile(self, url, name, **kwargs):
        layer = ipyleaflet.TileLayer(url=url, name=name, **kwargs)
        self.add(layer)

    def add_basemap(self, name):
        """
        Adds a basemap to the current map.

        Args:
            name (str or object): The name of the basemap as a string, or an object representing the basemap.

        Raises:
            TypeError: If the name is neither a string nor an object representing a basemap.

        Returns:
            None
        """
        if isinstance(name, str):
            url = eval(f"basemaps.{name}").build_url()
            self.add_layer_tile(url, name)
        else:
            self.add(name)

    def add_layer_control(self, position='topright'):
        """Adds a layers Control in the map.

        Args:
            position (str, optional): The position the layer control. Defaults to 'topright'.
        """
        self.add_control(ipyleaflet.LayersControl(position=position))

    def add_geojson(self,data,name='geojson', **kwargs):
        """Adds a GeoJSON layer to the map.

        Args:
            data (str | dict): The GeoJSON data as a string or a dictionary.
            name (str, optional): The name of the layer. Defaults to "geojson".
        """

        import json

        if isinstance(data,str):
            with open(data) as f:
                data = json.load(f)
        
        if 'style' not in kwargs:
            kwargs['style'] = {'color':'blue', 'weight': 1, 'fillOpacity':0}
        
        if 'hover_style' not in kwargs:
            kwargs['hover_style'] = {'fillColor':'blue','fillOpacity': 0.5}

        layer = ipyleaflet.GeoJSON(data=data,name=name, **kwargs)

        self.add(layer)
    
    def add_shp(self, data, name='Shapefile', **kwargs):
        """
        Adds a shapefile to the current map.

        Args:
            data (str or dict): The path to the shapefile as a string, or a dictionary representing the shapefile.
            name (str, optional): The name of the layer. Defaults to "shp".
            **kwargs: Arbitrary keyword arguments.

        Raises:
            TypeError: If the data is neither a string nor a dictionary representing a shapefile.

        Returns:
            None
        """

        import shapefile
        import json

        if isinstance(data, str):
            with shapefile.Reader(data) as shp:
                data = shp.__geo_interface__

        self.add_geojson(data, name, **kwargs)
    
    def add_imageOverlay(self, url, bounds, name="image", **kwargs):
        """Overlays the image on the map

        Args:
            urls (str): The URL of image in String
            bounds (list): The bounds of the image to Overlay on map
            name (str, Optional): The name of the overlaying image, Default is "image".  
        """
        layer = ipyleaflet.ImageOverlay(url=url, bounds=bounds, name=name, **kwargs)
        self.add(layer)
    
    def add_raster(self, data, name="raster", zoom_to_layer=True, **kwargs):
        """Add the Raster in map

        Args:
            data (_type_): _description_
            name (str, optional): _description_. Defaults to "raster".
            zoom_to_layer (bool, optional): _description_. Defaults to True.
        """
        try:
            from localtileserver import TileClient, get_leaflet_tile_layer
        except:
            raise ImportError("Please install localtileserver package")

        client = TileClient(data)
        layer = get_leaflet_tile_layer(client, name=name, **kwargs)
        self.add(layer)

        if zoom_to_layer:
            self.center = client.center()
            self.zoom = client.default_zoom
    
    def add_zoom_slider(self, description= "Zoom level", min=0, max=15, value=7, position="topright", **kwargs):

        """Add Slider-level bar in map

        Args:
            position (str, optional): The position of zoom slider. Default position: topright.
        """
        zoom_slider = widgets.IntSlider(description = description, min=min, max=max)

        control = ipyleaflet.widgetControl(widget = zoom_slider, position=position)
        self.add(control)
        widgets.jslink((zoom_slider,'value'),(self,'zoom'))