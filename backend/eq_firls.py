from scipy.signal import butter, sosfilt
import numpy as np
import librosa
from backend import audio_utils
from backend import spectrum
import matplotlib.pyplot as plt
import scipy.signal
from scipy.signal import firls


# Load audio
raw, sr_raw = audio_utils.load_audio_file('../tracks/edited/raw.wav')
raw, _ = audio_utils.preprocess_audio(raw, sr_raw)
ref, sr_ref = audio_utils.load_audio_file('../tracks/edited/reference.wav')
ref, _ = audio_utils.preprocess_audio(ref, sr_ref)

spec_raw, freq = spectrum.create_spectrum(raw, sr_raw)
spec_ref, freq = spectrum.create_spectrum(ref, sr_ref)

# Compute the difference between the two spectra.
diff_spectrum = spec_ref - spec_raw

# Specify the desired filter order (number of taps).
filter_order = 1


# Design an FIR filter using firls that matches the difference spectrum.
filter_taps = scipy.signal.firls(3, [0,0.25,0.5,1], [0,20,1,0], fs=sr_raw)



# Apply the filter to the target signal using convolution.
raw = scipy.signal.convolve(raw, filter_taps, mode="same")
spec_raw, freq = spectrum.create_spectrum(raw, sr_raw)

plt.plot(freq, spec_raw, label="raw")
plt.plot(freq, spec_ref, label="ref")
plt.xscale('log')
plt.grid(True, which="both", ls="-", color='0.65')
plt.legend()
plt.show()