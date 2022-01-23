import random

from .appointment_schedule import AppointmentSchedule
from .employee import Employee
from .doctor import Doctor
from .nurse import Nurse
from .patient import Patient
from .receptionist import Receptionist

class Clinic():

    def __init__(self):
        self._staff = []
        self._patients = []
        self._appointment_schedule = AppointmentSchedule()
        self._name = 'Golden Oak Clinic'
        self._prescriptions = []
    
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

    def register_prescription(self, patient:Patient, doctor:Doctor, prescription:str):
        self._prescriptions.append(Prescription(patient, doctor, prescription))

    def call(self) -> Receptionist:
        receptionists = self.receptionists
        tot = len(receptionists)
        if tot == 0:
            return None
        else:
            return receptionists[random.randint(0, tot - 1)]

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

    @property
    def name(self):
        return self._name

    @property
    def appointment_schedule(self):
        return self._appointment_schedule

    def _get_by_type(self, type):
        return list(filter(lambda staff: isinstance(staff,type), self._staff))

class Prescription():
    def __init__(self, patient:Patient, doctor:Doctor, prescription:str) -> None:
        self._patient = patient
        self._doctor = doctor
        self._prescription = prescription