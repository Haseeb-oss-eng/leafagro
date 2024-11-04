import ipyleaflet
from ipyleaflet import basemaps, WidgetControl,SplitMapControl
import ipywidgets as widgets
from ipywidgets import Output
from IPython.display import display, HTML

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
        if "scroll_wheel_zoom" not in kwargs:
            kwargs["scroll_wheel_zoom"] = True

        if "add_layer_control" not in kwargs:
            layer_control_flag = True
        else:
            layer_control_flag = kwargs["add_layer_control"]
        kwargs.pop("add_layer_control", None)

        super().__init__(center=center, zoom=zoom, **kwargs)
        if layer_control_flag:
            self.add_layer_control()

        self.add_toolbar()

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
        has_control = False
        for controls in self.controls:
            if isinstance(controls, ipyleaflet.LayersControl):
                has_control = True
                break
            
        if not has_control:
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

        control = ipyleaflet.WidgetControl(widget = zoom_slider, position=position)
        self.add(control)
        widgets.jslink((zoom_slider,'value'),(self,'zoom'))
    
    def add_widget(self, widget, position="topright"):
        """Adds a widget to the map.

        Args:
            widget (object): The widget to be added.
            position (str, optional): The position of the widget. Defaults to "topright".
        """
        control = ipyleaflet.WidgetControl(widget=widget, position=position)
        self.add(control)

    def add_opacity_slider(
        self, layer_index=-1, description="Opacity", position="topright"
    ):
        """Adds an opacity slider to the map.

        Args:
            layer (object): The layer to which the opacity slider is added.
            description (str, optional): The description of the opacity slider. Defaults to "Opacity".
            position (str, optional): The position of the opacity slider. Defaults to "topright".
        """
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
        """Adds a basemap GUI to the map.

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

    def add_toolbar(self, position="topright"):
        """Adds a toolbar to the map.

        Args:
            position (str, optional): The position of the toolbar. Defaults to "topright".
        """

        padding = "0px 0px 0px 5px"  # upper, right, bottom, left

        toolbar_button = widgets.ToggleButton(
            value=False,
            tooltip="Toolbar",
            icon="wrench",
            layout=widgets.Layout(width="28px", height="28px", padding=padding),
        )

        close_button = widgets.ToggleButton(
            value=False,
            tooltip="Close the tool",
            icon="times",
            button_style="primary",
            layout=widgets.Layout(height="28px", width="28px", padding=padding),
        )

        toolbar = widgets.VBox([toolbar_button])

        def close_click(change):
            if change["new"]:
                toolbar_button.close()
                close_button.close()
                toolbar.close()

        close_button.observe(close_click, "value")

        rows = 1
        cols = 1
        grid = widgets.GridspecLayout(
            rows, cols, grid_gap="0px", layout=widgets.Layout(width="65px")
        )

        # icons = ["folder-open", "map", "info", "question"]
        icons = ["basemap"]

        for i in range(rows):
            for j in range(cols):
                grid[i, j] = widgets.Button(
                    description="",
                    button_style="primary",
                    icon=icons[i * rows + j],
                    layout=widgets.Layout(width="28px", padding="0px"),
                )

        def toolbar_click(change):
            if change["new"]:
                toolbar.children = [widgets.HBox([close_button, toolbar_button]), grid]
            else:
                toolbar.children = [toolbar_button]

        toolbar_button.observe(toolbar_click, "value")
        toolbar_ctrl = WidgetControl(widget=toolbar, position="topright")
        self.add(toolbar_ctrl)

        output = widgets.Output()
        output_control = WidgetControl(widget=output, position="bottomright")
        self.add(output_control)

        def toolbar_callback(change):
            if change.icon == "basemap":
                with output:
                    output.clear_output()
                    self.add_basemap_gui()
            elif change.icon == "map":
                with output:
                    output.clear_output()
                    print(f"You can add a layer")
            else:
                with output:
                    output.clear_output()
                    print(f"Icon: {change.icon}")

        for tool in grid.children:
            tool.on_click(toolbar_callback)

    def add_split_map(self, left_layer, right_layer, **kwargs):
        """Adds a split map to the current map.

        Args:
            left_layer (object): The left layer of the split map.
            right_layer (object): The right layer of the split map.
        """

        control = SplitMapControl(
            left_layer=left_layer,
            right_layer=right_layer,
        )
        self.add(control)

    def show_agromonitoring_tile(self,API_key, polygonId, startDate, endDate, data,table=False):

        """Add the Agromonitoring tile layer in map

        Args:
            API_key (str): Provide the Agromonitoring API Key.
            polygonId (str): Provide the polygon ID (study area) from Agromonitoring.
            startDate (str): Date format "YYYY-MM-DD" (ex. "2018-01-01").
            endDate (str): Date format "YYYY-MM-DD" (ex. "2018-02-01").
            data (str): Data to retrieve from Agromonitoring. Available Data ['truecolor', 'falsecolor', 'ndvi', 'evi', 'evi2', 'ndwi', 'nri', 'dswi'].
            table (bool): Display the tables of Data available with data (default: False).
        """
        from  leafagro.agromonitoring import Agromonitoring as ag

        # Retrieve the tile data from agromonitoring.py
        df = ag.get_agromonitoring_tile(API_key, polygonId, startDate, endDate, data)

        if df is None:
            print("No data to display.")
            return

        # Display the table if requested
        if table:
            print(df)
        else:
        # Add all tiles to the map
            for index, row in df.iterrows():
                tile_url = row['URL']
                date = row['Date']
                self.add_layer_tile(tile_url, name=f"{date} {data}")
    
    def show_agromonitoring_stats(self,API_Key, polygonId, startDate, endDate, data, display=False):
        """Display the Summary Statistics of Table

        Args:
            API_key (str): Provide the Agromonitoring API Key.
            polygonId (str): Provide the polygon ID (study area) from Agromonitoring.
            startDate (str): Date format "YYYY-MM-DD" (ex. "2018-01-01").
            endDate (str): Date format "YYYY-MM-DD" (ex. "2018-02-01").
            data (str): Data to retrieve from Agromonitoring. Available Data ['truecolor', 'falsecolor', 'ndvi', 'evi', 'evi2', 'ndwi', 'nri', 'dswi'].
            display (bool): True to display the stats on map. (default: False)
        """
        from leafagro.agromonitoring import Agromonitoring as ag
        
        stats_df = ag.get_agromonitoring_stat(API_Key,polygonId, startDate, endDate, data)
          
        if display:
            for index, stat in stats_df.iterrows():
                self.display_stats(stat['URL'], stat['Date'])
        else:
            if stats_df is not None:
                    print(stats_df)
            else:
                    print(f"The given data or Polygon ID is Wrong is not available in Agromonitoring") 


    
    
    def display_stats(self, statsUrl, date):
        """Display Summary Statistics of Polygon

        Args:
            statsUrl (str): Input Stats Url from agromonitoring stats.
            date (str): Date of the stats.
        """
        import requests
        import time
        import pandas as pd
        from urllib.parse import urlparse, parse_qs
  
        try:
        # Fetch statistics data from the given URL
            data = requests.get(statsUrl)
            data_dict = data.json()
            stats_df = pd.DataFrame([data_dict], index=[date], columns=data_dict.keys())

            # Parse the stats URL to extract polygon ID and API key
            parsed_url = urlparse(statsUrl)
            path_segments = parsed_url.path.split('/')
            polygon_id = path_segments[-1]  # Extract polygon ID
            query_params = parse_qs(parsed_url.query)
            api_key = query_params.get('appid', [None])[0]  # Extract API key

            # Define polygons URL using the API key
            polygons_url = f"http://api.agromonitoring.com/agro/1.0/polygons?appid={api_key}"
            response = requests.get(polygons_url)

            if response.status_code == 200:
                metadata = response.json()
                coordinates = None
                if isinstance(metadata, list):
                    for polygons in metadata:
                        Id = polygons.get('id')
                        if Id == polygon_id:
                            coordinates = polygons['geo_json']  # Extract coordinates
                            break

                # Add the polygon's geojson to the map
                if coordinates:
                    self.add_geojson(coordinates)
                else:
                    print(f"No matching polygon found for ID: {polygon_id}")

                # If statistics data is available, display it
                if stats_df is not None:
                    # Convert stats_df to HTML with some inline styling
                    html_content = stats_df.to_html(classes='styled-table')
                    html_styled = f"""
                    <style>
                    .styled-table {{
                        font-size: 18px;
                        color: green;
                    }}
                    </style>
                    {html_content}
                    """
                    
                    # Create an output widget and add it to the map
                    widget = Output(layout={'border': '1px solid white'})
                    output_widget = WidgetControl(widget=widget, position='bottomright')
                    self.add(output_widget)
                    with widget:
                        widget.clear_output()
                        display(HTML(html_styled))
                else:
                    print("No statistics data available.")
            else:
                print(f"Error fetching polygons: {response.status_code}")

        except requests.exceptions.RequestException as e:
            print(f"An error occurred while making the API request: {e}")