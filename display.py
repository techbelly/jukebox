import serial
from time import sleep
import string


class BaseDisplay(object):

    def __init__(self):
        self.line1 = ""
        self.line2 = ""
        self.update()

    def clear(self):
        pass

    def write_lines(self, line1, line2):
        pass 

    def update(self):
        self.clear()
        clean_line1 = filter(lambda x: x in string.printable, self.line1)
        clean_line2 = filter(lambda x: x in string.printable, self.line2)
        line1_padded = clean_line1[:16].ljust(16)
        line2_padded = clean_line2[:16].ljust(16)
        self.write_lines(line1_padded, line2_padded)

    def set(self, line1, line2=""):
        if line1 != self.line1 or line2 != self.line2:
            self.line1 = line1
            self.line2 = line2
            self.update()
            

class PiLcdDisplay(BaseDisplay):

    def __init__(self, screen):
        self.ser = serial.Serial()
        self.ser.port = "/dev/ttyAMA0"
        self.ser.baudrate = 9600
        self.ser.open()
        super(PiLcdDisplay, self).__init__()

    def clear(self):
        self.ser.write("\xfe\x01")

    def write_lines(self, line1, line2):
        self.ser.write(line1 + line2)


class CursesDisplay(BaseDisplay):

    def __init__(self, screen):
        self.screen = screen
        super(CursesDisplay, self).__init__()

    def clear(self):
        self.screen.clear()

    def write_lines(self, line1, line2):
        self.screen.refresh()
        self.screen.addstr(2, 20, line1)
        self.screen.addstr(3, 20, line2)


if __name__ == "__main__":
    display = PiLcdDisplay()
    display.line1 = "Hello"
    display.line2 = "There"
    display.update()
