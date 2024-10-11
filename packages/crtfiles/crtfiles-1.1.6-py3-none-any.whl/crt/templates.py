import json
import pkg_resources


def get_templates(name: str):
    try:
        template_path = pkg_resources.resource_filename(
            __name__, 'data/templates.json')
        with open(template_path, 'r', encoding='utf-8') as json_file:
            temp_file: dict = json.load(json_file)
        if (name in temp_file):
            return temp_file.get(name)
        return None
    except FileNotFoundError:
        print("JSON file not found.")
        return None
    except json.JSONDecodeError:
        print("Error reading JSON file.")
        return None
