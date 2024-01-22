import random

class Kicks:
    def detect(song_path):
        print(f"Loading {song_path} into kick detector")

        # Just returns random array until further implemented
        num_events = random.randint(1, 50)  # Generate a random number of events
        events = list(sorted(random.sample(range(1, 2401), num_events)))  # Generate random events
        return events
       
