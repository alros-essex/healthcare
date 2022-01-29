import random

from healthcare.storage import Storage
from healthcare.patient import Patient

from .init_task import InitTask

class InitPatients(InitTask):
    def __init__(self, storage:Storage):
        super().__init__(12, 'registering patients')
        self._storage = storage

    def init(self):    
        self._notify('advertizing the clinic')
        self._generate_patients()
        self._notify('patients registration: done')

    def _generate_patients(self):
        surnames = ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Patel', 'Robinson']
        firstnames = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas', 
                 'Mary', 'Patricia', 'Linda', 'Barbara', 'Elizabeth', 'Jennifer', 'Maria', 'Susan', 'Margaret', 'Dorothy']
        street_names = ['Main St', '2nd St', '3rd St', '1st St', 'Oak St', '4th St', 'Elm St', 'Pine St', 'Church St', 'Maple St']

        for surname in surnames:
            for firstname in firstnames:
                self._storage.insert_patient(Patient(
                    firstname = firstname, 
                    surname = surname,
                    address = street_names[random.randrange(0,9)],
                    phone = '+44-7911 {:06d}'.format(random.randrange(111111,999999))))
            self._notify('patients named {}'.format(surname))
