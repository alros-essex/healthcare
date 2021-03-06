from datetime import datetime

class Appointment():
    """
    Represents an appointment
    """
    def __init__(self, type, staff, patient, date:datetime):
        """creates the instance
        
        Args:
            type: AppointmentType
            staff: member of staff who will receive the patient
            patient: Patient who booked the appoitment
            date: datetime of the appointment
        Returns:
            None
        """
        self._type = type
        self._staff = staff
        self._patient = patient
        self._date = date

    @property
    def type(self):
        return self._type

    @property
    def staff(self):
        return self._staff

    @property
    def patient(self):
        return self._patient

    @property
    def date(self) -> datetime:
        return self._date

    def is_on(self, filter_date:datetime.date) -> bool:
        """compares with a date
        
        Args:
            filter_date: a date
        Returns:
            True if the appointment is on filter_date
        """
        return self.date.year == filter_date.year and self.date.month == filter_date.month and self.date.day == filter_date.day

    def __lt__(self, other) -> bool:
        return self.date < other.date
    
    def __le__(self, other) -> bool:
        return self.date <= other.date

    def __eq__(self, other) -> bool:
        return self.date == other.date and self.staff == other.staff and self.patient == other.patient
    
    def __ne__(self, other) -> bool:
        return self.date != other.date
    
    def __gt__(self, other) -> bool:
        return self.date > other.date
    
    def __ge__(self, other) -> bool:
        return self.date >= other.date

    def __str__(self) -> str:
        return "{staff} with {patient} - {date}".format(
            staff=self.staff,patient=self.patient,date=self.date,type=self.type)