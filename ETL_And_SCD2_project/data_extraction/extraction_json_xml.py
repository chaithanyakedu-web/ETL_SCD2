import json
import pandas as pd
from parsers import parse_json_file,parse_xml_file
from parsers import *

def verify_file_extension_and_read_data(file_name):
    if file_name.endswith('.json'):
        j = parse_json_file(file_name)#parsing the json data
        #print(type(j))
        df = pd.DataFrame(j)
        #print(df.columns)-->give the list of columnsnames to readit oneby one use columns[0]
        return df

    elif file_name.endswith('.xml'):
        x = parse_xml_file(file_name)#parsing the xml data
        return x
    else:
        raise ValueError('File extension must be .json or .xml')

