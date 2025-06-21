from structures.subject import Subject

def load_data(file_path):
    with open(file_path, 'r') as file:
        lines= file.readlines()

        rooms={}
        line= lines[0].strip().split(':')
        room=line[1].split(',')
        for i in range(len(room)):
            rooms[i]= room[i].strip()

        n=len(lines[2:])
        events= [None for _ in range(n)]
        for i in range(n):
            event=lines[i+2].strip().split(',')
            s = Subject(event[0], int(event[1]))
            events[i] = s
        
        return rooms, events
    

def minutes_to_time(minutes):
    """Convert minutes since 7:00 to a time string in HH:MM format."""
    hours = 7 + minutes // 60
    mins = minutes % 60
    return f"{hours:02}:{mins:02}"

def duration_to_minutes(duration_str):
    """Convert a duration string in HH:MM format to minutes."""
    hours, mins = map(int, duration_str.split(':'))
    return hours * 60 + mins

        