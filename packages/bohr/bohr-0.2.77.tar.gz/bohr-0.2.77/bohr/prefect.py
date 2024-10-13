import os
import psycopg2
import pandas as pd
from psycopg2 import extras
import json
from pandas.core.common import flatten
import re

class Prefect(object):
    def __init__(self):
        """
        Initializes the DataQuality object with a DataFrame, a flow identifier, and a path to a configuration file.

        Args:
            df (pd.DataFrame): The DataFrame to assess for quality.
            flow (str): An identifier used to select the appropriate section of the configuration.
            config_path (str): The filesystem path to a JSON configuration file.
        """
        pass

################# COMPLETENESS #################

    @staticmethod
    def json_to_markdown(file_path):
        """
        Read a JSON file from the specified path and return its contents formatted as a Markdown string.

        Args:
        file_path (str): The path to the JSON file.

        Returns:
        str: The contents of the JSON file formatted as Markdown.
        """
        pattern = r"\/([^\/]+)\.json"
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)  # Load JSON data from the file
                match = re.search(pattern, file_path)
                df = pd.DataFrame.from_dict(data[match.group(1)])
                del(df['data_quality'])
                df=df.drop_duplicates()
                df= df.transpose()
                df.columns = ['value']
                df.index.name = 'key'
                print(df.to_markdown(index=True,tablefmt='fancy_grid'))
                return df.to_markdown(index=True,tablefmt='github')
        except Exception as e:
            print(f"An error occurred while reading the JSON file: {e}")
            return None
