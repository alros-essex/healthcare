from .employee import Employee
from .doctor import Doctor
from .nurse import Nurse
from .patient import Patient
from .receptionist import Receptionist

class Clinic():

    def __init__(self):
        self._staff = []
        self._patients = []
    
    def hire(self, employee:Employee):
        self._staff.append(employee)
        # TODO add validation
        return True, None

    def fire(self, employee_number:str, type):
        employee = next(filter(lambda e: e.employee_number == employee_number, self._staff), None)
        if employee is None:
            return False, 'Employee number {} not found'.format(employee_number)
        elif not isinstance(employee, type):
            return False, 'Employee number {} is not a {}'.format(employee_number, type.__name__)
        else:
            self._staff.remove(employee)
            return True, None

    def register_patient(self, patient:Patient):
        self._patients.append(patient)

    @property
    def doctors(self):
        return self._get_by_type(Doctor)

    @property
    def nurses(self):
        return self._get_by_type(Nurse)

    @property
    def receptionists(self):
        return self._get_by_type(Receptionist)

    @property
    def patients(self):
        return sorted(self._patients)

    def _get_by_type(self, type):
        return list(filter(lambda staff: isinstance(staff,type), self._staff))

    