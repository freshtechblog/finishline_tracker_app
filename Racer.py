from PIL import Image
from pathlib import Path
from config import config

class Racer():
    """Class to hold information about a Racer
    """
    def __init__(self, name, number):
        """Initializer

        Args:
            name (str): The name of the racer
            number (int): The racer's number
        """
        self.name = name
        self.number = number

        if Path(f"photos\\{number}.png").exists():
            self.image = Image.open(f"photos\\{number}.png")
        else:
            self.image = Image.open("person_icon.png")
        
    def __repr__(self):
        return f"{self.name}"   

if __name__ == "__main__":
    racer = Racer("Jason",10)