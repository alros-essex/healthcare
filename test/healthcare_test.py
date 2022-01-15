import unittest
from healthcare.clinic import Clinic
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.receptionist import Receptionist

class TestHealthcare(unittest.TestCase):

    def test_hire_staff(self):
        doctors = [
            Doctor('John Doe', 'D1'),
            Doctor('Jane Doe', 'D2')
        ]
        nurses = [
            Nurse('Martin Doe', 'N1'),
            Nurse('Martina Doe', 'N2')
        ]
        receptionists = [
            Receptionist('Tim Doe', 'R01'),
            Receptionist('Tina Doe', 'R02')
        ]
        clinic = Clinic()
        
        for doctor in doctors:
            clinic.hire(doctor)
        for nurse in nurses:
            clinic.hire(nurse)
        for receptionist in receptionists:
            clinic.hire(receptionist)

        self.assertEqual(doctors, clinic.get_doctors())
        self.assertEqual(nurses, clinic.get_nurse())
        self.assertEqual(receptionists, clinic.get_receptionist())

if __name__ == '__main__':
    unittest.main()