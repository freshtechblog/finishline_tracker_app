import tkinter as tk
from tkinter import scrolledtext
import sys
import io

class EditorFrame(tk.Frame):
    def __init__(self, parent, reference_object, **kwargs):
        super().__init__(parent, **kwargs)
        
        self.config(bd=2,relief=tk.SOLID)
        self.reference_object = reference_object
        
        # Configure the grid for expansion
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Create a scrolled text widget for code input
        self.code_editor = scrolledtext.ScrolledText(self, wrap=tk.WORD)
        self.code_editor.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Bind Ctrl+Enter to run the code
        self.code_editor.bind('<Control-Return>', self.run_code_event)

        # Create a button to run the code
        self.run_button = tk.Button(self, text="Run Code", command=self.run_code)
        self.run_button.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Create a text widget for output
        self.output_box = scrolledtext.ScrolledText(self, wrap=tk.WORD, state=tk.DISABLED)
        self.output_box.grid(row=2, column=0, padx=10, pady=10, sticky="nsew")

    def run_code_event(self, event):
        self.run_code()
        return "break"

    def run_code(self):
        # Capture the code from the editor
        code = self.code_editor.get("1.0", tk.END)
        
        # Redirect stdout to capture print statements
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout
        
        try:
            # Create a local namespace with the reference object
            local_vars = {'self': self.reference_object}
            # Execute the code with local_vars as locals
            exec(code, globals(), local_vars)
            output = new_stdout.getvalue()
        except Exception as e:
            output = str(e)
        finally:
            # Restore stdout
            sys.stdout = old_stdout

        # Display the output
        self.output_box.config(state=tk.NORMAL)
        self.output_box.delete("1.0", tk.END)
        self.output_box.insert(tk.END, output)
        self.output_box.config(state=tk.DISABLED)

class MyObject:
    def __init__(self):
        self.data = "This is some data"
    
    def do_something(self):
        return "This is a method of MyObject"

class CodeEditorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Python Code Editor")

        # Create an instance of MyObject
        self.my_object = MyObject()

        # Create an instance of EditorFrame
        self.editor_frame = EditorFrame(root, self.my_object, bd=2, relief=tk.SOLID)
        self.editor_frame.pack(fill=tk.BOTH, expand=True)

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    root.geometry("800x600")  # Set the initial size of the window

    # Create an instance of CodeEditorApp
    app = CodeEditorApp(root)

    # Start the Tkinter event loop
    root.mainloop()
