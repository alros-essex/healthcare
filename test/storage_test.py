from datetime import datetime
import unittest

class TestStorage(unittest.TestCase):

    def test_insert_select_doctor(self):
        from healthcare.doctor import Doctor
        storage = self._get_storage()
        storage.insert_employee(Doctor('Who','DR1234'))
        doctors = storage.select_employee(employee_number = 'DR1234')
        self.assertEquals(1, len(doctors))
        self.assertEqual('Who', doctors[0].name)

    def test_insert_select_nurse_from_group(self):
        from healthcare.doctor import Doctor
        from healthcare.nurse import Nurse
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
        from healthcare.patient import Patient
        storage = self._get_storage()
        storage.insert_patient(Patient('John', 'Nowhere st. 0', '+0 1111 0000'))
        patient = storage.select_patient('John')
        self.assertEquals('John', patient.name)
        self.assertEquals('Nowhere st. 0', patient.address)
        self.assertEquals('+0 1111 0000', patient.phone)

    def test_select_insert_appointment(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        from healthcare.appointment import Appointment
        from healthcare.appointment_type import AppointmentType
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

    def test_select_appointment_dates(self):
        from healthcare.appointment import Appointment
        from healthcare.appointment_type import AppointmentType
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        storage = self._get_storage()
        storage.insert_appointment(Appointment(
            AppointmentType.NORMAL, 
            Doctor('','DR1234'), 
            Patient('John', '', ''), 
            datetime(2022,1,1,10,30)))
        storage.insert_appointment(Appointment(
            AppointmentType.NORMAL, 
            Doctor('','DR1234'), 
            Patient('John', '', ''), 
            datetime(2022,2,2,10,30)))
        self.assertEquals(['01-01-2022', '02-02-2022'], storage.select_appointment_dates())

    def test_test_associate_doctor_patient_and_select_doctor_for_patient(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        storage = self._get_storage()
        doctor = Doctor('A','DR1')
        patient = Patient('P','','')
        storage.insert_employee(doctor)
        storage.insert_patient(patient)
        storage.associate_doctor_patient(doctor, patient)
        # this should find all doctors
        self.assertEqual(doctor, storage.select_doctor_for_patient(patient))

    def test_select_doctors(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        storage = self._get_storage()
        doctor1 = Doctor('A','DR1')
        doctor2 = Doctor('B','DR2')
        storage.insert_employee(doctor1)
        storage.insert_employee(doctor2)
        storage.associate_doctor_patient(doctor1, Patient('p1','',''))
        storage.associate_doctor_patient(doctor1, Patient('p2','',''))
        storage.associate_doctor_patient(doctor2, Patient('p3','',''))
        # this should find all doctors
        self.assertEqual(2, len(storage.select_doctors()))
        # this should find only the doctor with 1 or less patients
        self.assertEqual([doctor2], storage.select_doctors(max_patients=1))

    def test_select_receptionists(self):
        from healthcare.receptionist import Receptionist
        from healthcare.doctor import Doctor
        storage = self._get_storage()
        receptionist = Receptionist('A','123')
        storage.insert_employee(receptionist)
        storage.insert_employee(Doctor('D','456'))
        self.assertEqual([receptionist], storage.select_receptionists())

    def test_select_patients(self):
        from healthcare.patient import Patient
        storage = self._get_storage()
        storage.insert_patient(Patient('P1','A1','T1'))
        storage.insert_patient(Patient('P2','A2','T2'))
        storage.insert_patient(Patient('P3','A3','T3'))
        self.assertEqual(Patient('P2','A2','T2'), storage.select_patient('P2'))


    def test_delete_appointment(self):
        from healthcare.doctor import Doctor
        from healthcare.patient import Patient
        from healthcare.appointment import AppointmentType
        from healthcare.appointment import Appointment
        storage = self._get_storage()
        doctor = Doctor('','DR1234')
        patient = Patient('John', '', '')
        storage.insert_employee(doctor)
        storage.insert_patient(patient)
        appointment1 = Appointment(AppointmentType.NORMAL, doctor, patient, datetime(2022,1,1,10,30))
        storage.insert_appointment(appointment1)
        storage.insert_appointment(Appointment(AppointmentType.NORMAL, doctor, patient, datetime(2022,2,2,10,30)))
        self.assertEqual(2, len(storage.select_appointments()))
        storage.delete_appointment(appointment1)
        self.assertEqual(1, len(storage.select_appointments()))

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
        from healthcare.storage import Storage
        Storage.reset()
        return Storage.instance()