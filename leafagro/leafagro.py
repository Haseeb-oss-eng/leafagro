"""Main module."""
import ipyleaflet
from ipyleaflet import basemap

class Map(ipyleaflet.Map):
    def __init__(self, center=[20, 0], zoom=2, **kwargs):
        super().__init__(center=center, zoom=zoom, **kwargs)

    def add_tile_layer(self,name,url,**kwargs):
        layer = ipyleaflet.TileLayer(url=url,name=name,**kwargs)
        self.add(layer)

    def add_basemap(self, name):
        if isinstance(name,str):
            url = eval(f"basemap.{name}").build_url()
            self.add_tile_layer(url,name)
        else:
            self.add(name)
