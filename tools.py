import librosa

    
def estimate_bpm(song_object):
    # Load the song using the SongModel
    song_name = song_object.name
    song_path = song_object.path
    song_data, sample_rate = librosa.load(song_path)

    # Use librosa to estimate the BPM
    tempo, _ = librosa.beat.beat_track(y=song_data, sr=sample_rate)
    
    print(f"[TOOLS][estimate_bpm] song name: {song_name}, sample rate {sample_rate}, tempo {tempo}")
    return tempo