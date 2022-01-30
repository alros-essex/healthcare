from datetime import datetime
import unittest
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.patient import Patient
from healthcare.receptionist import Receptionist
from healthcare.storage import Storage

class TestReceptionist(unittest.TestCase):
    
    def flow_with_patient(self):
        storage = Storage()
        doctor = Doctor('Who', 'TRDS123')
        schedule = AppointmentSchedule(storage)
        r = Receptionist('','',schedule, storage)

        patient = Patient('John Test', 'Somewhere, 4, NY', '5555-1234')
        r.register_patient(patient)
        appointment = r.propose_appointment(doctor, patient, False, datetime(2022, 1, 28, 8, 0))
        r.register_appointment(appointment)

        reloadedPatient = storage.select_patient('John Test')
        self.assertEquals(patient, reloadedPatient)