from console.progress_bar import ProgressBar
from healthcare.appointment_schedule import AppointmentSchedule
from healthcare.storage import Storage

from .init_appointments import InitAppointments
from .init_clinic import InitClinic
from .init_doctors import InitDoctors
from .init_nurses import InitNurses
from .init_patients import InitPatients
from .init_receptionists import InitReceptionists

class Initializer():

    def __init__(self, db:Storage, schedule:AppointmentSchedule, quick:bool=False) -> None:
        self._db = db
        self._schedule = schedule
        self._quick = quick

    def initialize(self):
        init_steps = [
            InitClinic(),
            InitDoctors(self._db, self._schedule),
            InitNurses(self._db, self._schedule),
            InitReceptionists(self._db, self._schedule),
            InitPatients(self._db),
            InitAppointments(self._db, self._schedule)
        ]
        pause_time = 0.01 if self._quick else 0.3
        for index, init_step in enumerate(init_steps):
            init_step.add_event_listener(ProgressBar(
                steps = init_step.sub_steps_count, 
                init_message = init_step.description, 
                row = index, 
                pause_time = pause_time))

        for init_step in init_steps:
            init_step.init()

    


