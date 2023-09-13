# reference-master

Automated Music Mastering through an Optimization-Based Approach

## Installation

```python
pip install -r requirements.txt
```

## Usage

Put the Song you want to master in the "songs/raw" folder 

Put your reference Song in the "songs/references" folder

```python
from reference_master.mastering.master import master
```
Master and use loudness of reference Track 

```python
master("your-track.wav", "Bohemian Rhapsody.mp3")
```
Alternatively, you can manually specify the target loudness of the song to be mastered

```python
master("your-track.wav", "Bohemian Rhapsody.mp3", -7.0)
```
The mastered song will be automatically saved in the "songs/mastered" folder. 

Depending on how many epochs are set in the settings.yaml the process can take a couple of minutes.
You can change the number of epochs and other parameters for the mastering in the settings.yaml file.

During the mastering process the current distance between the songs is printed to the console. 
A distance somewhere close to 1 is a hint that the mastering was successful.
