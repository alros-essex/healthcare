from datetime import datetime, timedelta

from .appointment_schedule import AppointmentSchedule
from .appointment_type import AppointmentType
from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional
from .storage import Storage
from .employee import Employee
from .employee_role import EmployeeRole
from .patient import Patient


class Receptionist(Employee):
    """models a receptionist"""

    def __init__(self, name: str, employee_number: str, schedule:AppointmentSchedule = None, storage:Storage = None):
        """creates the instance
        
        Args:
            name: employee's name
            employee_number: employee's number
            schedule: instance of AppointmentSchedule (optional)
            storage: instance of Storage (optional)
        Returns:
            None
        """
        super().__init__(name, employee_number)
        self._schedule = schedule
        self._storage = storage

    @property
    def role(self) -> EmployeeRole:
        return EmployeeRole.RECEPTIONIST

    # TODO try to remove it
    def connect_to_schedule(self, schedule:AppointmentSchedule) -> None:
        """the receptionist needs access to the schedule to manage appointments
        
        Args:
            schedule: AppointmentSchedule
        Returns:
            None
        """
        self._schedule = schedule
    
    # TODO try to remove it
    def connect_to_storage(self, storage:Storage) -> None:
        """the receptionist needs access to the storage to manage the patients
        
        Args:
            storage: Storage
        Returns:
            None
        """
        self._storage = storage

    def register_appointment(self,  appointment:Appointment) -> None:
        """stores an appointment
        
        Args:
            appointment: Appointment to be saved
        Returns:
            None
        """
        self._schedule.add_appoitment(appointment)
        appointment.patient.add_appointment(appointment)

    def cancel_appointment(self, appointment:Appointment) -> None:
        """cancels an appointment
        
        Args:
            appointment: Appointment to be cancelled
        Returns:
            None
        """
        self._schedule.cancel_appoitment(appointment)

    def lookup_patient(self, first_name:str, surname:str) -> Patient:
        """finds the record of a Patient
        
        Args:
            first_name: patient's first name
            surname: patient's surname
        returns:
            Patient or None
        """
        return self._storage.select_patient(first_name=first_name, surname=surname)

    def register_patient(self, patient:Patient) -> None:
        """register a patient
        
        Args:
            patient: Patient to be registered
        Returns:
            None
        """
        self._storage.insert_patient(patient)

    # TODO remove
    def find_patient_appointments(self, patient:Patient):
        return self._schedule.find_appoitments(filter_patient=patient)

    def propose_appointment(self, professional:HealthcareProfessional, patient:Patient, urgent:bool, initial:datetime) -> Appointment:
        """creates a potential appointment
        
        Args:
            professional: HealthcareProfessional
            patient: Patient
            urgent: True to use also urgent-only timeslots
            initial: datetime with the earliest moment

        Returns:
            Appointment (not saved)
        """
        return self._schedule.find_next_available(professional, patient, urgent, initial)