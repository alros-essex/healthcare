import random
import unittest

class TestEndToEnd(unittest.TestCase):

    def test_register_patients(self):
        from healthcare.appointment import Appointment
        from healthcare.doctor import Doctor
        from healthcare.nurse import Nurse
        from healthcare.patient import Patient
        from healthcare.receptionist import Receptionist
        from healthcare.storage import Storage
        from healthcare.appointment_schedule import AppointmentSchedule
        st, sc = self._get_fresh_storage_and_schedule()
        storage:Storage = st
        schedule:AppointmentSchedule = sc

        # hire some employees
        for employee in [
            Doctor('James Kildare', 'DR001'),
            Doctor('Gregory House', 'DR002'),
            Nurse('Haleh Adams', 'NR001'),
            Nurse('Carla Espinosa', 'NR002'),
            Receptionist('Pam Beesly', 'RC001'),
            Receptionist('Randy Marsh', 'RC002')]:
            storage.insert_employee(employee)

        # the clinic just opened and patients came to register
        surnames = ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Patel', 'Robinson']
        firstnames = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas', 
                 'Mary', 'Patricia', 'Linda', 'Barbara', 'Elizabeth', 'Jennifer', 'Maria', 'Susan', 'Margaret', 'Dorothy']
        street_names = ['Main St', '2nd St', '3rd St', '1st St', 'Oak St', '4th St', 'Elm St', 'Pine St', 'Church St', 'Maple St']

        # find the staff from db
        receptionists = storage.select_receptionists()
        front_desk_receptionist:Receptionist = receptionists[0]
        phone_receptionist:Receptionist = receptionists[1]
        doctors = storage.select_doctors()
        nurses = storage.select_nurses()

        for surname in surnames:
            for firstname in firstnames:
                patient = Patient(
                    name = '{} {}'.format(firstname, surname),
                    address = street_names[random.randrange(0,9)],
                    phone = '+44-7911 {:06d}'.format(random.randrange(111111,999999)))
                front_desk_receptionist.register_patient(patient, random.choice(doctors))

        # check that everyone has been registered
        patients = storage.select_patients()
        self.assertEqual(len(surnames)*len(firstnames), len(patients))
        # ...and got a doctor
        for patient in patients:
            self.assertIsNotNone(storage.select_doctor_for_patient(patient))

        # patients call to get an appointment
        for i in range(1, 200):
            patient:Patient = random.choice(patients)
            initial_sc = len(schedule.find_appointments(filter_patient=patient))
            initial_db = len(storage.select_appointments(filter_patient=patient))
            patient.request_appointment(phone_receptionist)
            self.assertEquals(initial_db + 1, len(storage.select_appointments(filter_patient=patient)))
            self.assertEquals(initial_sc + 1, len(schedule.find_appointments(filter_patient=patient)))
        
        # patients come for the consultation
        for a in storage.select_appointments():
            appointment:Appointment = a
            staff = appointment.staff
            patient = appointment.patient
            self.assertIsNotNone(staff.consultation(patient))
            if isinstance(staff, Doctor):
                # every doctor gives a prescription the first time
                self.assertTrue(len(storage.select_prescriptions(patient))>0)

    def _get_fresh_storage_and_schedule(self):
        from healthcare.storage import Storage
        from healthcare.appointment_schedule import AppointmentSchedule
        Storage.reset()
        AppointmentSchedule.reset()
        storage = Storage.instance()
        schedule = AppointmentSchedule.instance()
        return storage, schedule