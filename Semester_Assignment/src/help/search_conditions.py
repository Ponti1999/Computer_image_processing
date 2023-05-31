def create_search_conditions(args, exc):
    search_conditions = {}

    for attr, value in vars(args).items():
        if value is not None and attr not in exc:
            search_conditions[attr] = value

    return search_conditions
