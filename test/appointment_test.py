from datetime import datetime,date
import unittest

class TestAppointment(unittest.TestCase):

    def test_is_on(self):
        from healthcare.appointment import Appointment
        from healthcare.appointment_type import AppointmentType
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        appointment = Appointment(
            AppointmentType.NORMAL, 
            Doctor('',''), 
            Patient('','',''), 
            datetime(2022,1,1,10,30))
        # verify is on the right date
        self.assertTrue(appointment.is_on(date(2022,1,1)))
        self.assertFalse(appointment.is_on(date(2022,1,2)))