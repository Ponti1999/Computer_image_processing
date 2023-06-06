import json

def search_items_recursive(data, item_conditions):
    results = {}

    if isinstance(data, dict):
        for key, value in data.items():
            if key in item_conditions and value == item_conditions[key]:
                results[key] = value
            elif isinstance(value, dict):
                nested_results = search_items_recursive(value, item_conditions)
                if nested_results:
                    results.update(nested_results)
            elif isinstance(value, list) and key in item_conditions and isinstance(item_conditions[key], list):
                # Check for a matching list value by comparing individual elements
                if len(value) == len(item_conditions[key]) and all(x == y for x, y in zip(value, item_conditions[key])):
                    results[key] = value
            elif key == "color" and "color" in item_conditions and isinstance(value, (list, tuple)) and isinstance(item_conditions["color"], (list, tuple)):
                # Check for a matching color value by comparing individual elements
                if len(value) == len(item_conditions["color"]) and all(x == y for x, y in zip(value, item_conditions["color"])):
                    results[key] = value
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


def create_search_conditions(args, exc):
    search_conditions = {}

    for attr, value in vars(args).items():
        if value is not None and attr not in exc:
            if attr == "color" and isinstance(value, str):
                search_conditions[attr] = [int(c) for c in value.split(",")]
            else:
                search_conditions[attr] = value

    return search_conditions


def get_level_length(config_path):
    with open(config_path, 'r') as jsonfile:
        data = json.load(jsonfile)
        level_lengths = [(level, len(level)) for level in data.values()]
        if level_lengths:
            max_length = max(level_lengths, key=lambda x: x[1])
            return max_length[1], max_length[0]
        else:
            return 0, None


def list_users_values(path:str, user:str=None, verbose:bool=False):
    with open(path, 'r') as jsonfile:
        data = json.load(jsonfile)
        user_keys = list(data.keys())

        if user is None:
            return user_keys, None

        user_data = data.get(user)
        if user_data is None:
            if verbose:
                print(f"Invalid user: {user}")
            return None, None

        return user_keys, user_data