import os
import json

def write_json(path: str, verbose: bool = False, **kwargs):
    if os.path.exists(path):
        with open(path, 'r+') as jsonfile:
            try:
                data = json.load(jsonfile)
            except json.decoder.JSONDecodeError:
                data = {}

            # Check if the same values already exist in the data
            for existing_name, existing_values in data.items():
                if existing_values == kwargs:
                    print("User with the same values already exists.")
                    return

            # Find the next available element name
            new_element_name = find_next_element_name(data)

            # Remove the "values" key if it exists
            if "values" in kwargs:
                kwargs = kwargs["values"]

            data[new_element_name] = kwargs
            jsonfile.seek(0)
            json.dump(data, jsonfile, indent=2)
            jsonfile.truncate()
    else:
        with open(path, 'w') as jsonfile:
            # Remove the "values" key if it exists
            if "values" in kwargs:
                kwargs = kwargs["values"]

            data = {find_next_element_name({}): kwargs}
            json.dump(data, jsonfile, indent=2)

    if verbose:
        print("JSON file created and written to")



def find_next_element_name(data):
    element_prefix = "user"
    max_index = 0

    for key in data.keys():
        if key.startswith(element_prefix):
            index = int(key[len(element_prefix):])
            max_index = max(max_index, index)

    return f"{element_prefix}{max_index + 1}"