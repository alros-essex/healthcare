from datetime import datetime
import unittest
from healthcare.appointment import Appointment
from healthcare.appointment_type import AppointmentType
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.receptionist import Receptionist
from healthcare.patient import Patient

class TestPatient(unittest.TestCase):

    def test_add_cancel_appointment(self):
        patient = Patient('','','')
        doctor = Doctor('','')
        date1 = datetime(2022,1,1,10,30)
        date2 = datetime(2022,2,2,10,30)

        self.assertEquals(0, len(patient.appointments))
        patient.add_appointment(Appointment(AppointmentType.NORMAL, doctor, patient, date1))
        patient.add_appointment(Appointment(AppointmentType.NORMAL, doctor, patient, date2))
        self.assertEquals(2, len(patient.appointments))
        patient.delete_appointment(Appointment(AppointmentType.NORMAL, doctor, patient, date1))
        self.assertEquals(1, len(patient.appointments))
        self.assertEquals(date2, patient.appointments[0].date)