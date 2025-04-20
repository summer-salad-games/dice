import logging
import time

logging.basicConfig(level=logging.INFO)


class Main:

    def __init__(self, init_delay=0, loop_delay=0):
        logging.info("Initializing program")

        self._init_delay = init_delay
        self._loop_delay = loop_delay

        time.sleep(self._init_delay)

    def _setup(self):
        logging.info("Setting up program")

    def _start_game(self):
        logging.info("Starting game")

    def _loop(self):
        time.sleep(self._loop_delay)

    def _exit(self):
        logging.info("Exiting program")

    def start(self):
        logging.info("Starting program")
        try:
            self._setup()
            time.sleep(self._init_delay)
            logging.info("Starting loop")
            while True:
                self._loop()
        except (KeyboardInterrupt, SystemExit):
            logging.info("Program interrupted")
        finally:
            self._exit()
