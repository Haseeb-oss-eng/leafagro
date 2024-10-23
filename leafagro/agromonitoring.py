import requests
import time
from datetime import datetime
import pandas as pd

class Agromonitoring():
    def get_agromonitoring_tile(self,API_Key,PolygonId,StartDate,EndDate,data):

        """Get the tile from Agromonitoring

        Args:
            API_Key (str): Agromonitoring API Key.
            PolygonId (str): Polygon Id created in Agromonitor (Area of Interest)
            StartDate (str): Provide the date of starting from (format ex."YYYY-MM-DD")
            EndDate (str): Provide the date of till last search (format ex."YYYY-MM-DD")
            data (str): Data to retrieve from Agromonitoring. Available data ["truecolor", "falsecolor", "ndvi", "evi", "evi2", "nri", "dswi", "ndwi"] 
        """
        dates = []
        data_files = []
        allowed = ["truecolor", "falsecolor", "ndvi", "evi", "evi2", "nri", "dswi", "ndwi"]
        if data in allowed:
            start_date = int(time.mktime(time.strptime(StartDate, '%Y-%m-%d')))
            end_date = int(time.mktime(time.strptime(EndDate, '%Y-%m-%d')))

            url = f"http://api.agromonitoring.com/agro/1.0/image/search?start={start_date}&end={end_date}&polyid={PolygonId}&appid={API_Key}"
            response = requests.get(url)

                    # Check if the response is successful
            if response.status_code == 200:  
                    response_json = response.json()  # Try to parse as JSON
                    for entry in response_json:
                                # Convert UNIX timestamp to human-readable date
                        dt = entry['dt']
                        date_str = datetime.utcfromtimestamp(dt).strftime('%Y-%m-%d')

                                # Print the date
                        dates.append(date_str)

                                # add the tile URLs
                        data_files.append(entry["tile"][data])
                    df = pd.DataFrame({'Date': dates, 'URL': data_files})
                    pd.set_option('display.max_colwidth', None)
                    return df
            else:
                    print(f"Error: API request failed with status code {response.status_code}")
                    print(f"Response content: {response.content}")
        else:
            print(f"The given data is not available in Agromonitoring")
    
    def get_agromonitoring_stat(self,API_Key,PolygonId,StartDate,EndDate,data):

        """Get the Statistics from Agromonitoring

        Args:
            API_Key (str): Agromonitoring API Key.
            PolygonId (str): Polygon Id created in Agromonitoring (Area of Interest)
            StartDate (str): Provide the date of starting from (format ex."YYYY-MM-DD")
            EndDate (str): Provide the date of till last search (format ex."YYYY-MM-DD")
            data (str): Data to retrieve from Agromonitoring. Available data ["truecolor", "falsecolor", "ndvi", "evi", "evi2", "nri", "dswi", "ndwi"] 
        """