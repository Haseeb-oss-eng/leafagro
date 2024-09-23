"""This is utils module that contains utility functions for leafagro
"""

def csv_df(csv_file):
    """Convert the csv file to dataframe

    Args:
        csv_file: The CSV file

    """
    import pandas as pd

    return pd.read(csv_file)