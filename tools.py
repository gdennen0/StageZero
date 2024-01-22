import librosa
import soundfile as sf
from view import DialogWindow
import numpy as np

from scipy.signal import butter, lfilter
    
def estimate_bpm(song_object):
    # Load the song using the SongModel
    song_name = song_object.name
    song_path = song_object.path
    song_data, sample_rate = librosa.load(song_path)

    desired_frame_rate = 30  # for example, 100 frames per second
    hop_length = int(sample_rate / desired_frame_rate)

    # Use librosa to estimate the BPM
    tempo, beats = librosa.beat.beat_track(y=song_data, sr=sample_rate, hop_length=hop_length)

    print(f"[TOOLS][estimate_bpm] song name: {song_name}, sample rate {sample_rate}, tempo {tempo}")
    return tempo, beats

def detect_onsets(song_object=None, song_data=None, sample_rate=None):
    if song_object is not None:
        if song_data is None:
            song_data = song_object.original_song_data

        if sample_rate is None:
            sample_rate = song_object.original_sample_rate
    
    desired_frame_rate = 30  # for example, 100 frames per second
    hop_length = int(sample_rate / desired_frame_rate)

    onsets = librosa.onset.onset_detect(y=song_data, sr=sample_rate, hop_length=hop_length, units='frames')
    print(f"Onsets: {onsets}")
    return onsets

def apply_lo_pass_filter(song_object):
    path = song_object.path
    song_data, sample_rate = librosa.load(path)
    sample_rate = song_object.original_sample_rate
    cutoff = 500

    # Apply the low pass filter
    b, a = butter_lowpass(cutoff, sample_rate, order=5)
    filtered_signal = lfilter(b, a, song_data)
    return filtered_signal

def butter_lowpass(cutoff, sample_rate, order=5):
    nyq = 0.5 * sample_rate
    normal_cutoff = cutoff / nyq
    # Create a low pass butterworth filter
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    return b, a


def create_frames_array(frame_qty):  # create tick array
        print(f"Creating {frame_qty} frame array")
        return np.arange(frame_qty)


