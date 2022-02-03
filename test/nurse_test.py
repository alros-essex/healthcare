import unittest
from healthcare.nurse import Nurse
from healthcare.patient import Patient

class TestDoctor(unittest.TestCase):
        
    def test_consultation(self):
        nurse = Nurse('','')
        ptn = Patient('','','')

        # nurse will say something
        self.assertIsNotNone(nurse.consultation(ptn))
