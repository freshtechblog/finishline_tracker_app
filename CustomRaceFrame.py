import tkinter as tk

class CustomRaceFrame(tk.Frame):
    """Frame to hold the data for the Custom race information

    Args:
        tk (tkinker.Frame): The parent Tkinter frame
    """
    def __init__(self, parent, tracker, **kwargs):
        """Init for class

        Args:
            parent (tkinter.Frame): The class that should hold this frame
            tracker (Tracker): The Tracker class
        """
        super().__init__(parent, **kwargs)
        
        self.tracker = tracker

        self.config(bd=2,relief=tk.SOLID)

        # Store references to racer entry widgets in a dictionary
        self.racer_entries = {}

        # Create a button called "Custom Setup" and make it fill the width of the frame
        self.custom_setup_button = tk.Button(self, text="Custom Setup", command=self.custom_setup)
        self.custom_setup_button.grid(row=0, column=0, columnspan=2, padx = 20, pady=20, sticky="ew")

        # Racer labels
        racer_labels = ['A', 'B', 'C', 'D']

        # Create four rows, each containing text that says "Racer" followed by a text entry box
        for i, label in enumerate(racer_labels):
            racer_label = tk.Label(self, text=f"Racer {label}")
            racer_label.grid(row=i+1, column=0, padx=10, pady=10, sticky="w")

            racer_entry = tk.Entry(self)
            racer_entry.grid(row=i+1, column=1, padx=10, pady=10, sticky="ew")

            # Store reference to the racer entry in the dictionary
            self.racer_entries[label] = racer_entry

        # Configure column weights to ensure the entry boxes fill to the right
        self.grid_columnconfigure(0, weight=0)
        self.grid_columnconfigure(1, weight=1)

    def custom_setup(self): 
        """Set up a custom list of racers
        """
        print("setting custom racers...",end='')
        
        # Return a list of the keys of racer_entries where the entry in the list is None if the value is empty
        for _,(key,value) in enumerate(self.racer_entries.items()):
            self.tracker.add_Racer(value.get(),key)
        racer_ids = [key if value.get()!="" else None for _,(key,value) in enumerate(self.racer_entries.items())]
        self.tracker.set_current_racers(racer_ids)  
        print('done')

# Main application window
if __name__ == "__main__":
    root = tk.Tk()
    root.title("Custom Race Frame Example")
    root.geometry("300x200")

    # Create an instance of CustomRaceFrame
    tracker = "Tracker Variable Example"  # Replace this with your actual tracker variable
    custom_race_frame = CustomRaceFrame(root, tracker)
    custom_race_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)  # Add padding when packing the frame

    root.mainloop()
