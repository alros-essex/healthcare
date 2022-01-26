from datetime import datetime
import unittest
from healthcare.clinic import Clinic
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.receptionist import Receptionist

class TestReceptionist(unittest.TestCase):

    def test_round_initial_time_round_hours(self):
        r = Receptionist('','')
        
        before = r._round_initial_time(datetime(2022, 1, 21, 8, 28))
        self.assertEqual(datetime(2022, 1, 21, 8, 30), before, 'it was: {}'.format(before))

        after = r._round_initial_time(datetime(2022, 1, 21, 8, 38))
        self.assertEqual(datetime(2022, 1, 21, 9, 0), after, 'it was: {}'.format(after))

    def test_next_slot_next_same_day(self):
        r = Receptionist('','')

        next = r._next_slot(False, datetime(2022, 1, 27, 7, 0))

        self.assertEquals(datetime(2022, 1, 27, 9, 0), next)

    def test_next_slot_next_tomorrow(self):
        r = Receptionist('','')

        next = r._next_slot(False, datetime(2022, 1, 27, 17, 0))

        self.assertEquals(datetime(2022, 1, 28, 9, 0), next)

    def test_next_slot_skip_weekends(self):
        r = Receptionist('','')

        next = r._next_slot(False, datetime(2022, 1, 28, 19, 0))

        self.assertEquals(datetime(2022, 1, 31, 9, 0), next)