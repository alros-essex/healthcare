from abc import abstractmethod, ABC
from .progress_bar import ProgressBar
from .clinic import Healthcare
from .init_clinic import InitClinic
from .init_doctors import InitDoctors
from .init_nurses import InitNurses
from .init_receptionists import InitReceptionists

def main():
    """Entry point: call this method to start the application"""

    healthcare = Healthcare()

    init_steps = [
        InitClinic(),
        InitDoctors(),
        InitNurses(),
        InitReceptionists()
    ]
        
    for index, init_step in enumerate(init_steps):
        init_step.add_event_listener(ProgressBar(init_step.sub_steps_count, init_step.description, index))

    for init_step in init_steps:
        init_step.init(healthcare)

    


