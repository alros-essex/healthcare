from datetime import datetime
import unittest
from healthcare.appointment import Appointment
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.doctor import Doctor
from healthcare.patient import Patient

class TestAppointmentSchedule(unittest.TestCase):

    def test_no_appointments(self):
        doctor = Doctor('Leonard McCoy', 'DR123')
        schedule = AppointmentSchedule()
        calendar = schedule.find_appoitment(filter_professional=doctor)[0]
        self.assertEquals(0, len(calendar.keys()))

    def test_one_appointment(self):
        doctor = Doctor('Leonard McCoy', 'DR123')
        patient = Patient('John','Doe','Some Street 1','1234567')
        schedule = AppointmentSchedule()
        moment = datetime(2022,1,22,10,30)
        schedule.add_appoitment(Appointment('',doctor,patient, moment))
        calendar = schedule.find_appoitment(filter_professional=doctor)[0]
        self.assertEquals(1, len(calendar.keys()))
        self.assertEquals(patient, calendar[moment].patient)

    def test_two_doctors_appointment(self):
        doctor1 = Doctor('Leonard McCoy', 'DR123')
        patient1 = Patient('John','Doe','Some Street 1','1234567')
        doctor2 = Doctor('Jodie Whittaker', 'DR321')
        patient2 = Patient('Jane','Doe','Some Street 10','7654321')
        schedule = AppointmentSchedule()
        moment = datetime(2022,1,22,10,30)
        schedule.add_appoitment(Appointment('',doctor1,patient1, moment))
        schedule.add_appoitment(Appointment('',doctor2,patient2, moment))
        calendar = schedule.find_appoitment(filter_professional=doctor1)[0]
        self.assertEquals(1, len(calendar.keys()))
        self.assertEquals(patient1, calendar[moment].patient)
        calendar = schedule.find_appoitment(filter_professional=doctor2)[0]
        self.assertEquals(1, len(calendar.keys()))
        self.assertEquals(patient2, calendar[moment].patient)

    def test_same_patient_two_doctors(self):
        doctor1 = Doctor('Leonard McCoy', 'DR123')
        patient1 = Patient('John','Doe','Some Street 1','1234567')
        doctor2 = Doctor('Jodie Whittaker', 'DR321')
        patient2 = Patient('Jane','Doe','Some Street 10','7654321')
        schedule = AppointmentSchedule()
        moment1 = datetime(2022,1,22,10,30)
        moment2 = datetime(2022,1,22,11,30)
        schedule.add_appoitment(Appointment('',doctor1,patient1, moment1))
        schedule.add_appoitment(Appointment('',doctor2,patient1, moment2))
        schedule.add_appoitment(Appointment('',doctor1,patient2, moment2))
        schedule.add_appoitment(Appointment('',doctor2,patient2, moment1))

        calendars = schedule.find_appoitment(filter_patient=patient1)

        self.assertEquals(1, len(calendars[0]))
        self.assertEquals(patient1, calendars[0][moment1].patient)
        self.assertEquals(doctor1, calendars[0][moment1].staff)
        self.assertEquals(1, len(calendars[1]))
        self.assertEquals(patient1, calendars[1][moment2].patient)
        self.assertEquals(doctor2, calendars[1][moment2].staff)

    def test_same_patient_two_doctors_flatten(self):
        doctor1 = Doctor('Leonard McCoy', 'DR123')
        patient1 = Patient('John','Doe','Some Street 1','1234567')
        doctor2 = Doctor('Jodie Whittaker', 'DR321')
        schedule = AppointmentSchedule()
        schedule.add_appoitment(Appointment('',doctor1,patient1, datetime(2022,1,22,10,30)))
        schedule.add_appoitment(Appointment('',doctor2,patient1, datetime(2022,1,22,11,30)))
        schedule.add_appoitment(Appointment('',doctor2,patient1, datetime(2022,1,22,12,30)))

        appointments = schedule.find_appoitment(filter_patient=patient1, flatten=True)

        self.assertEquals(3, len(appointments))

if __name__ == '__main__':
    unittest.main()