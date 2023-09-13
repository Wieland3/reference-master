"""
Constants used for the reference master
"""

import os

# PROJECT ROOT
PATH_TO_PROJECT_ROOT =  os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# SONG PATHS
PATH_TO_SONGS = os.path.join(PATH_TO_PROJECT_ROOT,'songs')
PATH_TO_RAW_SONGS = os.path.join(PATH_TO_SONGS, 'raw/')
PATH_TO_REFERENCE_SONGS = os.path.join(PATH_TO_SONGS, 'references/')
PATH_TO_MASTERED_SONGS = os.path.join(PATH_TO_SONGS, 'mastered/')

PATH_TO_WEBAPP_UPLOADS = '../webapp/uploads'

# Duration of the chorus in seconds
DURATION = 10

# Equalizer
NUM_ITERATIONS = 1 # Num Iterations used for eq optimization
HP_FREQ = 20 # High Pass Filter Frequency
LOOKBACK = 10 # Smoothing for Song Distance
