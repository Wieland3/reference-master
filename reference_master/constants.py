"""
Constants used for the reference master
"""

import os
import yaml

# Smoothing for Song Distance
LOOKBACK = 10

# PROJECT ROOT
PATH_TO_PROJECT_ROOT =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SONG PATHS
PATH_TO_SONGS = os.path.join(PATH_TO_PROJECT_ROOT,'songs')
PATH_TO_RAW_SONGS = os.path.join(PATH_TO_SONGS, 'raw/')
PATH_TO_REFERENCE_SONGS = os.path.join(PATH_TO_SONGS, 'references/')
PATH_TO_MASTERED_SONGS = os.path.join(PATH_TO_SONGS, 'mastered/')

PATH_TO_WEBAPP_UPLOADS = '../webapp/uploads'

# Path to yaml user settings
PATH_TO_SETTINGS_YAML = os.path.join(PATH_TO_PROJECT_ROOT, "settings.yaml")

# Load settings from the YAML file
with open(PATH_TO_SETTINGS_YAML, 'r') as settings_file:
    settings = yaml.safe_load(settings_file)

NUM_ITERATIONS = settings['NUM_ITERATIONS']
HP_FREQ = settings['HP_FREQ']
DURATION = settings['DURATION']
