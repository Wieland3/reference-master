# In this file constanst for the projects are defined

# Database Settings
LOUDNESS_NORM = -18.0 # Loudness normalization for reference tracks

PATH_TO_WEBAPP_UPLOADS = '../frontend/uploads'
PATH_TO_MASTERED_EMBEDDINGS = '../mastered_embeddings'

# Duration of the chorus in seconds
DURATION = 5
# Target Loudness for Mastering
LOUDNESS = -7.0

# Equalizer
NUM_ITERATIONS = 100 # Num Iterations used for eq optimization
HP_FREQ = 20 # High Pass Filter Frequency
LOOKBACK = 10 # Smoothing for Song Distance

# Compressor
REDUCE = 1 # Reduce the loudness of the track by this db



