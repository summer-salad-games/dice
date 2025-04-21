import logging
from random import randint
from signal import pause
from time import sleep

from gpiozero import Button, OutputDevice

logging.basicConfig(level=logging.INFO)


class Main:

    _BLANK = 0xFF
    _NUMBERS = [0x11, 0xD7, 0x32, 0x92, 0xD4, 0x98, 0x18, 0xD3, 0x10, 0x90]

    def __init__(
        self, init_delay=1, loop_delay=0.025, data_pin=17, latch_pin=27, clock_pin=22
    ):
        logging.info("Initializing program")

        self._is_loading = True
        self._init_delay = init_delay
        self._loop_delay = loop_delay

        self._data_pin = OutputDevice(data_pin)
        self._latch_pin = OutputDevice(latch_pin)
        self._clock_pin = OutputDevice(clock_pin)

        self._button = Button(5, bounce_time=0.1)

        sleep(self._init_delay)

    def _setup(self):
        logging.info("Setting up program")
        self._reset()

        self._button.when_activated = lambda: self._button_event(True)
        self._button.when_deactivated = lambda: self._button_event(False)
        self._is_loading = False

    def _loop(self):
        sleep(self._loop_delay)

    def _exit(self):
        logging.info("Exiting program")
        self._reset()

    def _reset(self):
        logging.info("Resetting program")
        self._clear_screen()
        self._data_pin.off()
        self._latch_pin.off()
        self._clock_pin.off()
        self._is_loading = False

    def _clear_screen(self):
        self._shift_out(self._BLANK)

    def _shift_out(self, data):
        sleep(0.01)
        self._latch_pin.off()
        for i in range(8):
            if (data >> i) & 0b1:
                self._data_pin.on()
            else:
                self._data_pin.off()

            self._clock_pin.on()
            sleep(0.01)
            self._clock_pin.off()

        sleep(0.01)
        self._latch_pin.on()
        sleep(0.01)
        self._latch_pin.off()
        sleep(0.01)

    def _show_number(self, number):
        if number < 0 or number > 9:
            self._clear_screen()
        else:
            self._shift_out(self._NUMBERS[number])

    def _button_event(self, pressed):
        if pressed and not self._is_loading:
            logging.info(f"Button pressed: {pressed}")
            self._is_loading = True
            number = randint(0, 9)
            logging.info(f"Chosen number: {number}")

            delay = 0.005
            for i in range(9):
                temporary_number = randint(0, 9)
                self._show_number(temporary_number)
                sleep(delay)
                delay += delay

            for i in range(5):
                self._show_number(number)
                sleep(0.5)
                self._clear_screen()
                sleep(0.5)

            self._show_number(number)
            self._is_loading = False

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
