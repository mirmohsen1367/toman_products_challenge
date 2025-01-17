def format_errors(errors):
    new_error = {}
    for field_name, field_errors in errors.items():
        new_error[field_name] = field_errors[0]
    return new_error
