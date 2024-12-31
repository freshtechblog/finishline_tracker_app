import tkinter as tk
from config import config 
import json

class DataFrame(tk.Frame):
    """Frame to hold the race and board data

    Args:
        tk (tkinter.Frame): The parent tkinter frame
    """
    def __init__(self, parent, tracker, **kwargs):
        """Initializer

        Args:
            parent (tkinter.Frame): The frame that will hold the dataFrame
            tracker (Tracker): The tracker class
        """
        super().__init__(parent)
        self.tracker = tracker
        self.parent = parent
        self.config(bd=2, relief=tk.SOLID)

        self.race_data_text = tk.StringVar()
        self.race_data_label = tk.Label(self, textvariable=self.race_data_text, justify='left', anchor='nw')
        self.race_data_label.config(font=(config["font"], config["font_size_debug"]))
        self.race_data_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

        self.board_data_text = tk.StringVar()
        self.board_data_label = tk.Label(self, textvariable=self.board_data_text, justify='left', anchor='nw')
        self.board_data_label.config(font=(config["font"], config["font_size_debug"]))
        self.board_data_label.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        self.grid_columnconfigure(0,weight = 1)
        self.grid_rowconfigure(0, weight = 1)
        self.grid_rowconfigure(1, weight = 1)

    def format_dict(self, d, indent=0):
        """Format the dictionary into a string

        Args:
            d (Dictionary): The dictionary to be formatted
            indent (int, optional): The indent spacing. Defaults to 0.

        Returns:
            str : string of the dictionary
        """
        spacing = '  ' * indent
        result = []
        for key, value in d.items():
            if isinstance(value, dict):
                result.append(f"{spacing}{key}:")
                result.append(self.format_dict(value, indent + 1))
            else:
                result.append(f"{spacing}{key}: {value}")
        return '\n'.join(result)
    
    def format_dict_single_line(self, d):
        """Format the dictionary into a single line string

        Args:
            d (Dictionary): The dictionary to be formatted
            indent (int, optional): The indent spacing. Defaults to 0.

        Returns:
            str : string of the dictionary
        """
        result = []
        for key, value in d.items():
            if isinstance(value, dict):
                result.append(f"{key}: {{ {self.format_dict_single_line(value)} }}")
            elif isinstance(value, list):
                result.append(f"{key}: [" + " ".join(f"- {item}" if isinstance(item, str) else str(item) for item in value) + "]")
            else:
                result.append(f"{key}: {value}")
        return " ".join(result)
    
    def update_frame(self):
        """Update the frame with data from the tracker
        """
        if not self.tracker.race_data:
            return
        self.race_data_text.set(self.format_dict(json.loads(self.tracker.race_data)))
        self.board_data_text.set(self.format_dict(json.loads(self.tracker.board_data)))