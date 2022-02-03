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
        storage = self._get_storage()
        storage.insert_employee(Doctor('Who','DR1234'))
        doctors = storage.select_employee(employee_number = 'DR1234')
        self.assertEquals(1, len(doctors))
        self.assertEqual('Who', doctors[0].name)

    def test_insert_select_nurse_from_group(self):
        storage = self._get_storage()
        
        storage.insert_employee(Doctor('Who','DR1234'))
        storage.insert_employee(Nurse('Pond','NR1111'))
        storage.insert_employee(Nurse('Song','NR2222'))
        storage.insert_employee(Nurse('Clara','NR3333'))
        nurses = storage.select_employee(employee_number = 'NR2222')
        self.assertEquals(1, len(nurses))
        self.assertEqual('Song', nurses[0].name)
        self.assertEqual(nurses, storage.select_nurses(employee_number = 'NR2222'))

    def test_insert_select_patient(self):
        storage = self._get_storage()
        storage.insert_patient(Patient('John', 'Nowhere st. 0', '+0 1111 0000'))
        patient = storage.select_patient('John')
        self.assertEquals('John', patient.name)
        self.assertEquals('Nowhere st. 0', patient.address)
        self.assertEquals('+0 1111 0000', patient.phone)

    def test_select_insert_appointment(self):
        storage = self._get_storage()
        doctor = Doctor('Who','DR1234')
        patient = Patient('John', 'Nowhere st. 0', '+0 1111 0000')
        date = datetime(2022, 1, 29)
        storage.insert_employee(doctor)
        storage.insert_patient(patient)
        storage.insert_appointment(Appointment(AppointmentType.NORMAL, doctor, patient, date))
        appointments = storage.select_appointments()
        self.assertEquals(1, len(appointments))
        appointment:Appointment = appointments[0]
        self.assertEquals('Who', appointment.staff.name)
        self.assertEquals('John', appointment.patient.name)
        self.assertEquals(AppointmentType.NORMAL, appointment.type)
        self.assertEquals(date, appointment.date)

    def test_associate_doctor_patient(self):
        pass

    def test_select_doctor_for_patient(self):
        pass

    def test_select_doctors(self):
        pass

    def test_select_receptionists(self):
        pass

    def test_select_patients(self):
        pass

    def test_select_appointment_dates(self):
        pass

    def test_delete_appointment(self):
        pass

    def test_insert_select_prescriptions(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        from healthcare.prescription import Prescription
        storage = self._get_storage()
        patient = Patient('James','','')
        doctor = Doctor('Who', 'DR123')
        patient._doctor = doctor
        storage.insert_patient(patient)
        storage.insert_prescription(Prescription('type', patient, doctor, 1, 1.2))
        prescriptions = storage.select_prescriptions(patient)
        self.assertEqual(1, len(prescriptions))
        prescription:Prescription = prescriptions[0]
        self.assertEqual(patient, prescription.patient)
        self.assertEqual(doctor, prescription.doctor)
        self.assertEqual(1, prescription.quantity)
        self.assertEqual(1.2, prescription.dosage)

    def _get_storage(self):
        Storage.reset()
        return Storage.instance()