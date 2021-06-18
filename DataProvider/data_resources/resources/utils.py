def retry_if_value_error(exception):
    return isinstance(exception, ValueError)
