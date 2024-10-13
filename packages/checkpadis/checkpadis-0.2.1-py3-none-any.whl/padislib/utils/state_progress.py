import threading


class StateProgress:
    def __init__(self):
        self.completed_checks = 0
        self.total_checks = 0
        self.lock = threading.Condition()

    def update_total_checks(self, total):
        self.total_checks = total

    def increment(self):
        with self.lock:
            self.completed_checks += 1
            self.lock.notify_all()

    def get_progress(self):
        return self.completed_checks, self.total_checks
