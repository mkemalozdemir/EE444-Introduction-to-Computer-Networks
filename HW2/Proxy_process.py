import socket
import time
import re

Proxy_Table_Index = []
Proxy_Table_Data = []

not_have_idx = []

ind = [] #Incoming indexes
dt = [] #Incoming data

cacheIndex = []
cacheData = []

op = -1
cacheOp = " "


#Loopback IP address
HOST_CLIENT = '127.0.0.1'
PORT_CLIENT = 6003
#Create Server for communication with Client
proxy_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ("Socket successfully created")
# This line avoids bind() exception: OSError: [Errno 48] Address already in use as you configure address reuse
proxy_server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
proxy_server_socket.bind((HOST_CLIENT, PORT_CLIENT))
print ("Socket is bound to IP:",HOST_CLIENT," PORT:",PORT_CLIENT)
proxy_server_socket.listen(1)
print("Listening for connections")
conn, clientAddress = proxy_server_socket.accept()
print ('Connected ', clientAddress)

#Loopback IP address
HOST_SERVER = '127.0.0.1'
PORT_SERVER = 6001
#Create Client to communicate with Server


def printProxyTable():
    print("*****PROXY TABLE*****")
    for i in range(len(Proxy_Table_Index)):
        print(str(Proxy_Table_Index[i]) + "\t" + str(Proxy_Table_Data[i]))
    

def ParseServerMessage(message):
    
    global cacheIndex
    global cacheData

    parsedMessage = []

    parsedMessage = re.split(' |=|,|;',message)
    cacheOp = parsedMessage[0]
    cacheIndex.clear()
    cacheData.clear()
    i = 2
    if(op == 0):
        while(parsedMessage[i] != "DATA" and i < (len(parsedMessage)-1)):
            cacheIndex.append(int(parsedMessage[i]))
            i = i + 1
        i = i + 1
        while(i < len(parsedMessage)-1):
            cacheData.append(int(parsedMessage[i]))
            i = i + 1
    return cacheOp

def ParseClientMessage(message):
    parsedMessage = []
    global op
    global ind
    global dt
    parsedMessage = re.split(' |=|,|;', message)
    ind.clear()
    dt.clear()
    if(parsedMessage[0] == "GET"):
        op = 0
        i = 2
        while(i < len(parsedMessage)-1):
            ind.append(int(parsedMessage[i]))
            i = i + 1
    elif(parsedMessage[0] == "SET"):
        op = 1
        i = 2
        while(parsedMessage[i] != "DATA"):
            ind.append(int(parsedMessage[i]))
            i = i + 1
        i = i + 1
        while(i < len(parsedMessage)-1):
            dt.append(int(parsedMessage[i]))
            i = i + 1
    elif(parsedMessage[0] == "RESET"):
        op = 2
        if(len(parsedMessage) > 2):
            dt.append(int(parsedMessage[2]))
    elif(parsedMessage[0] == "EVICT"):
        op = 3
        if(len(parsedMessage) > 2):
            i = 2
            while(i < len(parsedMessage)-1):
                ind.append(int(parsedMessage[i]))
                i = i + 1
        else:
            ind.append(-1)
    else:
        op = -1


def checkProxy():
    global not_have_idx
    not_have_idx.clear()
    for item in ind:
        if item not in Proxy_Table_Index and item not in not_have_idx:
            not_have_idx.append(item)
    if(len(not_have_idx) == 0):
        not_have_idx.append(-1)

