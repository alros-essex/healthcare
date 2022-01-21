import random

from healthcare.clinic import Clinic
from healthcare.patient import Patient

from .init_task import InitTask

class InitPatients(InitTask):
    def __init__(self):
        super().__init__(12, 'registering patients')

    def init(self, clinic:Clinic):    
        self._notify('advertizing the clinic')
        self._generate_patients(clinic)
        self._notify('patients registration: done')

    def _generate_patients(self, clinic:Clinic):
        surnames = ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Patel', 'Robinson']
        names = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas', 
                 'Mary', 'Patricia', 'Linda', 'Barbara', 'Elizabeth', 'Jennifer', 'Maria', 'Susan', 'Margaret', 'Dorothy']
        street_names = ['Main St', '2nd St', '3rd St', '1st St', 'Oak St', '4th St', 'Elm St', 'Pine St', 'Church St', 'Maple St']

        for surname in surnames:
            for name in names:
                clinic.register_patient(Patient(
                    name = name, 
                    surname = surname,
                    address = street_names[random.randrange(0,9)],
                    phone = '+44-7911 {:06d}'.format(random.randrange(111111,999999))))
            self._notify('patients named {}'.format(surname))
