import tkinter as tk
import socket
import threading
from tkinter.ttk import Combobox

# Constants
HOST = '192.168.103.1'
PORT = 4200

# Function to handle server communication
def communicate(request):
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((HOST, PORT))

    client_socket.sendall(request.encode())
    response = client_socket.recv(1024).decode()

    client_socket.close()
    return response

# Function to handle the "Check Availability" button click
def check_availability():
    floor = floor_entry.get()
    request = f'CHECK {floor}'
    response = communicate(request)
    availability_label.config(text=response)

# Function to handle the "Park Car" button click
def park_car():
    car_number = car_number_entry.get()
    floor = floor_entry.get()
    slot = slot_entry.get()
    request = f'PARK {car_number} {floor} {slot}'
    response = communicate(request)
    parking_info_label.config(text=response)

# Function to handle the "Leave Parking" button click
def leave_parking():
    token = token_entry.get()
    request = f'LEAVE {token}'
    response = communicate(request)
    bill_info_label.config(text=response)

# GUI setup
window = tk.Tk()
window.title("Parking System")
window.geometry("400x300+10+10")
window.config(bg="#d4faf6")

# Availability window
def create_availablity():
    avail = tk.Tk()
    avail.title("Check Availability")
    avail.geometry("400x300+10+10")
    avail.config(bg="#d4faf6")
    # Availability Label
    global availability_label
    availability_label = tk.Label(avail, text="", font=("Times New Roman", 12), bg="#d4faf6")
    availability_label.pack()

    # Car Number Entry
    global car_number_entry
    car_number_label = tk.Label(avail, text="Car Number:", font=("Helvetica", 12), height=2, bg="#d4faf6")
    car_number_label.pack()
    car_number_entry = tk.Entry(avail, bd=5)
    car_number_entry.pack()

    # Slot Entry
    global slot_entry, slot_label
    slot_label = tk.Label(avail, text="Slot:", font=("Helvetica", 12), height=2, bg="#d4faf6")
    slot_label.pack()
    slot_entry = tk.Entry(avail, bd=5)
    slot_entry.pack()

    # Park Car Button
    park_button = tk.Button(avail, text="Park Car", command=park_car, padx=35, bg="cyan", fg="black", font=("Helvetica", 10))
    park_button.pack()

    global parking_info_label
    # Parking Info Label
    parking_info_label = tk.Label(avail, text="", font=("Times New Roman", 14), bg="#d4faf6")
    parking_info_label.pack()





def check_pressed():
    create_availablity()
    check_availability()

# Floor Entry
floor_label = tk.Label(window, text="Floor:", font=("Helvetica", 12), height=3, bg="#d4faf6")
floor_label.pack()
floor_entry = tk.Entry(window, bd=5)
floor_entry.pack()

# Check Availability Button
check_button = tk.Button(window, text="Check Availability", command=check_pressed, padx=9, bg="cyan", fg="black", font=("Helvetica", 10), borderwidth=3, height=1 )
check_button.pack()
check_button.bind()


# Token Entry
token_label = tk.Label(window, text="Token:" , font=("Helvetica", 12), height=2, bg="#d4faf6")
token_label.pack()
token_entry = tk.Entry(window, bd=5)
token_entry.pack()
token_entry.bind('<FocusIn>')

# Leave Parking Button
leave_button = tk.Button(window, text="Leave Parking", command=leave_parking, padx=18, bg="cyan", fg="black", font=("Helvetica", 10), borderwidth=3, height=1)
leave_button.pack()
leave_button.bind('<Button-1>')

# Bill Info Label
bill_info_label = tk.Label(window, text="", font=("Times New Roman", 14), height=2, bg="#d4faf6")
bill_info_label.pack()

window.mainloop()
