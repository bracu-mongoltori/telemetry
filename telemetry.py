import serial
from time import sleep

class Telemetry():
    def __init__(self, port="/dev/ttyUSB0", baudrate=9600):
        self.ser = serial.Serial(port, baudrate)

    def read(self):
        return self.ser.readline().decode("utf-8")
    
    def write(self, data):
        self.ser.write(data.encode("UTF-8"))


if __name__ == "__main__":
    t = Telemetry()
    while True:
        inp = input("> Enter data: ")
        t.write(inp)
        sleep(1)
        print(t.read())
        sleep(1)