class Subject:
    """Represents a class of a subject with a name and duration that can be easily accessed in the list."""

    __slots__ = ('name', 'duration')
    def __init__(self, name: str, duration: int):
        self.name = name
        self.duration = duration // 15

        

    def get_name(self):
        """Returns the name of the subject."""
        return self.name
    
    def get_duration(self):
        """Returns the duration of the subject."""
        return self.duration

    def __repr__(self):
        return f"Subject(name={self.name}, duration={self.duration})"

    def __str__(self):
        return f"Subject: {self.name}, Duration: {self.duration}"

    def __eq__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return (self.name == other.name and 
                self.duration == other.duration)
    
    def __hash__(self):
        return hash((self.name, self.duration))

    def __ne__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return not self.__eq__(other)