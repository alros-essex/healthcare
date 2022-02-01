from datetime import datetime
import unittest

class TestPatient(unittest.TestCase):

    def test_request_appointment_unregistered_patient(self):
        from healthcare.receptionist import Receptionist
        from healthcare.patient import Patient
        from healthcare.doctor import Doctor
        from healthcare.storage import Storage

        Storage.reset()
        storage = Storage.instance()

        p = Patient('John', '', '')
        r = Receptionist('Jane', 'R123')
        
        storage.insert_employee(Doctor('White','DR1'))
        storage.insert_employee(Doctor('Black','DR2'))

        p.request_appointment(r)

        self.assertIsNotNone(storage.select_doctor_for_patient(p))
        self.assertIsNotNone(storage.select_appointments(filter_patient=p))