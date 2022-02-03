import unittest
from healthcare.doctor import Doctor
from healthcare.patient import Patient
from healthcare.storage import Storage

class TestDoctor(unittest.TestCase):

    def test_issue_prescription(self):
        mock = self._mock_storage()
        doc = Doctor('','')
        ptn = Patient('','','')

        # no initial prescriptions
        self.assertEquals(0, len(ptn.prescriptions))
        # doc will prescribe everything
        for i in range(0, len(doc._type)):
            self.assertIsNotNone(doc.issue_prescription(ptn))
            self.assertEquals(i+1, len(ptn.prescriptions))
        
        # doc won't prescribe anything more since patient already has everything
        self.assertIsNone(doc.issue_prescription(ptn))
        self.assertEquals(len(ptn.prescriptions), len(ptn.prescriptions))
        # verify that storage was called
        self.assertTrue(mock.called_insert_prescription)
        
    def test_consultation(self):
        mock = self._mock_storage()
        doc = Doctor('','')
        ptn = Patient('','','')

        # doc will say something
        self.assertIsNotNone(doc.consultation(ptn))
        # doc always prescribe something to a patient without prescriptions
        self.assertIsNotNone(ptn.prescriptions)
        # verify that storage was called
        self.assertTrue(mock.called_insert_prescription)

    def test_approve_repeat(self):
        from healthcare.prescription import Prescription
        doc = Doctor('','')
        # doc will always approve
        self.assertTrue(doc.approve_repeat(Prescription('',None,None,0,0)))

    def test_patients(self):
        mock = self._mock_storage()
        doc = Doctor('','')
        # check against mock
        self.assertEquals(1, len(doc.patients()))
        self.assertTrue(mock.called_select_patients)

    def _mock_storage(self):
        class MockStorage():

            def insert_prescription(self, prescription):
                self.called_insert_prescription = True

            def select_patients(self, doctor = None):
                from healthcare.patient import Patient
                self.called_select_patients = True
                return [Patient('', '', '')]
        Storage._instance = MockStorage()
        return Storage._instance