from structures.subject import Subject

data_timetable_txt = """rooms: A, B, C, D, E
events(name, duration):
NPiEA - Predavanje, 180
Diskretna matematika - Predavanje, 120
Organizacija podataka - Predavanje, 120
NAiNS - Predavanje, 180
Objektno orijentisano programiranje 2 - Predavanje, 90
Algebra - Predavanje, 30
Arhitektura racunara - Predavanje, 30
Engleski jezik - Predavanje, 90
Osnove programiranja - Predavanje, 30
Sociologija tehnike - Predavanje, 60
Objektno orijentisano programiranje 1 - Predavanje, 180
Algoritmi i strukture podataka - Predavanje, 90
Uvod u softversko inzenjerstvo - Predavanje, 60
Internet mreze - Predavanje, 180
Matematicka analiza - Predavanje, 120
NPiEA - Vezbe 1, 120
Diskretna matematika - Vezbe 1, 180
Organizacija podataka - Vezbe 1, 60
NAiNS - Vezbe 1, 180
Objektno orijentisano programiranje 2 - Vezbe 1, 120
Algebra - Vezbe 1, 180
Arhitektura racunara - Vezbe 1, 120
Engleski jezik - Vezbe 1, 60
Osnove programiranja - Vezbe 1, 60
Sociologija tehnike - Vezbe 1, 60
Objektno orijentisano programiranje 1 - Vezbe 1, 30
Algoritmi i strukture podataka - Vezbe 1, 180
Uvod u softversko inzenjerstvo - Vezbe 1, 90
Internet mreze - Vezbe 1, 180
Matematicka analiza - Vezbe 1, 90
NPiEA - Vezbe 2, 180
Diskretna matematika - Vezbe 2, 30
Organizacija podataka - Vezbe 2, 180
NAiNS - Vezbe 2, 30
Objektno orijentisano programiranje 2 - Vezbe 2, 120
Algebra - Vezbe 2, 30
Arhitektura racunara - Vezbe 2, 180
Engleski jezik - Vezbe 2, 180
Osnove programiranja - Vezbe 2, 120
Sociologija tehnike - Vezbe 2, 120
Objektno orijentisano programiranje 1 - Vezbe 2, 120
Algoritmi i strukture podataka - Vezbe 2, 30
Uvod u softversko inzenjerstvo - Vezbe 2, 180
Internet mreze - Vezbe 2, 180
Matematicka analiza - Vezbe 2, 180
NPiEA - Vezbe 3, 90
Diskretna matematika - Vezbe 3, 180
Organizacija podataka - Vezbe 3, 60
NAiNS - Vezbe 3, 180
Objektno orijentisano programiranje 2 - Vezbe 3, 90
Algebra - Vezbe 3, 120
Arhitektura racunara - Vezbe 3, 120
Engleski jezik - Vezbe 3, 180
Osnove programiranja - Vezbe 3, 90
Sociologija tehnike - Vezbe 3, 90
Objektno orijentisano programiranje 1 - Vezbe 3, 180
Algoritmi i strukture podataka - Vezbe 3, 120
Uvod u softversko inzenjerstvo - Vezbe 3, 60
Internet mreze - Vezbe 3, 180
Matematicka analiza - Vezbe 3, 60"""

def load_data_from_string():
    lines = data_timetable_txt.strip().split('\n')

    rooms = {}
    line = lines[0].strip().split(':')
    room_list = line[1].split(',')
    for i in range(len(room_list)):
        rooms[i] = room_list[i].strip()

    n = len(lines) - 2
    events = [None for _ in range(n)]
    for i in range(n):
        event = lines[i + 2].strip().split(',')
        s = Subject(event[0], int(event[1]))
        events[i] = s
    
    return rooms, events


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
    

        