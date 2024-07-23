def calculate_stats(data):
    stats = {}

    if not data:
        return stats

    for key in data[0].keys():
        values = [d[key] for d in data if key in d]
        if isinstance(values[0], (int, float)):
            stats[key] = {
                "min": min(values),
                "max": max(values),
                "mean": sum(values) / len(values)
            }
        elif isinstance(values[0], bool):
            true_count = sum(values)
            false_count = len(values) - true_count
            stats[key] = {
                "true_percent": (true_count / len(values)) * 100,
                "false_percent": (false_count / len(values)) * 100
            }
        elif isinstance(values[0], list):
            lengths = [len(v) for v in values]
            stats[key] = {
                "min_length": min(lengths),
                "max_length": max(lengths),
                "mean_length": sum(lengths) / len(lengths)
            }

    return stats


def display_stats(stats):
    for key, stat in stats.items():
        print(f"Stats for {key}:")
        for stat_key, stat_value in stat.items():
            print(f"  {stat_key}: {stat_value}")
