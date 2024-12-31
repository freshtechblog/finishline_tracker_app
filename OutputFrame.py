import tkinter as tk
import sys
import queue
import threading

class OutputFrame(tk.Frame):
    """Frame to hold the data outputted to the terminal

    Args:
        tk (tkinter.Frame): The parent frame
    """
    def __init__(self, parent=None, **kwargs):
        """Initializer

        Args:
            parent (tinkter.Frame, optional): The parent frame of this frame. Defaults to None.
        """
        super().__init__(parent, **kwargs)
        self.text = tk.Text(self, wrap='word')
        self.text.grid(row=0, column=0, padx=0, pady=0, sticky='nsew')
        self.config(bd=2, relief=tk.SOLID)
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.queue = queue.Queue()
        self.stdout = sys.stdout
        sys.stdout = self

        self.process_queue()

    def write(self, message):
        """Write a message

        Args:
            message (str): Message to output
        """
        self.queue.put(message)

    def flush(self):
        pass  # Needed for file-like object compatibility

    def process_queue(self):
        """The queue of text to output
        """
        try:
            while True:
                message = self.queue.get_nowait()
                self.text.insert('end', message)
                self.text.see('end')
        except queue.Empty:
            pass
        self.after(100, self.process_queue)

    def destroy(self):
        sys.stdout = self.stdout
        super().destroy()

# Main application
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Terminal to Tkinter")
        self.geometry("600x400")

        # Create and pack the OutputFrame
        self.output_frame = OutputFrame(self)
        self.output_frame.pack(fill='both', expand=True)

        # Add a button to simulate messages
        self.button = tk.Button(self, text="Send Message", command=self.start_thread)
        self.button.pack()

    def send_message(self):
        print("This is a message sent to the terminal.")

    def start_thread(self):
        threading.Thread(target=self.send_message).start()

if __name__ == "__main__":
    app = App()
    app.mainloop()
