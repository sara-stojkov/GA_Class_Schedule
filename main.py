from reading_data import load_data

def main():
    file_path = 'data_timetable.txt'
    rooms, events = load_data(file_path)

    print("Rooms:")
    for room_id, room_name in rooms.items():
        print(f"  {room_id}: {room_name}")

    print("\nEvents:")
    for event in events:
        print(f"  {event[0]}: {event[1]} ")

if __name__ == "__main__":
    main()