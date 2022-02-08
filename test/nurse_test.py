import unittest

class TestDoctor(unittest.TestCase):
        
    def test_consultation(self):
        from healthcare.nurse import Nurse
        from healthcare.patient import Patient
        nurse = Nurse('','')
        ptn = Patient('','','')

        # nurse will say something
        self.assertIsNotNone(nurse.consultation(ptn))
