class Event():
    """used by the progress bar"""
    
    def __init__(self, description:str) -> None:
        self._descripton = description

    @property
    def description(self):
        return self._descripton