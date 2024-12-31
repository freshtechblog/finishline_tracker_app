from PIL import Image
from CustomEvent import CustomEvent

class Lane():
    """Class to hold data for a lane
    """
    def __init__(self):
        """Initializer
        """
        self.racer = None
        self.finish_position = ""
        self.finish_time = ""
        self.updated_racer_event = CustomEvent()
        
    def insert_racer(self, racer):
        """Insert a racer into the lane

        Args:
            racer (Racer): The racer to insert
        """
        self.racer = racer
        self.finish_position = ""
        self.finish_time = ""
        self.updated_racer_event.notify(self.racer)

    def remove_racer(self):
        """Remove the racer from the lane
        """
        self.racer = None
        self.finish_position = ""
        self.finish_time = ""
        self.updated_racer_event.notify(self.racer)

    def get_racer_image(self):
        """Get the image of the racer

        Returns:
            ImageFile: The image of the racer
        """
        if self.racer is None:
            return Image.open(f"no_racer.png")
        else:
            self.racer.image
        
    def get_racer_name(self):
        """Get the name of the racer

        Returns:
            str: The name of the racer
        """
        if self.racer is None:
            return ""
        else:
            return self.racer.name
    
    def in_race(self):
        """Bool if the lane is in the race

        Returns:
            Bool: true if the lane will be in the race
        """
        return self.racer!=None
    
    def __repr__(self):
        return f"{f"{self.finish_position} : {self.racer}" if self.in_race() else "empty"}"
    
