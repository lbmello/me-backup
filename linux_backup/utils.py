
def process_config_lines(config_file):
    """Method used to process config file columns."""

    config_lines = config_file.readlines()

    config_values = dict()

    for line in config_lines:
        line = line.replace('\n', '')

        key, value = line.split(' = ')

        config_values[key] = value

    return config_values