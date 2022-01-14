class AppointmentSchedule():
    """
    Represents the schedule of the appointments
    """
    def __init__(self):
        """creates the instance
        
        Args:
            None
        Returns:
            None
        """
        self._appoitments = []

    @property
    def appointments(self):
        return self._appoitments

    def add_appoitment(self):
        """creates an appoitment
        
        Args:
            None
        Returns:
            Appointment: appointment just created
        """
        pass

    def cancel_appoitment(self):
        """deletes an appoitment
        
        Args:
            None
        Returns:
            Appointment: appoitment just deleted
        """
        pass

    def find_appoitment(self):
        """finds an appoitment
        
        Args:
            None
        Returns:
            Appointment: the found appointment
        """
        pass