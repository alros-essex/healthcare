from healthcare.storage import Storage
from .init_task import InitTask

class InitClinic(InitTask):
    def __init__(self):
        super().__init__(2, 'opening the clinic')

    def init(self):    
        self._notify('turning the lights on')
        self._notify('turning the lights on: done')

 