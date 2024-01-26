"""
Module: TimeUpdateThread

This module is responsible for managing the time updates in a separate thread. It emits a signal every time the time needs to be updated.
The TimeUpdateThread class is the main class in this module.

Arguments:
    None

Returns:
    None

The TimeUpdateThread class has several methods to manage the time updates. The 'run' method runs the thread and emits a signal with the updated time.
The 'start_clock' method starts the clock and begins the execution of the thread. The time updates are managed using a condition variable to synchronize the thread execution.
"""


import time
from threading import Condition
from PyQt5.QtCore import (
    pyqtSignal,
    QThread,
)
import constants


class TimeUpdateThread(QThread):
    # This class updates the time in a separate thread
    # Define a signal that will be emitted every time the label needs to be updated
    time_updated = pyqtSignal(int)

    STOPPED, RUNNING, PAUSED = range(3)

    def __init__(self):
        super().__init__()
        # self.model = main_controller.model
        self.state = self.STOPPED
        self.elapsed_time = 0
        self.start_time = None
        self.pause_time = None
        self.condition = Condition()
        self.time_per_frame_seconds = (
            constants.PROJECT_FPS / 1000
        )  # time per frame in seconds

    def run(self):
        # This function runs the thread
        while True:
            with self.condition:
                while self.state != self.RUNNING:
                    self.condition.wait()  # Pauses the thread
                adjusted_time = self.elapsed_time + (
                    time.perf_counter() - self.start_time
                )
                frame_number = int(adjusted_time * constants.PROJECT_FPS)
                self.time_updated.emit(frame_number)
            time.sleep(self.time_per_frame_seconds)

    def start_clock(self):
        # This function starts the clock
        with self.condition:
            if self.state == self.STOPPED:
                print(f"starting clock")
                self.start_time = time.perf_counter()
                self.state = self.RUNNING
                self.condition.notify_all()  # Wakes up all threads waiting on this condition
                self.start()  # Begins execution of the thread

    def pause_clock(self):
        # This function pauses the clock
        with self.condition:
            if self.state == self.RUNNING:
                self.paused_time = time.perf_counter()
                current_time = time.perf_counter()
                self.elapsed_time += current_time - self.start_time
                self.state = self.PAUSED
                # print(
                #     f"paused clock at {self.paused_time}, elapsed time is {self.elapsed_time}"
                # )

    def resume_clock(self):
        # This function resumes the clock
        with self.condition:
            if self.state == self.PAUSED:  # get the elapsed time
                self.start_time = time.perf_counter()
                self.state = self.RUNNING
                self.condition.notify_all()
                # print(f"resuming clock at start time {self.start_time}")

    def reset_clock(self):
        # This function resets the clock
        with self.condition:
            if self.state == self.PAUSED:
                # print(f"resetting clock")
                self.elapsed_time = 0
                self.start_time = None

            elif self.state == self.RUNNING:
                # print(f"resetting clock")
                self.state = self.PAUSED
                self.elapsed_time = 0
                self.start_time = time.perf_counter()
                self.state = self.RUNNING
                self.condition.notify_all()

            elif self.state == self.STOPPED:
                # print(f"resetting clock")
                self.state = self.STOPPED
                self.elapsed_time = 0
                self.start_time = None

    def stop_clock(self):
        # This function stops the clock
        if self.state == self.RUNNING:
            self.state = self.STOPPED

        if self.state == self.PAUSED:
            self.state = self.STOPPED
