from console.progress_bar import ProgressBar
from healthcare.clinic import Clinic

from .init_clinic import InitClinic
from .init_doctors import InitDoctors
from .init_nurses import InitNurses
from .init_patients import InitPatients
from .init_receptionists import InitReceptionists

class Initializer():

    def init(self, clinic:Clinic, quick:bool=False):
        init_steps = [
            InitClinic(),
            InitDoctors(),
            InitNurses(),
            InitReceptionists(),
            InitPatients()
        ]
        pause_time = 0.01 if quick else 0.3
        for index, init_step in enumerate(init_steps):
            init_step.add_event_listener(ProgressBar(
                steps = init_step.sub_steps_count, 
                init_message = init_step.description, 
                row = index, 
                pause_time = pause_time))

        for init_step in init_steps:
            init_step.init(clinic)

    


