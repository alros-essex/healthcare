from abc import abstractmethod, ABC

from .event import Event
from .event_listener import EventListener
from .console import CONSOLE
from .console import ProgressBar
from .console import LOG
from .progress_bar import ProgressBar
from .healthcare import Healthcare
from .receptionist import Receptionist
from .doctor import Doctor
from .nurse import Nurse  

def main():
    """Entry point: call this method to start the application"""

    healthcare = Healthcare()

    init_steps = [
        InitClinic(),
        InitDoctors(),
        InitNurses(),
        InitReceptionists()
    ]
        
    for index, init_step in enumerate(init_steps):
        init_step.add_event_listener(ProgressBar(init_step.sub_steps_count, init_step.description, index))

    for init_step in init_steps:
        init_step.init(healthcare)

    
class InitStep(ABC):
    def __init__(self, sub_steps_count:int, description:str):
        self._sub_steps_count = sub_steps_count
        self._description = description

    @abstractmethod
    def init(self, healthcare:Healthcare):
        """Initialize the headthcare and update the progress bar

        Args:
            healthcare: healthcare to be initialized
        Returns:
            None
        """
        pass

    def add_event_listener(self, event_listener:EventListener):
        self._event_listener = event_listener

    @property
    def sub_steps_count(self):
        return self._sub_steps_count

    @property
    def description(self):
        return self._description

    def _notify(self, message:str):
        self._event_listener.notify(Event(message))

class InitClinic(InitStep):
    def __init__(self):
        super().__init__(2, 'opening the clinic')

    def init(self, healthcare:Healthcare):    
        self._notify('turning the lights on')
        self._notify('turning the lights on: done')

class InitHiringStaff(InitStep, ABC):
    def __init__(self):
        super().__init__(len(self._get_candidates_to_hire())+2, 'hiring {type_of_staff}'.format(type_of_staff = self._get_type_of_staff()))

    def init(self, healthcare:Healthcare):
        self._notify('looking for {type_of_staff}'.format(type_of_staff = self._get_type_of_staff()))
        for staff in self._get_candidates_to_hire():
            self._notify('hiring {name}'.format(name = staff.name))
            healthcare.hire(staff)
        self._notify('hiring {type_of_staff}: done'.format(type_of_staff = self._get_type_of_staff()))
    
    @abstractmethod
    def _get_type_of_staff(self):
        pass

    @abstractmethod
    def _get_candidates_to_hire(self):
        pass

class InitDoctors(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'doctors'

    def _get_candidates_to_hire(self):
        return [
            Doctor('James Kildare', 'DR001'),
            Doctor('Gregory House', 'DR002'),
            Doctor('Augustus Bedford "Duke" Forrest', 'DR003'),
            Doctor('Benjamin Franklin "Hawkeye" Pierce', 'DR004')
        ]
    
class InitNurses(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'nurses'

    def _get_candidates_to_hire(self):
        return [
            Nurse('Haleh Adams', 'NR001'),
            Nurse('Carla Espinosa', 'NR002'),
            Nurse('Rory Williams', 'NR003'),
            Nurse('Mildred Ratched', 'NR004')
        ]

class InitReceptionists(InitHiringStaff):
    def _get_type_of_staff(self):
        return 'receptionists'

    def _get_candidates_to_hire(self):
        return [
            Receptionist('Pam Beesly', 'RC001'),
            Receptionist('Randy Marsh', 'RC002')
        ]

