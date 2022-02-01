from datetime import datetime, timedelta
from healthcare.doctor import Doctor
from .appointment_type import AppointmentType
from .appointment import Appointment
from .healthcare_professional import HealthcareProfessional
from .employee import Employee
from .employee_role import EmployeeRole
from .patient import Patient


class Receptionist(Employee):
    """models a receptionist"""

    _max_patients_per_doctor = 500

    def __init__(self, name: str, employee_number: str):
        """creates the instance
        
        Args:
            name: employee's name
            employee_number: employee's number
        Returns:
            None
        """
        super().__init__(name, employee_number)
        from .appointment_schedule import AppointmentSchedule
        self._schedule = AppointmentSchedule.instance()
        from .storage import Storage
        self._storage = Storage.instance()

    @property
    def role(self) -> EmployeeRole:
        return EmployeeRole.RECEPTIONIST

    def register_appointment(self,  appointment:Appointment) -> None:
        """stores an appointment
        
        Args:
            appointment: Appointment to be saved
        Returns:
            None
        """
        self._schedule.add_appoitment(appointment)

    def cancel_appointment(self, appointment:Appointment) -> None:
        """cancels an appointment
        
        Args:
            appointment: Appointment to be cancelled
        Returns:
            None
        """
        self._schedule.cancel_appoitment(appointment)

    def lookup_patient(self, name:str) -> Patient:
        """finds the record of a Patient
        
        Args:
            name: patient's name
        returns:
            Patient or None
        """
        return self._storage.select_patient(name)

    def find_available_doctors(self):
        """returns the list of doctors with less than 500 patients
        
        Args:
            None
        returns:
            array of Doctor
        """
        return self._storage.select_doctors(max_patients = Receptionist._max_patients_per_doctor)

    def register_patient(self, patient:Patient, doctor) -> None:
        """register a patient
        
        Args:
            patient: Patient to be registered
            doctor: Doctor for the patient
        Returns:
            None
        """
        self._storage.insert_patient(patient)
        self._storage.associate_doctor_patient(doctor, patient)

    def find_patient_appointments(self, patient:Patient):
        return self._schedule.find_appointments(filter_patient=patient)

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