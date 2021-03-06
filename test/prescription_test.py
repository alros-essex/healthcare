from datetime import datetime
import unittest

class TestPrescription(unittest.TestCase):

    def test_db(self):
        from healthcare.doctor import Doctor
        from healthcare.prescription import Prescription
        from healthcare.patient import Patient
        storage = self._get_storage()
        patient1 = Patient('John', '', '')
        patient2 = Patient('Jane', '', '')
        doctor = Doctor('Who', 'DR1234')

        storage.insert_prescription(Prescription('AAA', patient1, doctor, 10, 11.11))
        storage.insert_prescription(Prescription('BBB', patient1, doctor, 10, 11.11))
        storage.insert_prescription(Prescription('CCC', patient2, doctor, 20, 22.22))

        prescriptions = storage.select_prescriptions(patient1)
        self.assertEqual(2, len(prescriptions))
        prescription:Prescription = prescriptions[0]
        self.assertEqual(11.11, prescription.dosage)

    def _get_storage(self):
        from healthcare.storage import Storage
        Storage.reset()
        return Storage.instance()

    @classmethod
    def tearDownClass(cls):
        from healthcare.storage import Storage
        Storage.reset()