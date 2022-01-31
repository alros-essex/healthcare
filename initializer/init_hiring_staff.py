from abc import ABC, abstractmethod

from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.storage import Storage

from .init_task import InitTask

class InitHiringStaff(InitTask, ABC):
    def __init__(self, storage:Storage, schedule:AppointmentSchedule):
        super().__init__(self._get_candidates_to_hire_count()+2, 'hiring {type_of_staff}'.format(type_of_staff = self._get_type_of_staff()))
        self._storage = storage
        self._schedule = schedule

    def init(self):
        self._notify('looking for {type_of_staff}'.format(type_of_staff = self._get_type_of_staff()))
        for staff in self._get_candidates_to_hire(self._storage, self._schedule):
            self._notify('hiring {name}'.format(name = staff.name))
            self._storage.insert_employee(staff)
        self._notify('hiring {type_of_staff}: done'.format(type_of_staff = self._get_type_of_staff()))
    
    @abstractmethod
    def _get_type_of_staff(self):
        pass

    @abstractmethod
    def _get_candidates_to_hire(self, storage:Storage):
        pass

    @abstractmethod
    def _get_candidates_to_hire_count(self) -> int:
        pass