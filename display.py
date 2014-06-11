import serial
from time import sleep

class PiLcdDisplay(object):
    def __init__(self, screen):
        self.ser = serial.Serial()
        self.ser.port = "/dev/ttyAMA0"
        self.ser.baudrate = 9600
        self.ser.open()
        self.line1 = ""
        self.line2 = ""
        self.update()

    def clear(self):
        self.ser.write("\xfe\x01")

    def update(self):
        self.clear()
        line1_padded = self.line1[:16].ljust(16)
        line2_padded = self.line2[:16].ljust(16)
        self.ser.write(line1_padded + line2_padded)

    def set(self, line1, line2=""):
        if line1 != self.line1 or line2 != self.line2:
            self.line1 = line1
            self.line2 = line2
            self.update()

class FakeDisplay(object):
    def __init__(self, screen):
        self.screen = screen
        self.line1 = ""
        self.line2 = ""
        self.update()

    def clear(self):
        self.screen.clear()

    def update(self):
        self.clear()
        self.screen.refresh()
        self.screen.addstr(2, 20, self.line1)
        self.screen.addstr(3, 20, self.line2)

    def set(self, line1, line2=""):
        if line1 != self.line1 or line2 != self.line2:
            self.line1 = line1
            self.line2 = line2
            self.update()

if __name__ == "__main__":
    display = PiLcdDisplay()
    display.line1 = "Hello"
    display.line2 = "There"
    display.update()

