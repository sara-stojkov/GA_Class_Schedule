class Subject:
    """Represents a class of a subject with a name, duration, and index that can be easily accessed in the list."""

    __slots__ = ('name', 'duration', 'index')
    def __init__(self, name: str, duration: int, index: int ):
        self.name = name
        self.duration = duration
        self.index = index

    def get_name(self):
        """Returns the name of the subject."""
        return self.name
    
    def get_duration(self):
        """Returns the duration of the subject."""
        return self.duration

    def get_index(self):
        """Returns the index of the subject."""
        return self.index
    
    def __repr__(self):
        return f"Subject(name={self.name}, duration={self.duration}, index={self.index})"

    def __str__(self):
        return f"Subject: {self.name}, Duration: {self.duration}, Index: {self.index}"

    def __eq__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return (self.name == other.name and 
                self.duration == other.duration and 
                self.index == other.index)
    
    def __hash__(self):
        return hash((self.name, self.duration, self.index))
    
    def __lt__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return self.index < other.index
    
    def __le__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return self.index <= other.index
    
    def __gt__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return self.index > other.index
    
    def __ge__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return self.index >= other.index
    
    def __ne__(self, other):
        if not isinstance(other, Subject):
            return NotImplemented
        return not self.__eq__(other)