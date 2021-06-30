def retry_if_value_error(exception):
    return isinstance(exception, ValueError)


def transform_key_to(data, oldName, newName):
    new_data = {}
    for date in data:
        new_data[date] = {}
        for name in data[date]:
            if name == oldName:
                new_data[date][newName] = data[date][name]
            else:
                new_data[date][name] = data[date][name]
    return new_data
