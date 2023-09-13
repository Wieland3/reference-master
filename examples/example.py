"""
File contains code on how to reference master a song using python
"""

from reference_master.mastering.master import master

# call the master function with the raw audio file as first argument and the reference audio file as second argument
master("raw_0.wav", "11 - Circle With Me.mp3")

# If you do not want to match the loudness but chose a specific loudness you can do so by passing the loudness as a third argument
master("raw_0.wav", "11 - Circle With Me.mp3", -7.0)