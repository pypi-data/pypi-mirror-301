def get_label_names(num_labels: int, file: str = None) -> list:
    """Return label names in a list. Read from CSV file, if provided."""
    import csv

    from sonusai import SonusAIError

    if file is None:
        return [f'Class {val + 1}' for val in range(num_labels)]

    label_names = [''] * num_labels
    with open(file) as f:
        reader = csv.DictReader(f)
        if 'index' not in reader.fieldnames or 'display_name' not in reader.fieldnames:
            raise SonusAIError(f'Missing required fields in labels CSV.')

        for row in reader:
            index = int(row['index']) - 1
            if index >= num_labels:
                raise SonusAIError(f'The number of given label names does not match the number of labels.')
            label_names[index] = row['display_name']

    return label_names
