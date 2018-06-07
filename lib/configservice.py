import json

with open('config.json') as configfile:
    info = json.load(configfile)

raw_zip_file_location = info.get('RAW_DATA_ZIP')
state = info.get('STATE')
variables = info.get('VARIABLES')
historic_range = info.get('HISTORIC_RANGE')
sample_window = info.get('SAMPLE_WINDOW')