from datetime import date, datetime
import random

from healthcare.clinic import Clinic

from .init_task import InitTask

class InitAppointments(InitTask):
    def __init__(self):
        super().__init__(12, 'getting first appointments')

    def init(self, healthcare:Clinic):
        doctors = healthcare.doctors
        patients = healthcare.patients
        for i in range(0,11):
            patient = patients[random.randrange(0,len(patients))]
            doctor = doctors[random.randrange(0,len(doctors))]
            self._notify('booking appointment for {}'.format(patient))
            slot = healthcare.receptionists[0].find_next_free_timeslot(healthcare.appointment_schedule, doctor, False, datetime.now())
            healthcare.receptionists[0].make_appointment(healthcare.appointment_schedule, doctor, patient, slot, False)
        self._notify('booking appointment: done')

 