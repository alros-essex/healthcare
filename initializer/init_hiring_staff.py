from abc import ABC, abstractmethod
from .init_task import InitTask

class InitHiringStaff(InitTask, ABC):
    """initialize the staff with some employees, it must be extended by each employee-type"""

    def __init__(self, storage):
        super().__init__(self._get_candidates_to_hire_count()+2, 'hiring {type_of_staff}'.format(type_of_staff = self._get_type_of_staff()))
        self._storage = storage

    def init(self):
        self._notify('looking for {type_of_staff}'.format(type_of_staff = self._get_type_of_staff()))
        for staff in self._get_candidates_to_hire():
            self._notify('hiring {name}'.format(name = staff.name))
            self._storage.insert_employee(staff)
        self._notify('hiring {type_of_staff}: done'.format(type_of_staff = self._get_type_of_staff()))
    
    @abstractmethod
    def _get_type_of_staff(self):
        """template method: return 'doctor' or 'nurse'"""
        pass

    @abstractmethod
    def _get_candidates_to_hire(self):
        """template method: return a list of employees"""
        pass

    @abstractmethod
    def _get_candidates_to_hire_count(self) -> int:
        """how many candidates: this is to fill the progress bar"""
        pass