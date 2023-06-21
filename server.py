import socket
import csv
import time
import threading
import hashlib

# Constants
HOST = 'localhost'
PORT = 4200
PARKING_RATE = 20  # Rs per hour
NUM_FLOORS = 5
SLOTS_PER_FLOOR = 15

# Data structures
parking_lot = {}
for floor in range(1, NUM_FLOORS + 1):
    parking_lot[str(floor)] = { str(slot): None for slot in range(1, SLOTS_PER_FLOOR + 1) }

# Function to check the availability of parking slots on a floor
def check_availability(floor):
    for slot, car in parking_lot[floor].items():
        if car is None:
            return slot
    return None

# Function to generate a unique 8-digit token number derived from entry time
def generate_token(entry_time):
    md5_hash = hashlib.md5(str(entry_time).encode()).hexdigest()
    token = md5_hash[:8]
    return token

# Function to calculate parking bill
def calculate_bill(entry_time, exit_time):
    parking_duration = exit_time - entry_time
    bill = (parking_duration // 3600 + 1) * PARKING_RATE
    return bill

# Function to update the log file
def update_log(entry_time, exit_time, bill, floor, slot, car_number, token):
    with open('parking_log.csv', mode='a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([token, car_number, entry_time, exit_time, bill, floor, slot])

# Function to handle client requests
def handle_client(client_socket, client_address):
    print(f'Connected to client: { client_address }')

    while True:
        # Receive client request
        request = client_socket.recv(1024).decode()

        if request.startswith('CHECK'):
            _, preferred_floor = request.split()
            available_slot = check_availability(preferred_floor)

            if available_slot is None:
                # Find the nearest floor with available slots
                for floor in parking_lot.keys():
                    available_slot = check_availability(floor)
                    if available_slot:
                        break

            response = f'FLOOR { preferred_floor }: SLOT { available_slot } AVAILABLE'
            client_socket.sendall(response.encode())
            print('Checking for request')

        elif request.startswith('PARK'):
            _, car_number, floor, slot = request.split()
            if parking_lot[floor][slot] is None:
                entry_time = int(time.time())
                token = generate_token(entry_time)
                parking_lot[floor][slot] = {
                    'car_number': car_number,
                    'entry_time': entry_time,
                    'token': token
                }
                response = f'CAR {car_number} PARKED. TOKEN: {token}'
            else:
                response = f'THE SLOT {slot} IS FULL'
            client_socket.sendall(response.encode())
            print('Parking request')

        elif request.startswith('LEAVE'):
            _, token = request.split()
            exit_time = int(time.time())
            floor = None
            slot = None
            car_number = None
            bill = 0

            # Find the car details using the token
            for floor, slots in parking_lot.items():
                for slot, car in slots.items():
                    if car and car['token'] == token:
                        car_number = car['car_number']
                        entry_time = car['entry_time']
                        bill = calculate_bill(entry_time, exit_time)
                        parking_lot[floor][slot] = None
                        break

            if car_number is not None:
                response = f'CAR { car_number } LEFT. BILL: { bill } Rs'
                update_log(entry_time, exit_time, bill, floor, slot, car_number, token)
            else:
                response = f'The token number { token } is invalid'
            client_socket.sendall(response.encode())
            print('Leaving the parking site')

    client_socket.close()

# Socket server
def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((HOST, PORT))
    server_socket.listen()

    print('Server started. Listening for connections...')

    while True:
        client_socket, client_address = server_socket.accept()
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()

# Create parking_log.csv if it does not exist
with open('parking_log.csv', mode='a') as file:
    pass

# Start the server
if __name__ == '__main__':
    start_server()
