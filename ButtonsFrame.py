import tkinter as tk
from EditorFrame import EditorFrame

class ButtonsFrame(tk.Frame):
    
    def __init__(self, parent, tracker, *args, **kwargs):
        super().__init__(parent,**kwargs)
        self.parent = parent
        self.tracker = tracker
        self.config(bd=2, relief=tk.SOLID)        

        # Spacer to push the next buttons to the right 
        self.spacer = tk.Label(self, text="", width=1) 
        self.spacer.pack(side=tk.LEFT, expand=True)
        
        self.start_button = tk.Button(self, text="START", command=lambda:self.tracker.set_race(), width=25)
        self.start_button.pack(side=tk.RIGHT, padx=(10, 10), pady=10)

        self.ready_button = tk.Button(self, text="Ready", command=lambda:self.tracker.set_ready(), width=25)
        self.ready_button.pack(side=tk.RIGHT, padx=(10, 0), pady=10)

        self.setup_button = tk.Button(self, text="Sheets Racers", command=self.sheets_clicked, width=25)
        self.setup_button.pack(side=tk.RIGHT, padx=(10, 0), pady=10)

        self.setup_button = tk.Button(self, text="Setup", command=lambda:self.tracker.set_setup(), width=25)
        self.setup_button.pack(side=tk.RIGHT, padx=(10, 0), pady=10)

        self.load_racers_button = tk.Button(self, text="Load Racers", command=lambda:self.tracker.load_racers(), width=25)
        self.load_racers_button.pack(side=tk.RIGHT, padx=(10, 0), pady=10)

        self.testing_button = tk.Button(self, text="Testing", command=self.test_button_clicked, width=25)
        self.testing_button.pack(side=tk.RIGHT, padx=(10, 30), pady=10)

    def sheets_clicked(self):
        print("getting current racers from google sheet...",end='')
        racers = self.tracker.data_runner.get_current_racer()
        print("done")
        print("setting google sheet racers...",end='')
        racer_numbers = [racer[0] if racer else None for racer in racers]
        self.tracker.set_current_racers(racer_numbers)
        print('done')
        
    def update_frame(self):
        pass
        # self.status_text.set(self.tracker.get_race_status())

    def open_editor_window(self):
        # Create a new window
        new_window = tk.Toplevel(self.parent)
        new_window.title("Editor")

        # Create an instance of CustomFrame and add it to the new window
        custom_frame = EditorFrame(new_window, self)
        custom_frame.pack(fill=tk.BOTH, expand=True)
        

    def test_button_clicked(self):
        self.tracker.set_setup()
        self.tracker.set_ready()
        self.tracker.set_race()
