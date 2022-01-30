from datetime import datetime
import unittest
from healthcare.appointment import Appointment
from healthcare.appointment_type import AppointmentType
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.prescription import Prescription
from healthcare.receptionist import Receptionist
from healthcare.patient import Patient
from healthcare.storage import Storage

class TestPrescription(unittest.TestCase):

    def test_db(self):
        storage = Storage()
        patient1 = Patient('John', '', '')
        patient2 = Patient('Jane', '', '')
        doctor = Doctor('Who', 'DR1234')

        storage.insert_prescription(Prescription('AAA', patient1, doctor, 10, 11.11))
        storage.insert_prescription(Prescription('BBB', patient1, doctor, 10, 11.11))
        storage.insert_prescription(Prescription('CCC', patient2, doctor, 20, 22.22))

        prescriptions = storage.select_prescriptions(patient1)
        self.assertEquals(2, len(prescriptions))
        prescription:Prescription = prescriptions[0]
        self.assertEquals(11.11, prescription.dosage)