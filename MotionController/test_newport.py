#from newportESP302 import ESP
from ethernet_newport import ESP
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import socket
import time
import sys
import math
import time


def connect_to_device(ip_address, port):
    try:
        # Create a socket object
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        # Set a timeout for the connection (optional)
        client_socket.settimeout(5)

        # Connect to the device using the IP address and port number
        client_socket.connect((ip_address, port))
        
        print(f"Successfully connected to {ip_address}:{port}")

        # Perform any necessary communication with the device here
        
        # Close the socket when done
        client_socket.close()

    except socket.error as e:
        print(f"Error connecting to {ip_address}:{port}: {e}")

def send_string_over_socket(ip_address, port, data):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        try:
            sock.connect((ip_address, port))
            sock.sendall(data.encode())
            response = sock.recv(1024).decode()
            print("Response from the device:", response)
        except (socket.error, ConnectionRefusedError) as e:
            print(f"Error while connecting to the device: {e}")
        finally:
            sock.close()
        
    
if __name__ == '__main__':
    device_ip = '192.168.254.254'
    device_port = 5001
    esp = ESP(device_ip, device_port)
    
    #data_to_send = '1PR1\r'5
    axis_x = esp.axis(1)
    axis_y= esp.axis(2)

    # axis1.on()
    # axis2.on()


    # print("Resolution")
    # axis_x.backlash
    # axis_y.backlash
    # print("Home")
    axis_y.move_to(0)
    axis_x.move_to(0)
    
    # axis1.move_by(1, True)
    # axis1.move_by(1.5, True)


    
    