import unittest
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.patient import Patient
from healthcare.storage import Storage


class TestStorage(unittest.TestCase):

    def test_insert_select_doctor(self):
        storage = Storage()
        
        storage.insert_employee(Doctor('Who','DR1234'))
        doctors = storage.select_employee(employee_number = 'DR1234')

        self.assertEquals(1, len(doctors))
        self.assertEqual('Who', doctors[0].name)

    def test_insert_select_nurse_from_group(self):
        storage = Storage()
        
        storage.insert_employee(Doctor('Who','DR1234'))
        storage.insert_employee(Nurse('Pond','NR1111'))
        storage.insert_employee(Nurse('Song','NR2222'))
        storage.insert_employee(Nurse('Clara','NR3333'))
        nurses = storage.select_employee(employee_number = 'NR2222')

        self.assertEquals(1, len(nurses))
        self.assertEqual('Song', nurses[0].name)

    def test_insert_select_patient(self):
        storage = Storage()

        storage.insert_patient(Patient('John', 'Doe', 'Nowhere st. 0', '+0 1111 0000'))
        patient = storage.select_patient('John', 'Doe')

        self.assertEquals('John', patient.firstname)
        self.assertEquals('Doe', patient.surname)
        self.assertEquals('Nowhere st. 0', patient.address)
        self.assertEquals('+0 1111 0000', patient.phone)