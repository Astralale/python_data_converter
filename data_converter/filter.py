def filter_data(data, criteria):
    filtered_data = []
    for item in data:
        match = True
        for key, value in criteria.items():
            if key not in item or item[key] != value:
                match = False
                break
        if match:
            filtered_data.append(item)
    return filtered_data

def advanced_filter_data(data, criteria):
    filtered_data = []
    for item in data:
        match = True
        for key, condition in criteria.items():
            if key not in item:
                match = False
                break
            if isinstance(condition, tuple) and len(condition) == 2:
                op, val = condition
                if op == "contains" and val not in item[key]:
                    match = False
                    break
                elif op == "startswith" and not item[key].startswith(val):
                    match = False
                    break
                elif op == "endswith" and not item[key].endswith(val):
                    match = False
                    break
            elif item[key] != condition:
                match = False
                break
        if match:
            filtered_data.append(item)
    return filtered_data
