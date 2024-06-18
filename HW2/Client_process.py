import socket
import time

commchoice = 0
def GUI():
    print("Welcome to Message Creater Interface for the Client Process!")
    print("Message formats: OPCODE IND = Ind1,Ind2,...,IndN DATA=Dat1,Dat2,...,DatN;")
    print("To create valid message, choose valid opcode and index/indices\n")
    print("For the Opcode choice: ")

    print("0: GET (Request for the values of the specified indices)")
    print("1: SET (Request for updating the values of the specified indices)")
    print("2: RESET (Clear the whole table for the proxy / Reset each index on the back end server to data)")
    print("3: EVICT (Evict from the proxy table)")

    inp = input("Choose the opcode: ")
    opcode = int(inp)

    while(opcode < 0 or opcode > 3):
        inp = input("Choose the opcode with a valid number!: ")
        opcode = int(inp)
    
    if(opcode == 0): #GET
        msg = "GET IND="
        
        inp = input("Enter the number of indices that will be chosen: ")
        numIndex = int(inp)

        while(numIndex < 1 or numIndex > 10):
            inp = input("Choose the number of indices with a valid number (1-10)!: ")
            numIndex = int(inp)
        
        for i in range(numIndex):
            inp = input("Enter the indices one by one with valid numbers: ")
            index = int(inp)
            while(index < 0 or index > 9):
                inp = input("Last number is invalid. Enter a valid number to choose index(0-9)!: ")
                index = int(inp)
            if(i == numIndex-1):
                msg = msg + inp + ";"
            else:
                msg = msg + inp + ","
    
    elif(opcode ==1): #SET
        msg = "SET IND="
        
        inp = input("Enter the number of data that will be set: ")
        numData = int(inp)        
        while(numData < 1 or numData > 10):
            inp = input("Choose a valid number to set data! (1-10)!: ")
            numData = int(inp)
        DATA =[]
        for i in range(numData):
            inp = input("Enter the indices one by one with valid numbers: ")
            index = int(inp)
            while(index < 0 or index > 9):
                inp = input("Last number is invalid. Enter a valid number to choose index (0-9)!: ")
                index = int(inp)
            if(i == numData-1):
                msg = msg + inp + " "
            else:
                msg = msg + inp + ","
            value = input("Enter the data value for this index: ")
            data = int(value)
            DATA.append(data)
        msg = msg + "DATA="
        for i in range(numData):
            if(i == numData-1):
                msg = msg + str(DATA[i]) + ";"
            else:
                msg = msg + str(DATA[i]) + ","

    elif(opcode == 2): #RESET
        msg = "RESET"

        choice = int(input("Enter 1 for reset the all data to certain value, 0 for reset the all data to empty: "))
        while(choice !=1 and choice !=0):
            choice = int(input("Invalid input. Enter 1 for reset to a value, 0 for reset to empty: "))
        if(int(choice)):
            value = input("Enter the value to which all data reset: ")
            msg = msg + " DATA=" + str(value) + ";"
        else:
            msg = msg + ";"
    
    else: #EVICT
        msg = "EVICT"

        choice = int(input("Enter 1 for evict the chosen indices, 0 for evict the all indices: "))
        while(choice !=1 and choice !=0):
            choice = int(input("Invalid input. Enter 1 for reset to a value, 0 for reset to empty: "))
        if(int(choice)):
            msg = msg + " IND="
            inp = input("Enter the number of indices that will be chosen: ")
            numIndex = int(inp)

            while(numIndex < 1 or numIndex > 10):
                inp = input("Choose the number of indices with a valid number (1-10)!: ")
                numIndex = int(inp)
            
            for i in range(numIndex):
                inp = input("Enter the indices one by one with valid numbers: ")
                index = int(inp)
                while(index < 0 or index > 9):
                    inp = input("Last number is invalid. Enter a valid number to choose index(0-9)!: ")
                    index = int(inp)
                if(i == numIndex-1):
                    msg = msg + inp + ";"
                else:
                    msg = msg + inp + ","
        else:
            msg = msg + ";"
    return msg
                                    
#Loopback IP address
HOST_PROXY = '127.0.0.1'
PORT_PROXY = 6003
client_socket_proxy = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket_proxy.connect((HOST_PROXY,PORT_PROXY))

HOST_SERVER = '127.0.0.1'
PORT_SERVER = 6001

#Create sockets for proxy and server

controlSocket = "NOP"

while True:
    commchoice = input("Firstly you should choose 1 for communication directly with Server or 0 for communication with Proxy: ")
    while(commchoice != "1" and commchoice != "0"):
        commchoice = input("Enter valid number to choose communication way!: ")
    msg = GUI()
    if(commchoice == "0"):
        print("Message sent by client to proxy: ")
        print(msg)       
        client_socket_proxy.sendall(bytes(msg,'utf-8'))
        time.sleep(0.5)

        dataReceived_proxy=client_socket_proxy.recv(1024)
        print("Received Message from Proxy is:")
        print(dataReceived_proxy)
        #Decode the data into a string
        dataReceived_proxy = dataReceived_proxy.decode('utf-8')
        print("Decoded Message is:")
        print(dataReceived_proxy)
    
    elif(commchoice == "1"):
        client_socket_server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket_server.connect((HOST_SERVER,PORT_SERVER))
        print("Message sent by client to server: ")
        print(msg)
        client_socket_server.sendall(bytes(msg,'utf-8'))
        time.sleep(0.5)

        dataReceived_server=client_socket_server.recv(1024)
        print("Received Message from Server is:")
        print(dataReceived_server)
        #Decode the data into a string
        dataReceived_server = dataReceived_server.decode('utf-8')
        print("Decoded Message is:")
        print(dataReceived_server)
        client_socket_server.close()

