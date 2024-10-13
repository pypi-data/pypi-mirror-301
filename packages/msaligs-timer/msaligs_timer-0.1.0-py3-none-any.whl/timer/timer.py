import time

class TimerError(Exception):
    """A custom exception used to report errors in the use of the Timer class."""
    def __init__(self, message="Timer error occurred"):
        self.message = message
        super().__init__(self.message)
    def __str__(self):
        return f"TimerError: {self.message}"

class Timer:
    """A Timer class to measure the running time of a program, with support for context management and multiple runs."""

    def __init__(self):
        self.start_time = None
        self.elapsed_time = None

    def start(self):
        """Start a new timer if it is not already running."""
        if self.start_time is not None:
            raise TimerError("Timer is already running. Use .stop() to stop it before starting again.")
        self.start_time = time.perf_counter()

    def stop(self):
        """Stop the timer, and add the elapsed time to the total elapsed time."""
        if self.start_time is None:
            raise TimerError("Timer is not running. Use .start() to start it.")

        self.elapsed_time = time.perf_counter() - self.start_time
        self.start_time = None

    def reset(self):
        """Reset the timer to its initial state."""
        self.start_time = None
        self.elapsed_time = None

    def elapsed(self):
        """Return the elapsed time """
        if self.elapsed_time is None:
            raise TimerError("Timer has not been run yet. First Run the Timer")
        return self.elapsed_time

    def __repr__(self):
        """Return a string representation of the timer status and elapsed time."""
        status = "running" if self.start_time else "stopped"
        return f"<Timer({status}): {time.perf_counter() - self.start_time:.4f} seconds elapsed>"

    def __str__(self):
        """Return a user-friendly string of the elapsed time."""
        return f"Elapsed time: {self.elapsed():.4f} seconds"