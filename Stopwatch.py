import time

class Stopwatch:
    """Stopwatch class to keep track of timing
    """
    def __init__(self):
        """Initializer
        """
        self.start_time = None
        self.elapsed_time = 0
        self.running = False

    def start(self):
        """Start the timer
        """
        if not self.running:
            self.start_time = time.time() - self.elapsed_time
            self.running = True
            print("Stopwatch started.")

    def stop(self):
        """Stop the timer
        """
        if self.running:
            self.elapsed_time = time.time() - self.start_time
            self.running = False
            print("Stopwatch stopped.")

    def reset(self):
        """Reset and stop the timer
        """
        self.start_time = None
        self.elapsed_time = 0
        self.running = False
        print("Stopwatch reset.")

    def get_time(self):
        """Get the current time on the timer if running, the elapsed time
        if stopped.

        Returns:
            float: The time in seconds
        """
        if self.running:
            return time.time() - self.start_time
        else:
            return self.elapsed_time

    def format_time(self, seconds)->str:
        """Format the time in seconds to a string

        Args:
            seconds (float): The time in seconds

        Returns:
            str: A string of the time
        """
        millis = int((seconds % 1) * 1000)
        seconds = int(seconds)
        mins, secs = divmod(seconds, 60)
        hours, mins = divmod(mins, 60)
        return f"{hours:02}:{mins:02}:{secs:02}.{millis:03}"


if __name__=="__main__":
    stopwatch = Stopwatch()
    stopwatch.start()