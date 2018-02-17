import time, multiprocessing
from smbus import SMBus

# Address of the PCF8574 I/0 Expander
bus = SMBus(1)
io_id = 0x20
byte = bus.read_byte(io_id)

# Inputs/Outputs
gpio = {"1": 0x01, "2": 0x02, "3": 0x04, "4": 0x08, "5": 0x10, "6": 0x20, "7": 0x40, "8": 0x80}

# Get state of GPIO
class getState(multiprocessing.Process):
    def __init__(self):
        super(getState, self).__init__()

    def run(self):
        states = []
        for k,v in gpio.items():
            if(byte & v == 0):
                state.append(1)
            else:
                state.append(0)
        print state

# Set state of output
class SetOutput(multiprocessing.Process):
    def __init__(self, id, *args):
        self.id = id
        self.gpio = gpio[self.id]
        self.type = args[0]
        self.pperiod = args[1]
        if(len(args) == 0):
            self.type = "toggle"
        else:
            if(len(args) > 1):
                self.period = args[1]
            else:
                self.period = 0
        self.exit = multiprocessing.Event()
        super(Timer, self).__init__()

    def run(self):
        while not self.exit.is_set():
            data = self.id ^ ~byte
            gpio_set = bus.write_byte_data(io_id, 0x00, ~data)

            if(self.type == "toggle"):
                gpio_set()
            else:
                if(byte & self.id != 0): gpio_set()
                time.sleep(self.pperiod)
                if(byte & self.id != 1): gpio_set()
                if self.period == 0: self.exit.set()
                time.sleep(self.period)

    def terminate(self):
        self.exit.set()
   
if __name__ == "__main__":
    relays = SetOutput("1", "toggle", 0, 0)
    relays.start()
