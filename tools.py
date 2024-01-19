import librosa

    
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

def detect_onsets(song_object):
    song_name = song_object.name
    song_path = song_object.path
    song_data, sample_rate = librosa.load(song_path)


    desired_frame_rate = 30  # for example, 100 frames per second
    hop_length = int(sample_rate / desired_frame_rate)

    onsets = librosa.onset.onset_detect(y=song_data, sr=sample_rate, hop_length=hop_length, units='frames')
    print(f"Onsets: {onsets}")
    return onsets