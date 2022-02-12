import unittest

class TestDoctor(unittest.TestCase):

    def test_issue_prescription(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        mock = self._mock_storage()
        doc = Doctor('','')
        ptn = Patient('','','')
        # doc will prescribe everything
        for i in range(0, len(Doctor._type)):
            self.assertIsNotNone(doc.issue_prescription(ptn))
        # verify that storage was called
        self.assertEqual(len(Doctor._type), mock.called_insert_prescription)
    
    def test_dont_issue_same_prescription_twice(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        mock = self._mock_storage(Doctor._type)
        doc = Doctor('','')
        ptn = Patient('','','')
        # doc won't prescribe anything more since patient already has everything
        self.assertIsNone(doc.issue_prescription(ptn))
        
    def test_consultation(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
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
        from healthcare.doctor import Doctor
        from healthcare.prescription import Prescription
        doc = Doctor('','')
        # doc will always approve
        self.assertTrue(doc.approve_repeat(Prescription('',None,None,0,0)))

    def test_patients(self):
        from healthcare.doctor import Doctor
        mock = self._mock_storage()
        doc = Doctor('','')
        # check against mock
        self.assertEqual(1, len(doc.patients()))
        self.assertTrue(mock.called_select_patients)

    def _mock_storage(self, prescriptions=[]):
        """utility that creates a mock of the Storage with predefined replies 
        to unit-test the class without the complexity of the db"""
        from healthcare.storage import Storage
        from healthcare.prescription import Prescription
        class MockStorage():
            def __init__(self) -> None:
                self.called_insert_prescription = 0
            def insert_prescription(self, prescription):
                self.called_insert_prescription = self.called_insert_prescription + 1

            def select_patients(self, doctor = None):
                from healthcare.patient import Patient
                self.called_select_patients = True
                return [Patient('', '', '')]
            
            def select_prescriptions(self, patient):
                return [Prescription(t,None,None,0,0) for t in prescriptions]
        Storage._instance = MockStorage()
        return Storage._instance

    @classmethod
    def tearDownClass(cls):
        from healthcare.storage import Storage
        Storage.reset()