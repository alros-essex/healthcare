class Initializer():
    """Main class of the initialization utility"""

    def __init__(self, db, schedule, quick:bool=False) -> None:
        self._db = db
        self._schedule = schedule
        self._quick = quick

    def initialize(self):
        """calls all init tasks"""
        from .init_appointments import InitAppointments
        from .init_doctors import InitDoctors
        from .init_nurses import InitNurses
        from .init_patients import InitPatients
        from .init_receptionists import InitReceptionists
        from .progress_bar import ProgressBar
        init_steps = [
            InitDoctors(self._db),
            InitNurses(self._db),
            InitReceptionists(self._db),
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

    


