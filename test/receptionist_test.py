from datetime import datetime
import unittest
from healthcare.clinic import Clinic
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.receptionist import Receptionist

class TestHealthcare(unittest.TestCase):

    def test_round_hours(self):
        r = Receptionist('','')
        
        before = r._round_initial_time(datetime(2022, 1, 21, 8, 28))
        self.assertEqual(datetime(2022, 1, 21, 8, 30), before, 'it was: {}'.format(before))

        after = r._round_initial_time(datetime(2022, 1, 21, 8, 38))
        self.assertEqual(datetime(2022, 1, 21, 9, 0), after, 'it was: {}'.format(after))