
import serial
import time
import threading 

class SerialComm:
    """Class to handle communication to a serial port
    """
    def __init__(self, port, baudrate=115200, timeout=1):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.connect()
        
        # Set read and write buffer sizes
        self.serial_connection.set_buffer_size(rx_size=4096, tx_size=4096)
        self.thread_running = True
        self.thread = threading.Thread(target=self.get_data_loop)
        self.thread.start()
        self.last_json = ""
        self.wait_event = threading.Event()
        self.wait_event.set()
        time.sleep(2)  # Give some time for the connection to establish

    def connect(self):
        """connect to the serial port
        """
        while True:
            try:
                self.serial_connection = serial.Serial(self.port, self.baudrate, timeout=self.timeout)
                print("Connected to serial port.")
                break
            except serial.SerialException as e:
                print(f"Failed to connect: {e}. Retrying in 1 second...")
                time.sleep(1)
    
    def read_from_serial(self):
        """Read data from the serial port

        Returns:
            str: the string data from the serial port
        """
        while True:
            try:
                if self.serial_connection.is_open:
                    self.serial_connection.reset_input_buffer()
                    val = self.serial_connection.readline()
                    return val.decode().strip()
                else:
                    print("Serial port not open")
            except PermissionError as e:
                print(f"PermissionError: {e}")
                self.serial_connection.close()
                print("Trying to reconnect...")
                self.connect()
            except serial.SerialException as e:
                print(f"SerialException: {e}")
                self.serial_connection.close()
                print("Trying to reconnect...")
                self.connect()

    def send_json_data(self, data) -> str:
        """Send json data to the serial port and wait for a json response

        Args:
            data (str): json data as a string

        Returns:
            str: string of the response json
        """
        if self.serial_connection.is_open: 
            self.wait_event = threading.Event()
            # Append the newline character to the data 
            data_with_newline = data + '\n'
            
            #send data in chunks
            for i in range(0, len(data_with_newline), 128):
                chunk = data_with_newline[i:i + 128]
                self.serial_connection.write(chunk.encode())
                self.serial_connection.flush()
                time.sleep(.001)  # Small delay to ensure the buffer is not overwhelmed

            self.wait_event.wait()
            return self.last_json
        return ""


    def receive_data(self) ->str:
        """Read the data from a serial port

        Returns:
            str: The data read from the serial port
        """
        if self.serial_connection.is_open:
            txt = self.serial_connection.readline()
            return txt.decode().strip()
        else:
            return ""
        
    def close_connection(self):
        """Close the connection to the serial port
        """
        if self.thread_running:
            self.thread_running = False
            self.thread.join()
        if self.serial_connection.is_open:
            self.serial_connection.close()

    def get_data_loop(self):
        """Loop to get data. if data doesn't start with "{", then print it. 
        Data that starts with "{" is a json object.
        """
        while(self.thread_running):
            data = self.read_from_serial()
            if data is None or len(data)==0:
                continue
            elif data[0]!="{" and data[0].strip() !="":
                print(data)
            else:
                self.last_json = data
                self.wait_event.set()

    def is_connected(self):
        """Return true if the port is connected

        Returns:
            Bool: returns true if there is a connection open
        """
        return self.serial_connection.is_open        
    


# Example usage
if __name__ == "__main__":        
    # Replace 'COM3' with your port name
    serial_comm = SerialComm(port='COM3', baudrate=115200, timeout=1)

    # Send data
    for i in range(0,10):
        response = serial_comm.send_json_data(r'{"method":"getdata"}')    
        print(f"{i} : {response}")

    serial_comm.close_connection()  
