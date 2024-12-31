import tkinter as tk
from PIL import Image, ImageTk
from Racer import Racer
from Lane import Lane
from config import config

class LaneFrame(tk.Frame):
    """Frame for the Lane data

    Args:
        tk (tkinter.Frame): Parent frame
    """
    def __init__(self, parent, lane, **kwargs):
        """Initializer

        Args:
            parent (tkinter.Frame): The parent frame that will hold this frame
            lane (Lane): The lane data
        """
        super().__init__(parent, **kwargs)
        
        self.lane = lane
        self.image_width = 450
        self.image_height = 450
        self.update_racer = True

        self.display_image()       

        self.grid_rowconfigure(0,weight=1)
        self.grid_rowconfigure(1,weight=1)
        self.grid_rowconfigure(2,weight=1) 
        self.grid_rowconfigure(3,weight=1)
        self.grid_columnconfigure(0,weight=1)

        self.name = tk.StringVar()
        self.name.set(self.lane.get_racer_name())
        self.name_label = tk.Label(self, textvariable=self.name)
        self.name_label.config(font=(config["font"], config["font_size"]))
        self.name_label.grid(row = 1, padx=10, pady=10, sticky="nsew")

        self.finish_position = tk.StringVar()
        self.name.set(self.lane.finish_position)
        self.finish_position_label = tk.Label(self, textvariable=self.finish_position)
        self.finish_position_label.config(font=(config["font"], config["font_size_finish_position"]))
        self.finish_position_label.grid(row = 2, padx=10, pady=10, sticky="nsew")

        self.finish_time = tk.StringVar()
        self.name.set(self.lane.finish_time)
        self.finish_time_label = tk.Label(self, textvariable=self.finish_time)
        self.finish_time_label.config(font=(config["font"], config["font_size"]))
        self.finish_time_label.grid(row = 3, padx=10, pady=10, sticky="nsew")

        self.lane.updated_racer_event.subscribe(self.racer_callback)

    def racer_callback(self, racer):
        """Callback when the lane has change, e.g. changes in racer

        Args:
            racer (Racer): The racer data
        """
        self.update_racer=True
        
    def display_image(self): 
        """Display the image of the racer in the frame
        """
        if self.update_racer:
            self.update_racer = False
            # Convert the image to PhotoImage 
            self.photo_image = ImageTk.PhotoImage(self.get_image().resize((self.image_width, self.image_height))) 
            # self.photo_image = ImageTk.PhotoImage(self.get_image()) 
            if hasattr(self, 'image_label'):    
                self.image_label.config(image=self.photo_image) 
                self.image_label.image = self.photo_image # Keep a reference
            else:
                self.image_label = tk.Label(self,image=self.photo_image)
                # self.image_label.pack(fill=tk.BOTH, expand=True)
                self.image_label.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")

    def get_image(self):
        """Get the image for the racer

        Returns:
            ImageFile: The image of the racer
        """
        if(self.lane.racer is None):
            return Image.open("no_racer.png")
        else:
            return self.lane.racer.image

    def update_frame(self):
        """Update the information in the frame
        """
        self.display_image()
        self.name.set(self.lane.get_racer_name())
        self.finish_position.set(self.lane.finish_position)
        self.finish_time.set(self.lane.finish_time)
                
if __name__ == "__main__":
    
    racer = Racer("Jason", 10)
    racer2 = Racer("Benji",20)
    
    lane = Lane()
    lane.insert_racer(racer)
    root = tk.Tk()

    root.title("Lane Frame test")
    root.geometry("1920x1080")
    
    lane_frame = LaneFrame(root,lane)

    lane.insert_racer(racer2)
    lane.finish_position="2nd"
    lane.finish_time = "52.230s"
    lane_frame.update_frame()
    lane_frame.pack()
    
    root.mainloop()