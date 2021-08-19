from Models.models.daily_data_related.action import Action


def divide_results(results):
    buy_results = []
    sell_results = []
    for result in results:
        if result["Action"] == Action.BUY:
            buy_results.append(result)
        elif result["Action"] == Action.SELL:
            sell_results.append(result)
    return buy_results, sell_results


def normalize_to_sum(results, percentage):
    intensity_sum = sum(float(a["Intensity"]) for a in results)
    new_results = []
    for result in results:
        result["Intensity"] = (result["Intensity"] * percentage) / intensity_sum
        new_results.append(result)
    return new_results