def updateProxy():
    global Proxy_Table_Index
    global Proxy_Table_Data
    global cacheIndex
    global cacheData
    if(op == 1):       
        cacheIndex = ind.copy()
        cacheData = dt.copy()
    for item in cacheIndex:
        if item not in Proxy_Table_Index:
            if(len(Proxy_Table_Index) == 5):
                Proxy_Table_Index = Proxy_Table_Index[1:]
                Proxy_Table_Data = Proxy_Table_Data[1:]

                Proxy_Table_Index.append(int(cacheIndex[cacheIndex.index(item)]))
                Proxy_Table_Data.append(int(cacheData[cacheIndex.index(item)]))
            else:
                Proxy_Table_Index.append(int(cacheIndex[cacheIndex.index(item)]))
                Proxy_Table_Data.append(int(cacheData[cacheIndex.index(item)]))
        else:
            del Proxy_Table_Data[Proxy_Table_Index.index(item)]
            del Proxy_Table_Index[Proxy_Table_Index.index(item)]
            Proxy_Table_Index.append(int(cacheIndex[cacheIndex.index(item)]))
            Proxy_Table_Data.append(int(cacheData[cacheIndex.index(item)]))


def getProxy():
    msg = "OK IND="
    checkProxy()
    if(not_have_idx[0] != -1):
        proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        proxy_client_socket.connect((HOST_SERVER,PORT_SERVER))
        msg2Server = "GET IND="
        for i in range(len(not_have_idx)):
            if(i == len(not_have_idx)-1):
                msg2Server = msg2Server + str(not_have_idx[i]) + ";"
            else:
                msg2Server = msg2Server + str(not_have_idx[i]) + ","
        while True:
            print("Message sent by proxy to server: ")
            print(msg2Server)
            proxy_client_socket.sendall(bytes(msg2Server,'utf-8'))
            time.sleep(0.5)

            msgReceivedFromServer = proxy_client_socket.recv(1024)
            print("New Table message is received from Server")
            print(msgReceivedFromServer)
            msgReceivedFromServer = msgReceivedFromServer.decode('utf-8')
            print("Decoded Message is:")
            print(msgReceivedFromServer)  

            if(ParseServerMessage(msgReceivedFromServer) == "OK"):       
                for i in range(len(ind)):
                    if(i == len(ind)-1):
                        msg = msg + str(ind[i]) + " "
                    else:
                        msg = msg + str(ind[i]) + ","
                msg = msg + "DATA="
                for i in range(len(ind)):
                    for j in range(len(Proxy_Table_Index)):
                        if(ind[i] == Proxy_Table_Index[j]):
                            if(i == len(ind)-1): 
                                msg = msg + str(Proxy_Table_Data[j]) + ";"
                            else:
                                msg = msg + str(Proxy_Table_Data[j]) + ","
                    for k in range(len(cacheIndex)):
                        if(ind[i] == cacheIndex[k]):
                            if(i == len(ind)-1):
                                msg = msg + str(cacheData[k]) + ";"
                            else:
                                msg = msg + str(cacheData[k]) + ","

                updateProxy()
                printProxyTable()
                break
        proxy_client_socket.close()
    else:
        for i in range(len(ind)):
            if(i == len(ind)-1):
                msg = msg + str(ind[i]) + " "
            else:
                msg = msg + str(ind[i]) + ","
        msg = msg + "DATA="

        for i in range(len(ind)):
            for j in range(len(Proxy_Table_Index)):
                if(ind[i] == Proxy_Table_Index[j]):
                    if(i == len(ind)-1):
                        msg = msg + str(Proxy_Table_Data[j]) + ";"
                    else:
                        msg = msg + str(Proxy_Table_Data[j]) + ","
    return msg

