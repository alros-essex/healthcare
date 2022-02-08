import random
from .init_task import InitTask

class InitPatients(InitTask):
    """fill the database with random patients"""
    
    def __init__(self, storage):
        super().__init__(11, 'registering patients')
        self._storage = storage

    def init(self):
        self._generate_patients()
        self._notify('patients registration: done')

    def _generate_patients(self):
        from healthcare.patient import Patient
        surnames = ['Smith', 'Jones', 'Taylor', 'Brown', 'Williams', 'Wilson', 'Johnson', 'Davies', 'Patel', 'Robinson']
        firstnames = ['James', 'John', 'Robert', 'Michael', 'William', 'David', 'Richard', 'Charles', 'Joseph', 'Thomas', 
                 'Mary', 'Patricia', 'Linda', 'Barbara', 'Elizabeth', 'Jennifer', 'Maria', 'Susan', 'Margaret', 'Dorothy']
        street_names = ['Main St', '2nd St', '3rd St', '1st St', 'Oak St', '4th St', 'Elm St', 'Pine St', 'Church St', 'Maple St']

        doctors = self._storage.select_doctors()

        for surname in surnames:
            for firstname in firstnames:
                patient = Patient(
                    name = '{} {}'.format(firstname, surname),
                    address = street_names[random.randrange(0,9)],
                    phone = '+44-7911 {:06d}'.format(random.randrange(111111,999999)))
                self._storage.insert_patient(patient)
                self._storage.associate_doctor_patient(random.choice(doctors), patient)
            self._notify('patients named {}'.format(surname))
