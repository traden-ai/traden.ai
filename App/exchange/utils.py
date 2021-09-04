from App.utils import *


def ask_model(instances):

    while True:
        instances = ask_model_instances(instances)

        if (len(instances) > 1):
            print("Please choose a single model")
            continue

        return instances


def render_position(position):

    price_evo = (position.current_price - position.average_open) / \
        position.average_open * 100
    #FIXME eq?
    capital_evo = (position.capital_value - position.capital_invested) / \
        position.capital_invested * 100

    res = f"\n\tTicker {position.ticker}\n"
    res += f"\tPrice evolution: {position.average_open} >> {position.current_price} ({price_evo:.2f}%)\n"
    res += f"\tCapital evolution: {position.capital_invested} >> {position.capital_value} ({capital_evo:.2f}%)\n"
    res += f"\tHolding {position.units} units\n"
    return res


def render_ledger(ledger):
    res = "\nOpen Positions:"
    for pos in ledger.positions:
        res += render_position(pos)

    cap_total = ledger.capital_allocated + ledger.capital_available
    allocated_share = ledger.capital_allocated / cap_total * 100
    available_share = ledger.capital_available / cap_total * 100

    res += f"\nIn use Capital: {ledger.capital_allocated} / {cap_total} ({allocated_share:.2f}%)\n"
    res += f"Available Capital: {ledger.capital_available} / {cap_total} ({available_share:.2f}%)\n"
    # FIXME get profit in % as well
    res += f"Total profit: {ledger.profit}"
    return res


def render_model(name, model):
    res = f"Model {name}"
    res += render_ledger(model.model_ledger)
    res += f"\n\nModel ledger share: {model.ledger_representation}%"
    return res
