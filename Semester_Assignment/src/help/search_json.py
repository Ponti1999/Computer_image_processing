import json

def search_items_recursive(data, item_conditions):
    results = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if key in item_conditions and value == item_conditions[key]:
                results[key] = value
            elif isinstance(value, (dict, list)):
                nested_results = search_items_recursive(value, item_conditions)
                if nested_results:
                    results.update(nested_results)
    elif isinstance(data, list):
        for item_data in data:
            nested_results = search_items_recursive(item_data, item_conditions)
            if nested_results:
                results.update(nested_results)

    return results

def search_item_in_users(path:str, item_conditions):
    with open(path, 'r') as jsonfile:
        data = json.load(jsonfile)
        return search_items_recursive(data, item_conditions)


def get_level_length(config_path):
    with open(config_path, 'r') as jsonfile:
        data = json.load(jsonfile)
        level_lengths = [(level, len(level)) for level in data.values()]
        if level_lengths:
            max_length = max(level_lengths, key=lambda x: x[1])
            return max_length[1], max_length[0]
        else:
            return 0, None
