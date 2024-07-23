import csv
import json
import xml.etree.ElementTree as ET
import yaml


def load_csv(file_path):
    with open(file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        return [row for row in reader]


def save_csv(data, file_path):
    if not data:
        return

    with open(file_path, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)


def load_json(file_path):
    with open(file_path, mode='r') as file:
        return json.load(file)


def save_json(data, file_path):
    with open(file_path, mode='w') as file:
        json.dump(data, file, indent=4)


def load_xml(file_path):
    tree = ET.parse(file_path)
    root = tree.getroot()
    return [{child.tag: child.text for child in elem} for elem in root]


def save_xml(data, file_path):
    root = ET.Element("root")
    for item in data:
        elem = ET.Element("item")
        for key, val in item.items():
            child = ET.Element(key)
            child.text = str(val)
            elem.append(child)
        root.append(elem)
    tree = ET.ElementTree(root)
    tree.write(file_path)


def load_yaml(file_path):
    with open(file_path, mode='r') as file:
        return yaml.safe_load(file)


def save_yaml(data, file_path):
    with open(file_path, mode='w') as file:
        yaml.dump(data, file)
