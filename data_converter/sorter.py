def sort_data(data, key):
    return sorted(data, key=lambda x: x.get(key))

def sort_data_multiple(data, keys):
    from operator import itemgetter
    return sorted(data, key=itemgetter(*keys))