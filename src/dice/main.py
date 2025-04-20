import logging
from time import sleep
from signal import pause
from gpiozero import OutputDevice, Button
from random import randint

logging.basicConfig(level=logging.INFO)


class Main:
    
    _BLANK = 0xFF
    _NUMBERS = [0x11, 0xD7, 0x32, 0x92, 0xD4, 0x98, 0x18, 0xD3, 0x10, 0x90]

    def __init__(self, init_delay=1, loop_delay=0.025, data_pin=17, latch_pin=27, clock_pin=22):
        logging.info("Initializing program")

        self._init_delay = init_delay
        self._loop_delay = loop_delay

        self.dataPin = OutputDevice(data_pin)
        self.latchPin = OutputDevice(latch_pin)
        self.clockPin = OutputDevice(clock_pin)

        sleep(self._init_delay)

    def _setup(self):
        logging.info("Setting up program")
        self._reset()

        self._button = Button(5, bounce_time=0.1)
        self._button.when_activated = lambda: self._button_event(True)
        self._button.when_deactivated = lambda: self._button_event(False)
        
    def _loop(self):
        sleep(self._loop_delay)

    def _exit(self):
        logging.info("Exiting program")
        self._reset()

    def _reset(self):
        logging.info("Resetting program")
        self._shift_out(0xFF)
        self.dataPin.off()
        self.latchPin.off()
        self.clockPin.off()

    def _shift_out(self, data):
        sleep(0.01)
        self.latchPin.off()
        for i in range(8):
            if (data >> i) & 0b1:
                self.dataPin.on()
            else:
                self.dataPin.off()
        
            self.clockPin.on()
            sleep(0.01)
            self.clockPin.off()

        sleep(0.01)
        self.latchPin.on()
        sleep(0.01)
        self.latchPin.off()
        sleep(0.01)

    def _show_number(self, number):
        if number < 0 or number > 9:
            self._shift_out(self._BLANK)
        else:
            self._shift_out(self._NUMBERS[number])

    def _button_event(self, pressed):
        logging.info(f"Button pressed: {pressed}")
        if pressed:
            number = randint(0, 9)
            logging.info(f"Showing number: {number}")
            self._show_number(number)

    def start(self):
        logging.info("Starting program")
        try:
            self._setup()
            sleep(self._init_delay)
            logging.info("Starting loop")
            while True:
                self._loop()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Program interrupted")
        finally:
            self._exit()
