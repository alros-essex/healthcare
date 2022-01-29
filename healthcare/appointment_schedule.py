from collections import defaultdict
from datetime import date

class AppointmentSchedule():
    """
    Represents the schedule of the appointments
    """
    from .storage import Storage
    from .patient import Patient
    from .appointment import Appointment
    from .healthcare_professional import HealthcareProfessional

    def __init__(self, storage:Storage):
        """creates the instance
        
        Args:
            storage: db instance
        Returns:
            None
        """
        self._storage = storage
        # self._appoitments = defaultdict(lambda: defaultdict(lambda: None))

    @property
    def appointments(self):
        return self._storage.select_appointments()

    def add_appoitment(self, appointment:Appointment):
        """creates an appoitment
        
        Args:
            None
        Returns:
            None
        """
        self._storage.insert_appointment(appointment)
        #self._appoitments[appointment.staff.employee_number][appointment.date]=appointment

    def cancel_appoitment(self, appointment:Appointment):
        """deletes an appoitment
        
        Args:
            appointment: the appointment to delete
        Returns:
            None
        """
        self._storage.delete_appointment(appointment)
        # self._appoitments[appointment.staff.employee_number].pop(appointment.date)

    def find_appoitment(self, filter_professional:HealthcareProfessional=None, 
        filter_professionals=[], filter_date:date=None, filter_patient:Patient=None):
        """finds an appoitment
        
        Args:
            filter_professional: filter by healthcare professional (default None)
            filter_professionals: filter by list of healthcare professionals (default None)
            filter_date: filter by date
            filter_patient: filter by patient
        Returns:
            Appointment: dict of professional -> (dict of date -> appoitment)
        """
        employee_numbers_to_consider = [p.employee_number for p in self._merge_professional_filters(filter_professional, filter_professionals)] if filter_professional is not None or len(filter_professionals)>0 else None
        return self._storage.select_appointments(filter_patient=filter_patient, filter_employee_numbers=employee_numbers_to_consider, filter_date = filter_date)

    def _merge_professional_filters(self, filter_professional:HealthcareProfessional, filter_professionals):
        filter = []
        if filter_professional is not None:
            filter.append(filter_professional)
        filter = filter + filter_professionals
        return filter

    '''
    
    def _filter_by_date(self, professional_appointments, filter_date:date):
        return {k: v for k, v in professional_appointments.items() if v.is_on(filter_date)}

    def _filter_by_patient(self, professional_appointments, filter_patient:Patient):
        return {key:value for (key,value) in professional_appointments.items() if value is not None and value.patient == filter_patient}

    def _flatten(self, appoitments):
        return [app for cal in appoitments for k,app in cal.items() if app is not None]

    ''' 