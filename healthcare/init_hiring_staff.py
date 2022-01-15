from abc import ABC, abstractmethod
from .healthcare import Healthcare
from .init_task import InitTask

class InitHiringStaff(InitTask, ABC):
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
