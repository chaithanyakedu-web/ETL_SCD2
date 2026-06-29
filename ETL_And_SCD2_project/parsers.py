"""parsers.py - parse json and xml into list[dict]"""
import json
import xml.etree.ElementTree as ET

def parse_json_file(path):
    with open(path, 'r', encoding='utf-8') as x:
        j = json.load(x)
    # assume array of objects
    return j

def parse_xml_file(path):
    tree = ET.parse(path)
    root = tree.getroot()
    records = []
    for org in root.findall('.//Organization'):
        r = {}
        for child in org:
            r[child.tag] = child.text
        records.append(r)
    return records
