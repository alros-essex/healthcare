import unittest
from healthcare.doctor import Doctor
from healthcare.storage import Storage


class TestStorage(unittest.TestCase):

    def test_insert_select_doctor(self):
        storage = Storage()
        
        storage.insert_employee(Doctor('Who','DR1234'))
        doctors = storage.select_employee(employee_number = 'DR1234')

        self.assertEquals(1, len(doctors))
        self.assertEqual('Who', doctors[0].name)