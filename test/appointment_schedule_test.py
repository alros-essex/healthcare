from datetime import timedelta
import unittest

from healthcare.appointment_schedule import AppointmentSchedule

class TestAppointmentSchedule(unittest.TestCase):

    def test_appointments(self):
        from healthcare.appointment import Appointment
        storage = self._mock_storage([Appointment(None, None, None, None)])
        schedule = AppointmentSchedule(storage)
        # test with mock
        self.assertEqual(1, len(schedule.appointments))

    def test_add_appoitment(self):
        from healthcare.appointment import Appointment
        storage = self._mock_storage()
        schedule = AppointmentSchedule(storage)
        # test with mock
        schedule.add_appoitment(Appointment(None, None, None, None))
        self.assertTrue(storage._called_insert_appointment)

    def test_cancel_appoitment(self):
        from healthcare.appointment import Appointment
        storage = self._mock_storage()
        schedule = AppointmentSchedule(storage)
        # test with mock
        schedule.cancel_appoitment(Appointment(None, None, None, None))
        self.assertTrue(storage._called_delete_appointment)

    def test_find_next_available(self):
        from datetime import datetime
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        storage = self._mock_storage()
        schedule = AppointmentSchedule(storage)
        doctor = Doctor('','')
        patient = Patient('','','')
        # if patients calls before opening time between Mon-Fri, appointments should be on the same day at opening time for urgency
        appointment = schedule.find_next_available(doctor, patient, True, datetime(2022, 1, 19, 5, 15))
        self.assertEqual(datetime(2022, 1, 19, 8, 0), appointment.date)
        # if patients calls before opening time between Mon-Fri, appointments should be on the same day at normal opening time
        appointment = schedule.find_next_available(doctor, patient, False, datetime(2022, 1, 19, 5, 15))
        self.assertEqual(datetime(2022, 1, 19, 9, 0), appointment.date)
        # if patients calls after opening time between Mon-Fri, appointments should be on the same day at the next slot of 30 minutes after the current one
        appointment = schedule.find_next_available(doctor, patient, False, datetime(2022, 1, 19, 10, 31))
        self.assertEqual(datetime(2022, 1, 19, 11, 30), appointment.date)
        # if patients calls after closing time between Mon-Fri, appointments should be on the next day at opening time
        appointment = schedule.find_next_available(doctor, patient, False, datetime(2022, 1, 19, 15, 31))
        self.assertEqual(datetime(2022, 1, 20, 9, 0), appointment.date)
        # if patients calls after closing time on Fri, appointments should be on the next Monday
        appointment = schedule.find_next_available(doctor, patient, False, datetime(2022, 1, 21, 15, 31))
        self.assertEqual(datetime(2022, 1, 24, 9, 0), appointment.date)

    def test_find_next_appointment(self):
        from datetime import datetime
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        storage = self._mock_storage()
        schedule = AppointmentSchedule(storage)
        doctor = Doctor('','')
        patient = Patient('','','')
        appointments = []
        storage.set_return_select_appointments(appointments)
        expected_datetime = datetime(2022, 1, 19, 8, 0)

        # check how appointments are scheduled during a single day
        for i in range(0, 14):
            appointment = schedule.find_next_available(doctor, patient, True, datetime(2022, 1, 19, 5, 15))
            self.assertEqual(expected_datetime, appointment.date)
            appointments.append(appointment)
            expected_datetime = expected_datetime + timedelta(minutes=30)

        # until the overflow to next day
        appointment = schedule.find_next_available(doctor, patient, True, datetime(2022, 1, 19, 5, 15))
        self.assertEqual(datetime(2022, 1, 20, 8, 0), appointment.date)
        appointments.append(appointment)

    def test_find_appointments(self):
        from datetime import date, datetime
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        storage = self._mock_storage()
        schedule = AppointmentSchedule(storage)
        # vefify filters in the query
        schedule.find_appointments(
            filter_professional=Doctor('','1'), 
            filter_professionals=[Doctor('','2'), Doctor('','3')],
            filter_date=date(2022, 1, 20),
            filter_patient=Patient('4','',''))
        # values are stored in the mock
        self.assertEqual(storage._called_select_appointments['filter_employee_numbers'],['1','2','3'])
        self.assertEqual(storage._called_select_appointments['filter_date'],date(2022, 1, 20))
        self.assertEqual(storage._called_select_appointments['filter_patient'],Patient('4','',''))

    def find_dates_with_appointments(self):
        storage = self._mock_storage()
        schedule = AppointmentSchedule(storage)
        # verify with mock
        schedule.find_dates_with_appointments()
        self.assertTrue(storage._called_select_appointment_dates)

    def _mock_storage(self, appointments = []):
        from healthcare.appointment import Appointment
        from healthcare.storage import Storage
        class MockStorage():
            def __init__(self) -> None:
                self._return_select_appointments = appointments
            def select_appointments(self, filter_employee_numbers=[], filter_date=None, filter_patient=None):
                return [Appointment(None, None, None, None)]
            def insert_appointment(self, appointment):
                self._called_insert_appointment = True
            def delete_appointment(self, appointment):
                self._called_delete_appointment = True
            def select_appointments(self, filter_employee_numbers=[], filter_date=None, filter_patient=None):
                self._called_select_appointments={
                    'filter_employee_numbers': filter_employee_numbers,
                    'filter_date': filter_date,
                    'filter_patient': filter_patient
                }
                return self._return_select_appointments
            def select_appointment_dates(self):
                self._called_select_appointment_dates = True
            def set_return_select_appointments(self, appointments):
                self._return_select_appointments = appointments
        Storage._instance = MockStorage()
        return Storage._instance

    @classmethod
    def tearDownClass(cls):
        from healthcare.storage import Storage
        Storage.reset()