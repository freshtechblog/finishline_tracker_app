import tkinter as tk
from EditorFrame import EditorFrame
from OutputFrame import OutputFrame
from DataFrame import DataFrame
from CustomRaceFrame import CustomRaceFrame

class DebugWindow(tk.Toplevel):
    def __init__(self, parent, tracker, master=None):
        super().__init__(parent)
        self.tracker = tracker
        self.parent = parent
        self.title("Debug")
        self.geometry("800x700")

        self.output_frame = OutputFrame(self)
        self.output_frame.grid(row=0, column=0,sticky='nsew')
        self.output_frame.grid_propagate(False)

        self.editor_frame = EditorFrame(self,parent)
        self.editor_frame.grid(row=0, column=1,sticky='nsew')
        self.editor_frame.grid_propagate(False)
        
        self.data_frame = DataFrame(self,self.tracker)
        self.data_frame.grid(row=1, column=0,sticky='nsew')
        self.data_frame.grid_propagate(False)

        self.custom_race_frame = CustomRaceFrame(self,self.tracker)
        self.custom_race_frame.grid(row=1, column=1,sticky='nsew')
        self.custom_race_frame.grid_propagate(False)

        self.grid_columnconfigure(0,weight=1) 
        self.grid_columnconfigure(1,weight=1)
        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)

    def update_window(self):
        self.parent.after(0,self.data_frame.update_frame)

class MainApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Main Application Window")
        self.geometry("300x200")

        # Button to open the secondary window
        self.open_window_button = tk.Button(self, text="Open Secondary Window", command=self.open_secondary_window)
        self.open_window_button.pack(pady=20)

    def open_secondary_window(self):
        secondary_window = DebugWindow(self)

if __name__ == "__main__":
    app = MainApp()
    app.mainloop()
