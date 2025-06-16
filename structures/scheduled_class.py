class ScheduledClass:
    """
    Represents a scheduled class with its associated details. Event has the index of the class,
    day is the day of the week (0-4), room is the room number, start_time is the start time in minutes from 7:00 (so 60 becomes 8:00) and
    end_time is the end time in minutes from 7:00.
    """
    __slots__ = ('event', 'day', 'room', 'start_time', 'end_time')

    def __init__(self, event: int, day: int, room: int, start_time: int, end_time: int):
        self.event = event
        self.day = day
        self.room = room
        self.start_time = start_time
        self.end_time = end_time

    def __repr__(self):
        return (f"ScheduledClass(event={self.event}, day={self.day}, room={self.room}, "
                f"start_time={self.start_time}, end_time={self.end_time})")
    
    def __str__(self):
        return (f"ScheduledClass: Event {self.event}, Day {self.day}, Room {self.room}, "
                f"Start Time: {self.start_time}, End Time: {self.end_time}")
    
    def __eq__(self, other):
        if not isinstance(other, ScheduledClass):
            return NotImplemented
        return (self.event == other.event and 
                self.day == other.day and 
                self.room == other.room and 
                self.start_time == other.start_time and 
                self.end_time == other.end_time)
    
    