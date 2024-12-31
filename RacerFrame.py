import tkinter as tk
from LaneFrame import LaneFrame
from Racer import Racer
from Lane import Lane
from config import config

class RacerFrame(tk.Frame):
    """Frame to hold Racer data

    Args:
        tk (tkinter.Frame): The parent frame
    """
    def __init__(self, parent, lanes, **kwargs):
        """Initializer

        Args:
            parent (tkinter.Frame): Parent frame to hold this frame
            lanes (Lane): The lanes
        """
        super().__init__(parent)
        self.config(bd=2, relief=tk.SOLID)
        self.grid(sticky='nsew', padx = 10, pady = 10)
        self.grid_rowconfigure(0, weight = 1)
        self.lanes = lanes
        self.laneFrames = [
            LaneFrame(self,self.lanes[0]),
            LaneFrame(self,self.lanes[1]),
            LaneFrame(self,self.lanes[2]),
            LaneFrame(self,self.lanes[3])]
        for i in range(0,4):
            self.grid_columnconfigure(i,weight=1)
            self.laneFrames[i].grid(row=0,column=i,padx=5,pady=5,sticky="nsew")

    def update_frame(self):
        """Update the race frame data
        """
        for lane_frame in self.laneFrames:
            lane_frame.update_frame()
        for i in range(0,4):
            self.columnconfigure(i,weight=1)

if __name__ == "__main__":
    
    lane1 = Lane()
    lane1.insert_racer(Racer("Jason", 10))
    lane2 = Lane()
    lane2.insert_racer(Racer("Benji",20))
    lane3 = Lane()
    lane4 = Lane()
    lane4.insert_racer(Racer("Remy",30))
    root = tk.Tk()

    root.title("Lane Frame test")
    root.geometry("1920x1080")
    
    racer_frame = RacerFrame(root,[lane1, lane2, lane3, lane4])
    racer_frame.update_frame()

    root.mainloop()