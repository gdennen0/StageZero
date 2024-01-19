import numpy as np
import matplotlib.pyplot as plt
import librosa

class GraphWindowController:
    def __init__(self, main_controller):
        self.main_controller = main_controller
        self.stack = main_controller.model.stack
        self.model = main_controller.model
        self.view = main_controller.view
        self.init_connections()
        self.init_status()

    def init_status(self):
        self.status = {
            "stft_linear_spectrogram" : False, 
            "log_frequency_axis" : False, 
            "mel_spectrogram": False,
            }

    def init_connections(self):
        self.view.graphs_window.graph_selector.currentIndexChanged.connect(self.on_stack_widget_selected)

    def on_stack_widget_selected(self, index):
        self.view.graphs_window.open_graph(index)
        graph_name = self.view.graphs_window.graph_selector.itemText(index)
        print(f"index opening graph stack {graph_name} at index {index}")
        if graph_name == "stft_linear_spectrogram" and not self.status["stft_linear_spectrogram"]:
            self.status["stft_linear_spectrogram"] = True
            song_object = self.model.loaded_song
            figure = self.stft_linear_spectrogram(song_object)
            self.view.graphs_window.stft_linear_spectrogram.plot(figure)
        
        if graph_name == "log_frequency_axis" and not self.status["log_frequency_axis"]:
            self.status["log_frequency_axis"] = True
            song_object = self.model.loaded_song
            figure = self.log_frequency_axis(song_object)
            self.view.graphs_window.log_frequency_axis.plot(figure)
        
        if graph_name == "mel_spectrogram" and not self.status["mel_spectrogram"]:
            self.status["mel_spectrogram"] = True
            song_object = self.model.loaded_song
            figure = self.mel_spectrogram(song_object)
            self.view.graphs_window.mel_spectrogram.plot(figure)

    def stft_linear_spectrogram(self, song_object):
        song_data = song_object.song_data

        stft_song_data = librosa.stft(song_data) # short-time Fourier transform
        amplitude_scale = librosa.amplitude_to_db(np.abs(stft_song_data), ref=np.max)

        fig, ax = plt.subplots()
        img = librosa.display.specshow(amplitude_scale, x_axis='time', y_axis='linear', ax=ax)
        ax.set(title='stft linear spectrogram')
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        return fig
    
    def log_frequency_axis(self, song_object):
        song_data = song_object.song_data
        sample_rate = song_object.original_sample_rate

        stft_song_data = librosa.stft(song_data) # short-time Fourier transform  D
        amplitude_scale = librosa.amplitude_to_db(np.abs(stft_song_data), ref=np.max) # S_db


        fig, ax = plt.subplots()
        img = librosa.display.specshow(amplitude_scale, x_axis='time', y_axis='log', ax=ax)
        ax.set(title='Using a logarithmic frequency axis')
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        return fig
    
    def mel_spectrogram(self, song_object):
        song_data = song_object.song_data
        sample_rate = song_object.original_sample_rate

        mel_song_data = librosa.feature.melspectrogram(y=song_data, sr=sample_rate)
        mel_song_data_db = librosa.power_to_db(mel_song_data, ref=np.max)

        fig, ax = plt.subplots()
        img = librosa.display.specshow(mel_song_data_db, y_axis='mel', x_axis='time', ax=ax)
        ax.set(title='Mel spectrogram display')
        fig.colorbar(img, ax=ax, format="%+2.f dB")
        return fig