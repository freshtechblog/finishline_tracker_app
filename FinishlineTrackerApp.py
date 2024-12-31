import tkinter as tk
from RaceTracker import RaceTracker
from RacerFrame import RacerFrame
import threading
import time
from MessageFrame import MessageFrame
from ButtonsFrame import ButtonsFrame
from DebugWindow import DebugWindow

class FinishLineTrackerApp(tk.Frame):
    """Class for the finish line tracker app

    Args:
        tk (tkinter.Frame): The parent frame
    """
    def __init__(self, parent, tracker,**kwargs):
        """Initializer

        Args:
            parent (tkinter.Frame): The parent class that will hold this frame
            tracker (Tracker): The tracker class
        """
        super().__init__(parent, **kwargs)
        self.tracker = tracker
        self.parent = parent

        # create the frames and windows
        self.create_racer_frame()
        self.create_buttons_frame()
        self.create_message_frame()
        self.create_debug_window()

        # start the thread that will perform the data refresh
        self.start_refresh_task()

        # Configure grid weights for autoscaling
        self.grid_columnconfigure(0, weight = 1)
        self.grid_rowconfigure(0, weight = 0)
        self.grid_rowconfigure(1, weight = 0)
        self.grid_rowconfigure(2, weight = 1)

        # Bind the window close event 
        self.parent.protocol("WM_DELETE_WINDOW", self.on_closing)

    def start_refresh_task(self): 
        """Create the thread for refreshing the app
        """
        # Create and start a background thread 
        threading.Thread(target=self.refresh_task, daemon=True).start() 

    def refresh_task(self): 
        """Refresh method
        """
        while(True):
            time.sleep(.01)
            self.parent.after(0, self.racer_frame.update_frame)
            self.parent.after(0, self.message_frame.update_frame)
            self.parent.after(0, self.buttons_frame.update_frame)
            self.parent.after(0, self.debug_window.update_window)

    def create_debug_window(self):
        """Create the debug window
        """
        self.debug_window = DebugWindow(self, self.tracker)

    def create_buttons_frame(self):
        """Create the frame to hold the user buttons
        """
        self.buttons_frame = ButtonsFrame(self, self.tracker)
        self.buttons_frame.grid(row = 0, column = 0, sticky = "nsew")

    def create_message_frame(self):
        """Create the frame that will display the message from the tracker
        """
        self.message_frame = MessageFrame(self, self.tracker)
        self.message_frame.grid(row = 1, column = 0, sticky="nsew")

    def create_racer_frame(self):       
        """Create the frame that will hold the racer information
        """
        self.racer_frame = RacerFrame(self, self.tracker.lanes)
        self.racer_frame.grid_propagate(False)
        self.racer_frame.grid(row = 2, column = 0, sticky="nsew")

    def on_closing(self): 
        """Method called when the app closes
        """
        # Perform cleanup or other actions here 
        print("Window is closing")
        self.tracker.close()
        self.parent.destroy() # Close the window
    
if __name__ == '__main__':

    tracker = RaceTracker('com7')
    
    root = tk.Tk()
    icon = tk.PhotoImage(file="car.png")
    root.iconphoto(True, icon)
    root.title("Finishline tracker")
    root.geometry("1920x1080")
    app = FinishLineTrackerApp(root, tracker)
    app.pack(fill=tk.BOTH, expand=True)
    
    tracker.load_racers()

    root.mainloop()
