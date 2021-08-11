from datetime import datetime


def chunks(lst, n):
    """Yield successive n-sized chunks from lst."""
    for i in range(0, len(lst), n):
        yield lst[i:i + n]


def get_current_date():
    return datetime.today().strftime('%Y-%m-%d')
