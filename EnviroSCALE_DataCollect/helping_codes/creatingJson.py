import json
config = {'key1': 'value1', 'key2': 'value2'}
with open('config.json', 'w') as f:
    json.dump(config, f)

