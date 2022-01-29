from datetime import datetime
import unittest
from healthcare.appointment import Appointment
from healthcare.appointment_type import AppointmentType
from healthcare.doctor import Doctor
from healthcare.nurse import Nurse
from healthcare.patient import Patient
from healthcare.storage import Storage


class TestStorage(unittest.TestCase):

    def test_insert_select_doctor(self):
        storage = Storage()
        
        storage.insert_employee(Doctor('Who','DR1234'))
        doctors = storage.select_employee(employee_number = 'DR1234')

        self.assertEquals(1, len(doctors))
        self.assertEqual('Who', doctors[0].name)

    def test_insert_select_nurse_from_group(self):
        storage = Storage()
        
        storage.insert_employee(Doctor('Who','DR1234'))
        storage.insert_employee(Nurse('Pond','NR1111'))
        storage.insert_employee(Nurse('Song','NR2222'))
        storage.insert_employee(Nurse('Clara','NR3333'))
        nurses = storage.select_employee(employee_number = 'NR2222')

        self.assertEquals(1, len(nurses))
        self.assertEqual('Song', nurses[0].name)

    def test_insert_select_patient(self):
        storage = Storage()

        storage.insert_patient(Patient('John', 'Doe', 'Nowhere st. 0', '+0 1111 0000'))
        patient = storage.select_patient('John', 'Doe')

        self.assertEquals('John', patient.firstname)
        self.assertEquals('Doe', patient.surname)
        self.assertEquals('Nowhere st. 0', patient.address)
        self.assertEquals('+0 1111 0000', patient.phone)

    def test_select_insert_appointment(self):
        storage = Storage()
        doctor = Doctor('Who','DR1234')
        patient = Patient('John', 'Doe', 'Nowhere st. 0', '+0 1111 0000')
        date = datetime(2022, 1, 29)
        storage.insert_employee(doctor)
        storage.insert_patient(patient)

        storage.insert_appointment(Appointment(AppointmentType.NORMAL, doctor, patient, date))
        appointments = storage.select_appointments()

        self.assertEquals(1, len(appointments))
        appointment:Appointment = appointments[0]
        self.assertEquals('Who', appointment.staff.name)
        self.assertEquals('Doe', appointment.patient.surname)
        self.assertEquals(AppointmentType.NORMAL, appointment.type)
        self.assertEquals(date, appointment.date)