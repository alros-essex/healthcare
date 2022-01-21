from healthcare.clinic import Clinic
from .init_task import InitTask

class InitClinic(InitTask):
    def __init__(self):
        super().__init__(2, 'opening the clinic')

    def init(self, healthcare:Clinic):    
        self._notify('turning the lights on')
        self._notify('turning the lights on: done')

 