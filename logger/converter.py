


def convert_to_string(data):
    content = data['Body'].read().decode("utf-8")
    return content