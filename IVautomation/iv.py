import socket
    
#instantiate a socket
mySocket=socket.socket(socket.AF_INET, socket.SOCK_STREAM) 
#interface using port 5025 standard to all Keysight Equipment
mySocket.connect(('10.80.5.189', 5025)) 
mySocket.setsockopt(socket.IPPROTO_TCP, socket.TCP_NODELAY, 1) 
#set timeout
mySocket.settimeout(2) 
#send command
command = '*IDN?\n'
mySocket.send(command.encode('ASCII'))  
#read reply
print ('ID: ' + mySocket.recv(1024).decode('ASCII') )

mySocket.close() 
 
print 'complete :)'