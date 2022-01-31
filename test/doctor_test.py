from datetime import datetime
import unittest
from healthcare.appointment import Appointment
from healthcare.appointment_type import AppointmentType
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.receptionist import Receptionist
from healthcare.patient import Patient
from healthcare.storage import Storage

class TestDoctor(unittest.TestCase):

    def test_issue_prescription(self):
        doc = Doctor('','', Storage())
        ptn = Patient('','','')

        self.assertEquals(0, len(ptn.prescriptions))
        for i in range(0, len(doc._type)):
            self.assertIsNotNone(doc.issue_prescription(ptn))
            self.assertEquals(i+1, len(ptn.prescriptions))
        
        self.assertIsNone(doc.issue_prescription(ptn))
        self.assertEquals(len(ptn.prescriptions), len(ptn.prescriptions))
        