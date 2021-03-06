import unittest
from healthcare.patient import Patient

class TestPatient(unittest.TestCase):

    def test_assigned_to_doctor(self):
        from healthcare.doctor import Doctor
        storage = self._mock_storage(Doctor('',''))
        patient = Patient('','','')
        # test against the mock
        self.assertIsNotNone(patient.doctor())
        self.assertTrue(storage.select_doctor_for_patient)

    def test_not_assigned_to_doctor(self):
        storage = self._mock_storage()
        patient = Patient('','','')
        # test against the mock
        self.assertIsNone(patient.doctor())
        self.assertTrue(storage.select_doctor_for_patient)

    def test_request_repeat(self):
        from healthcare.prescription import Prescription
        storage = self._mock_storage(prescriptions=[Prescription('',None, None, 0, 0)])
        doctor = self._mock_doctor()
        patient = Patient('','','')
        patient.request_repeat(doctor)
        # verify with the mock
        self.assertTrue(doctor.called_approve_repeat)

    def test_request_appointment_registered_patient(self):
        from healthcare.doctor import Doctor
        self._mock_storage(Doctor('',''))
        receptionist =self._mock_receptionist()
        patient = Patient('', '', '')
        # verify with mock
        patient.request_appointment(receptionist)
        self.assertTrue(receptionist._called_register_appointment)

    def test_unrequest_appointment_registered_patient(self):
        self._mock_storage(None)
        receptionist =self._mock_receptionist()
        patient = Patient('', '', '')
        # verify with mock
        patient.request_appointment(receptionist)
        # receptionist should also register the patient
        self.assertTrue(receptionist._called_register_patient)
        self.assertTrue(receptionist._called_register_appointment)

    def _mock_storage(self, patients_doctor=None, prescriptions=[]):
        """utility that creates a mock of the Storage with predefined replies 
        to unit-test the class without the complexity of the db"""
        from healthcare.storage import Storage
        class MockStorage():

            def select_doctor_for_patient(self, patient):
                self.select_doctor_for_patient = True
                return patients_doctor

            def select_prescriptions(self, patient):
                return prescriptions

        Storage._instance = MockStorage()
        return Storage._instance

    def _mock_doctor(self):
        """utility that creates a mock of the Doctor with predefined replies 
        to unit-test the class without the complexity of the doctor"""
        class MockDoctor():
            def approve_repeat(self, prescription):
                self.called_approve_repeat = True
                return True
        return MockDoctor()

    def _mock_receptionist(self):
        """utility that creates a mock of the Receptionist with predefined replies 
        to unit-test the class without the complexity of the receptionist"""
        class MockReceptionist():
            def propose_appointment(self, professional, patient, urgent, initial):
                from healthcare.appointment import Appointment
                return Appointment(None, None, None,None)
            def register_appointment(self,  appointment):
                self._called_register_appointment = True
            def find_available_doctors(self):
                from healthcare.doctor import Doctor
                return [Doctor('','')]
            def register_patient(self, patient, doctor):
                self._called_register_patient = True
        return MockReceptionist()

