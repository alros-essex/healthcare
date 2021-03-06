from datetime import datetime
import random
from .init_task import InitTask

class InitAppointments(InitTask):
    """creates some appointments in the schedule"""
    def __init__(self, storage, schedule):
        super().__init__(12, 'getting first appointments')
        self._storage = storage
        self._schedule = schedule

    def init(self):
        doctors = self._storage.select_doctors()
        patients = self._storage.select_patients()
        receptionist = self._storage.select_receptionists()[0]
        for i in range(0,11):
            # this is also a good end-to-end test
            patient = patients[random.randrange(0,len(patients))]
            doctor = doctors[random.randrange(0,len(doctors))]
            self._notify('booking appointment for {}'.format(patient))
            appointment = receptionist.propose_appointment(doctor, patient, False, datetime.now())
            receptionist.register_appointment(appointment)
        self._notify('booking appointment: done')

 