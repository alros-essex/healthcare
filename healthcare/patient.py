from datetime import datetime
import random


class Patient():
    """
    Models a patient of the clinic
    """
    def __init__(self, name:str, address:str, phone:str):
        """creates the instance
        
        Args:
            name: patient's name
            address: patient's address
            phone: patient's phone
        Returns:
            None
        """
        from healthcare.storage import Storage
        self._name = name
        self._address = address
        self._phone = phone
        self._prescriptions = {}
        self._storage = Storage.instance()

    @property
    def name(self):
        return self._name

    @property
    def address(self):
        return self._address

    @property
    def phone(self):
        return self._phone

    def doctor(self):
        return self._storage.select_doctor_for_patient(self)

    def request_repeat(self, doctor):
        for p in self.prescriptions.values():
            doctor.approve_repeat(p)

    def request_appointment(self, receptionist) -> None:
        my_doctor = self.doctor()
        if my_doctor is None:
            available_doctors = receptionist.find_available_doctors()
            my_doctor = random.choice(available_doctors)
            receptionist.register_patient(self, my_doctor)
        urgent = random.randint(1, 20) == 20
        accepted = False
        while not accepted:
            appointment = receptionist.propose_appointment(my_doctor, self, urgent, datetime.now())
            accepted = random.randint(1, 4) == 4
        receptionist.register_appointment(appointment)

    def accept_prescription(self, prescription) -> None:
        self._prescriptions[prescription.type] = prescription

    @property
    def prescriptions(self):
        return self._prescriptions

    def __lt__(self, other):
        return other is not None and self.name < other.name
    
    def __le__(self, other):
        return other is not None and self.name <= other.name

    def __eq__(self, other):
        return other is not None and self.name == other.name
    
    def __ne__(self, other):
        return other is not None and self.name != other.name
    
    def __gt__(self, other):
        return other is not None and self.name > other.name
    
    def __ge__(self, other):
        return other is not None and self.name >= other.name

    def __str__(self) -> str:
        return self.name