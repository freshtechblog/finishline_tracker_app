import time
import json
from SerialComm import SerialComm
import threading
from enum import Enum
from Stopwatch import Stopwatch
from Lane import Lane
from Racer import Racer
from config import config
from DataRunner import DataRunner

class Request(Enum):
    NONE = 1
    TO_SETUP = 2
    TO_READY = 3
    TO_RACE = 4
    UPDATE_RACERS = 10

class RaceTracker():
    """Class which manages the communication to the finish line tracker hardware
    """
    def __init__(self, com):
        """Initializer

        Args:
            com (str): The com of the hardware
        """
        self.hw_comm = SerialComm(com)
        self.lanes = [Lane(), Lane(), Lane(), Lane()]
        self.racer_dictionary = {}
        self.data_runner = DataRunner('google_sheets_config.json')
        self.custom_race = False
        
        self.request = [Request.NONE, None]

        self.thread_running = True
        self.thread = threading.Thread(target=self.update_loop)
        self.thread.start()

        self.race_data = ""
        self.board_data = ""
    
    #for thread to update data from the hardware
    def update_loop(self):
        """Update loop
        """
        
        #get the board data
        self.board_data = self.hw_comm.send_json_data(r'{"method":"board"}') 

        #update the race data
        self.race_data = self.hw_comm.send_json_data(r'{"method":"getdata"}')

        previous_time = time.time() 
        interval = .05 # Interval in seconds

        while self.thread_running:
            current_time = time.time()
                        
            #update config if requested
            if self.request[0] == Request.UPDATE_RACERS:
                #add method to config so hardware knows what to do with config
                config={"method": "config"}
                config["inRace"] = [1 if p else 0 for p in [lane.in_race() for lane in self.lanes]]
                cfgJson = json.dumps(config, separators=(',', ':'))
                self.hw_comm.send_json_data(cfgJson)
                self.request[1].set()
                self.request = [Request.NONE, None]
            elif self.request[0] == Request.TO_SETUP:
                self.hw_comm.send_json_data(r'{"method":"setup"}')
                self.request[1].set()
                self.request = [Request.NONE, None]
            elif self.request[0] == Request.TO_READY:
                self.hw_comm.send_json_data(r'{"method":"ready"}')
                self.request[1].set()
                self.request = [Request.NONE, None]
            elif self.request[0] == Request.TO_RACE:
                self.hw_comm.send_json_data(r'{"method":"race"}')
                self.request[1].set()
                self.request = [Request.NONE, None]
            

            # Check if the interval has passed
            if current_time - previous_time >= interval:
                previous_time = current_time     

                #get the board data
                self.board_data = self.hw_comm.send_json_data(r'{"method":"board"}') 

                #update the race data
                self.race_data = self.hw_comm.send_json_data(r'{"method":"getdata"}')

                #update the lane data
                self.update_lane_data()

            time.sleep(.01)

    def update_lane_data(self):
        """Update the data for each lane
        """
        #create json object from data
        jsonObj = json.loads(self.race_data)
        for (index,lane) in enumerate(self.lanes):
            lane.finish_position = self.positionToString(jsonObj["finishPosition"][index])
            lane.finish_time = self.format_milliseconds(jsonObj["finishTime"][index])

    def get_race_message(self):
        """Get the message from the tracker hardware

        Returns:
            str: Message from the hardware
        """
        #create json object from data
        if self.race_data == '':
            return ""
        jsonObj = json.loads(self.race_data)
        return jsonObj["message"]
    
    def get_race_status(self):
        """Get the status of the race from the hardware

        Returns:
            str: The status of the race
        """
        #create json object from data
        jsonObj = json.loads(self.race_data)
        return jsonObj["status"]

    def format_milliseconds(self, ms):
        """Format a time into a string

        Args:
            ms (Any): The time in milliseconds

        Returns:
            str: The time as a string in seconds
        """
        if ms == 0 : return ""
        # Convert milliseconds to seconds
        seconds = ms / 1000.0
        # Format the seconds to three decimal places
        return "{:.3f}s".format(seconds)

    def positionToString(self, pos):
        """The position as a string

        Args:
            pos (Any): The position

        Returns:
            str: The position as a string with proper ending
        """
        if pos == 1:
            return "1st"
        elif pos == 2:
            return "2nd"
        elif pos == 3:
            return "3rd"
        elif pos == 4:
            return "4th"
        else:
            return ""

    def load_racers(self):
        """Load the racers from the google sheet
        """
        print("Loading racers...", end='')
        self.racer_dictionary={}
        self.add_Racer("A","A")
        self.add_Racer("B","B")
        self.add_Racer("C","C")
        self.add_Racer("D","D")
        for racer in self.data_runner.get_all_racers():
            self.add_Racer(racer[1], racer[0])
        print("done")
    
    def add_Racer(self, name, id):
        """Add a racer to the dictionary of racers. Dictionary keys 
        are the racer numbers with the value as the name

        Args:
            name (str): The name of the racer
            id (int): The number of the racer
        """
        self.racer_dictionary[id] = Racer(name,id)

    def close(self) -> None:
        """Method to call when closing the tracker
        """
        self.thread_running = False

        #wait for update loop thread to stop
        self.thread.join()
        self.hw_comm.close_connection()  
        
    def set_current_racers(self, racer_ids):
        """Update the racers participating in the race takes in the racer id 
        for each lane. This should be an array of four. If there is no 
        racer in a lane, pass a none.

        Args:
            racer_ids (List[int]): List of the racer ids to set for the race
        """
        print("Setting the current racers...", end='')
        for (index, id) in enumerate(racer_ids):
            if id == None:
                self.lanes[index].remove_racer()
            else:
                self.lanes[index].insert_racer(self.racer_dictionary[id]) 
        wait_event = threading.Event()
        self.request = [Request.UPDATE_RACERS, wait_event]
        wait_event.wait()
        print('done')

    def set_setup(self):
        """Try to set the hardware into the setup state
        """
        print("Setting status to setup...", end='')
        self.custom_race = False
        wait_event = threading.Event()
        self.request = [Request.TO_SETUP, wait_event]
        wait_event.wait()
        print('done')

    def set_ready(self):
        """Try to set the hardware into the ready state
        """
        print("Setting status to ready...", end='')
        wait_event = threading.Event()
        self.request = [Request.TO_READY, wait_event]
        wait_event.wait()
        print('done')

    def set_race(self):
        """Try to set the hardware to the race state
        """
        print("Setting status to race...", end='')
        wait_event = threading.Event()
        self.request = [Request.TO_RACE, wait_event]
        wait_event.wait()
        print('done')
        #create a thread to monitor the end of the race, then push the results
        threading.Thread(target=self.watch_and_push_results).start()

    def watch_and_push_results(self):
        """Method to watch and wait for the race to complete.
        """
        print("Waiting for race to finish...", end='')
        while json.loads(self.race_data)["status"]!="FINISHED":
            time.sleep(.5)
        print('done')
        print('pushing results to google sheet...',end='')
        #now that race is finished, push the results
        self.data_runner.set_race_positions([str(pos) for pos in json.loads(self.race_data)["finishPosition"]])
        print('done')

    def print_race_info(self):
        """Print the race info
        """
        for lane in self.lanes:
            print(lane)

if __name__ == "__main__":
    tracker = RaceTracker('COM3')
    
    tracker.racer_dictionary[0] = Racer("Jason",0)
    tracker.racer_dictionary[2] = Racer("Benji",2)
    tracker.racer_dictionary[3] = Racer("Remy",3)

    tracker.set_ready()

    tracker.set_race()
    
    stopwatch = Stopwatch()
    stopwatch.start()

    while(stopwatch.get_time()<10):
        time.sleep(.1)
        print(tracker.race_data)
        # print(tracker.board_data)
    # print(tracker.get_data())
    # tracker.print_race_info()

    tracker.set_setup()
    time.sleep(1)
    print(tracker.race_data)
    tracker.close() 