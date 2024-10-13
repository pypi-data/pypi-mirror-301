import threading

from padislib.renderer.checkpadis_runner import CheckpadisRunner
from padislib.utils.state_progress import StateProgress


class ProgressManager:
    def __init__(self):
        self.progress_state = StateProgress()
        self.runner = CheckpadisRunner()
        self.progress_thread = None

    def start_progress(self):
        """
        Starts a new thread to display the progress of a task.

        This method initializes a new thread that runs the `display_progress`
        method of the `runner` object, passing the `progress_state` as an
        argument. The thread is then started to begin displaying the progress.
        """
        self.progress_thread = threading.Thread(
            target=self.runner.display_progress, args=(self.progress_state,)
        )
        self.progress_thread.start()

    def stop_progress(self):
        """
        Stops the progress thread if it is running.
        This method checks if the progress thread is active and, if so, waits
        for it to complete by calling the join() method.
        """

        if self.progress_thread:
            self.progress_thread.join()
