from datetime import datetime
import random

from healthcare.storage import Storage
from healthcare.appointment_schedule import AppointmentSchedule

from .init_task import InitTask

class InitAppointments(InitTask):
    def __init__(self, storage:Storage, schedule:AppointmentSchedule):
        super().__init__(12, 'getting first appointments')
        self._storage = storage
        self._schedule = schedule

    def init(self):
        doctors = self._storage.select_doctors()
        patients = self._storage.select_patients()
        receptionist = self._storage.select_receptionists()[0]
        receptionist.connect_to_schedule(self._schedule)
        for i in range(0,11):
            patient = patients[random.randrange(0,len(patients))]
            doctor = doctors[random.randrange(0,len(doctors))]
            self._notify('booking appointment for {}'.format(patient))
            slot = receptionist.find_next_free_timeslot(doctor, False, datetime.now())
            receptionist.make_appointment(doctor, patient, slot, False)
        self._notify('booking appointment: done')

 