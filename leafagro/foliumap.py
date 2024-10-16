import folium


class Map(folium.Map):

    def __init__(self, center=[20,0],zoom=2, **kwargs):
        super().__init__(location=center, zoom_start=zoom, **kwargs)

    def add_raster(self, data, name="raster", **kwargs):
        """Add the Raster in map

        Args:
            data (_type_): _description_
            name (str, optional): _description_. Defaults to "raster".
            zoom_to_layer (bool, optional): _description_. Defaults to True.
        """
        try:
            from localtileserver import TileClient, get_folium_tile_layer
        except:
            raise ImportError("Please install localtileserver package")

        client = TileClient(data)
        layer = get_folium_tile_layer(client, name=name, **kwargs)
        layer.add_to(self)

        