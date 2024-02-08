import json

def process_json_data(file):
    """
    Read JSON data from file, remove double-escaping, and load the JSON data.
    """
    json_data = file.read()
    # Remove double-escaping
    json_data = json_data.replace(b'\\"', b'"')
    try:
        data = json.loads(json_data)
        processed_data = []
        for entry in data:
            # Lowercase the table value if it is in the allowed tables
            # merges i.e. Airfield and airfield
            if entry.get('table') in ['Aircraft', 'Airfield', 'Flight', 'Pilot']:
                entry['table'] = entry['table'].lower()

            # Update each entry with its 'meta' field. Normalize the db
            entry.update(entry.get('meta', {}))

            # Drop unnecessary fields
            entry.pop('user_id', None)
            entry.pop('platform', None)
            entry.pop('_modified', None)

            # Filter out rows that aren't specified below
            if entry.get('table') in ['aircraft', 'airfield', 'flight', 'pilot']:
                processed_data.append(entry)

        return processed_data

    except json.JSONDecodeError as e:
        print(f"Error decoding JSON: {e}")
        return None
