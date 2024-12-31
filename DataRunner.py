from GoogleSheetManager import GoogleSheetManager
import json

class DataRunner:
    """Class to get data from a google sheet
    """
    def __init__(self, json_config_filepath):
        self.is_sheets_connected = True
        try:
            self.config = json.loads(open(json_config_filepath, 'r').read())
            self.gsmanager = GoogleSheetManager(
                self.config['credentials'],
                self.config['token'],
                self.config['worksheet'])
        except:
            self.is_sheets_connected = False
    
    def get_all_racers(self):
        if self.is_sheets_connected:
            data = self.gsmanager.get_range(self.config['racer_range'], self.config['racer_sheet'])
            return [sublist for _, sublist in enumerate(data) if len(sublist) == 2]
        
        else:
            return {}

    def get_current_racer(self):
        if self.is_sheets_connected:
            return self.gsmanager.get_range(self.config['current_race_range'], self.config['current_race_sheet'])
        else:
            return {}
    
    def set_race_positions(self,arr):
        if self.is_sheets_connected:
            self.gsmanager.set_range(self.config['race_position_range'], [[str(pos)] for pos in arr], self.config['current_race_sheet'])

if __name__ == "__main__":
    dr = DataRunner()
    print(dr.get_all_racers())