import tkinter as tk
from config import config

class MessageFrame(tk.Frame):
    """Frame to hold the tracker message

    Args:
        tk (tkinter.Frame): The parent frame
    """
    def __init__(self, parent, tracker, **kwargs):
        """Initializer

        Args:
            parent (tkinter.Frame): The parent frame the message frame will be held in
            tracker (Tracker): The tracker class
        """
        super().__init__(parent, **kwargs)
        self.config(bd=2, relief=tk.SOLID)     
        self.grid(sticky='nsew', padx = 10, pady = 10)
        self.tracker = tracker
        self.text_var = tk.StringVar()
        self.create_widgets()

    def create_widgets(self):
        """Create the widgets for the class
        """
        self.label = tk.Label(
            self, 
            textvariable=self.text_var, 
            anchor="center", 
            justify="center",
            font=(config["font"],config["font_size_message"]))
        self.label.grid(row=0, column=0, sticky="nsew")

        # Configure the grid to expand properly
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

    def update_text(self, new_text):
        """Update the message

        Args:
            new_text (str): The new text that will be displayed in the frame
        """
        self.text_var.set(new_text)

    def update_frame(self):
        """Update the frame data
        """
        self.update_text(self.tracker.get_race_message())


# Example usage
if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.title("MessageFrame Example")
    root.geometry("400x300")

    # Configure the grid for the main window
    root.grid_rowconfigure(0, weight=1)
    root.grid_columnconfigure(0, weight=1)

    # Create an instance of MessageFrame
    message_frame = MessageFrame(root, bd=2, relief=tk.SUNKEN)
    message_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    # Function to update the text in the MessageFrame
    def update_message():
        new_text = "Updated text content from another part of the application!"
        message_frame.update_text(new_text)

    # Example to update the text after 2 seconds
    root.after(2000, update_message)

    # Start the Tkinter event loop
    root.mainloop()
