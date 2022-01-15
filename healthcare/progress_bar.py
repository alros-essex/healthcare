from tqdm import tqdm
import time
from healthcare.event import Event

from healthcare.event_listener import EventListener

class ProgressBar(EventListener):

    _PAUSE = 0.5

    def __init__(self, steps:int, init_message:str, row:int, padding:int=50):
        self._bar = tqdm(range(0, steps), position=row)
        self._init_message = init_message
        self._padding = padding
        self._update_description(init_message)

    def notify(self, event:Event):
        self._tick(event.description)
    
    def _tick(self, message:str):
        time.sleep(ProgressBar._PAUSE)
        self._bar.update()
        self._update_description(message)

    def _update_description(self, message):
        self._bar.set_description(message.rjust(self._padding))