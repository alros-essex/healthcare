from datetime import datetime
from pydoc import Doc
import unittest
from healthcare.appointment import Appointment
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.patient import Patient
from healthcare.receptionist import Receptionist

class TestReceptionist(unittest.TestCase):
    '''
    def flow_with_patient(self):
        storage = Storage()
        doctor = Doctor('Who', 'TRDS123')
        schedule = AppointmentSchedule(storage)
        r = Receptionist('','',schedule, storage)

        patient = Patient('John Test', 'Somewhere, 4, NY', '5555-1234')
        r.register_patient(patient)
        appointment = r.propose_appointment(doctor, patient, False, datetime(2022, 1, 28, 8, 0))
        r.register_appointment(appointment)

        reloadedPatient = storage.select_patient('John Test')
        self.assertEquals(patient, reloadedPatient)
    '''

    def test_register_appointment(self):
        schedule = self._mock_schedule()
        receptionist = Receptionist('','')
        # verify with mock
        receptionist.register_appointment(Appointment(None, None, None, None))
        self.assertTrue(schedule._called_add_appoitment)

    def test_cancel_appointment(self):
        schedule = self._mock_schedule()
        receptionist = Receptionist('','')
        # verify with mock
        receptionist.cancel_appointment(Appointment(None, None, None, None))
        self.assertTrue(schedule._called_cancel_appoitment)

    def test_propose_appointment(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        self._mock_schedule()
        receptionist = Receptionist('','')
        doctor = Doctor('','')
        patient = Patient('','','')
        # verify with mock
        self.assertIsNotNone(receptionist.propose_appointment(doctor, patient, True, datetime(2022, 1, 1, 10, 30)))

    def test_lookup_patient(self):
        self._mock_storage()
        receptionist = Receptionist('','')
        # verify with mock
        self.assertIsNotNone(receptionist.lookup_patient('name'))
        
    def test_find_available_doctors(self):
        self._mock_storage()
        receptionist = Receptionist('','')
        # verify with mock
        self.assertEqual(1, len(receptionist.find_available_doctors()))

    def test_register_patient(self):
        from healthcare.patient import Patient
        from healthcare.doctor import Doctor
        storage = self._mock_storage()
        receptionist = Receptionist('','')
        # verify with mock
        receptionist.register_patient(Patient('','',''), Doctor('',''))
        self.assertTrue(storage._called_associate_doctor_patient)
        self.assertTrue(storage._called_insert_patient)

    def test_find_patient_appointments(self):
        from healthcare.patient import Patient
        schedule = self._mock_schedule()
        receptionist = Receptionist('','')
        # verify with mock
        self.assertEqual(1, len(receptionist.find_patient_appointments(Patient('','',''))))

    def _mock_storage(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        from healthcare.storage import Storage
        class MockStorage():
            def select_patient(self, name):
                return Patient('','','')
            def select_doctors(self, employee_number=None, max_patients=None):
                return [Doctor('','')]
            def insert_patient(self, patient):
                self._called_insert_patient = True
            def associate_doctor_patient(self, doctor, patient):
                self._called_associate_doctor_patient = True
        Storage._instance = MockStorage()
        return Storage._instance

    def _mock_schedule(self):
        from healthcare.appointment_schedule import AppointmentSchedule
        from healthcare.appointment import Appointment
        class MockAppointmentSchedule():
            def add_appoitment(self, appointment):
                self._called_add_appoitment = True
            def cancel_appoitment(self, appointment):
                self._called_cancel_appoitment = True
            def find_appointments(self, filter_professional=None, 
                filter_professionals=[], filter_date=None, filter_patient=None):
                from healthcare.appointment import Appointment
                return [Appointment(None, None, None, None)]
            def find_next_available(self, professional, patient, urgent, initial):
                return Appointment(None, None, None, None)
        AppointmentSchedule._instance = MockAppointmentSchedule()
        return AppointmentSchedule._instance

    