def setProxy():
    global Proxy_Table_Index
    global Proxy_Table_Data
    msg2Client = "OK;"
    msg2Server = "SET IND="
    proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_client_socket.connect((HOST_SERVER,PORT_SERVER))
    for i in range(len(ind)):
        if(i == len(ind)-1):
            msg2Server = msg2Server + str(ind[i]) + " "
        else:
            msg2Server = msg2Server + str(ind[i]) + ","
    msg2Server = msg2Server + "DATA="
    
    for i in range(len(dt)):
        if(i == len(dt)-1):
            msg2Server = msg2Server + str(dt[i]) + ";"
        else:
            msg2Server = msg2Server + str(dt[i]) + ","       
    while True:
        print("Message sent by proxy to server: ")
        print(msg2Server)
        proxy_client_socket.sendall(bytes(msg2Server,'utf-8'))
        time.sleep(0.5)

        msgReceivedFromServer = proxy_client_socket.recv(1024)
        print("New Table message is received from Server")
        print(msgReceivedFromServer)
        msgReceivedFromServer = msgReceivedFromServer.decode('utf-8')
        print("Decoded Message is:")
        print(msgReceivedFromServer)

        if(ParseServerMessage(msgReceivedFromServer) == "OK"):
            updateProxy()
            printProxyTable()
            break
    proxy_client_socket.close()
    return msg2Client

def resetProxy():

    msg2Client = "OK;"
    msg2Server = ""

    proxy_client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    proxy_client_socket.connect((HOST_SERVER,PORT_SERVER))
    
    if(len(dt) != 0):
        msg2Server = "RESET DATA=" + str(dt[0]) + ";"
        for i in range(len(Proxy_Table_Data)):
            Proxy_Table_Data[i] = dt[0]
    else:
        msg2Server = "RESET;"
        for i in range(len(Proxy_Table_Data)):
            Proxy_Table_Data[i] = ""
    while True:
        print("Message sent by proxy to server: ")
        print(msg2Server)
        proxy_client_socket.sendall(bytes(msg2Server,'utf-8'))
        time.sleep(0.5)

        msgReceivedFromServer = proxy_client_socket.recv(1024)
        print("New Table message is received from Server")
        print(msgReceivedFromServer)
        msgReceivedFromServer = msgReceivedFromServer.decode('utf-8')
        print("Decoded Message is:")
        print(msgReceivedFromServer)
        if(msgReceivedFromServer == "OK;"):
            printProxyTable()
            break
    proxy_client_socket.close()
    return msg2Client 

def evictProxy():
    global Proxy_Table_Index
    global Proxy_Table_Data
    msg = "OK;"

    if(ind[0] == -1):
        Proxy_Table_Index.clear()
        Proxy_Table_Data.clear()
        printProxyTable()
    else:
        for i in range(len(ind)):
            del Proxy_Table_Data[Proxy_Table_Index.index(ind[i])]
            del Proxy_Table_Index[Proxy_Table_Index.index(ind[i])]
        printProxyTable()
    return msg       


while True:
    
    try:
        msgReceived_client = conn.recv(1024)
    except:
        print (clientAddress, 'disconnected')
        proxy_server_socket.listen(1)
        conn, clientAddress = proxy_server_socket.accept()
        print ('Connected by', clientAddress)
        time.sleep(0.5)
    else:
        print("Client Message is:")
        #Initial data should be a byte object with utf-8 encoding
        print(msgReceived_client)
        #Decode the data into a string
        msgReceived_client = msgReceived_client.decode('utf-8')
        print("Decoded Message from Client is:")
        print(msgReceived_client)

        ParseClientMessage(msgReceived_client)
        if(op == 0):
            msgSent2Client = getProxy()
            print("Message sent by proxy to client: ")
            print(msgSent2Client)
            conn.sendall(bytes(msgSent2Client,'utf-8'))
        elif(op == 1):
            msgSent2Client = setProxy()
            print("Message sent by proxy to client: ")
            print(msgSent2Client)
            conn.sendall(bytes(msgSent2Client,'utf-8'))
        elif(op == 2):
            msgSent2Client = resetProxy()
            print("Message sent by proxy to client: ")
            print(msgSent2Client)
            conn.sendall(bytes(msgSent2Client,'utf-8'))
        elif(op == 3):
            msgSent2Client = evictProxy()
            print("Message sent by proxy to client: ")
            print(msgSent2Client)
            conn.sendall(bytes(msgSent2Client,'utf-8'))
            
