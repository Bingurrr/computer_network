from socket import *
import sys

# ID, Name
print("Student ID : 20181612")
print("Name : Byeonggyu Park")

def main(argv) :
    #serverName = "netapp.cs.kookmin.ac.kr"
    #serverPort = 80
    serverName = argv[1]
    serverPort = int(sys.argv[2])
    path = argv[3]
    fileName = list(path.split('/'))[-1]
    #print(path)
    clientSocket = socket(AF_INET, SOCK_STREAM)
    try :
        clientSocket.connect((serverName,serverPort))
    except :
        print(serverName+": unknown host")
        exit()
    #sentence = raw_input('Input lowercase sentence:')

    #end_str = "\r\n"
    sentence = bytes("GET " + path + " HTTP/1.0\r\nHost: "+serverName+"\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n", 'utf-8')
    print(sentence)
    #sentence = b"GET /member/palladio.JPG HTTP/1.0\r\nHost: netapp.cs.kookmin.ac.kr\r\nUser-agent: HW1/1.0\r\nConnection: close\r\n\r\n"
    clientSocket.sendall(sentence)

    ## first input
    while True :
        modifiedSentence = clientSocket.recv(1024)
        if b"\r\n\r\n" in  modifiedSentence :
            break

    full_byte = []
    """
        name
        cl : Content-Length
        msg_num : 200, 404, etc...
        msg : not found, Moved Permanently etc ..
    """
    arr = list(modifiedSentence.split(b"\r\n\r\n"))
    #print(arr[0])
    num = ["0","1","2","3","4","5","6","7","8","9"]
    cl_arr = list(arr[0].decode('utf-8').split("Content-Length: "))
    str_cl = ""
    for i in range(len(cl_arr[1])) :
        if cl_arr[1][i] in num :
            str_cl += cl_arr[1][i]
        else :
            break
    #print(str_cl)
    cl = int(str_cl)
    #print(arr[0])
    msg_arr = list(arr[0].decode('utf-8').split("\r\n"))
    #print(msg_arr)
    msg_arr2 = msg_arr[0].split('HTTP/1.')
    #print(msg_arr2)
    msg_arr3 = msg_arr2[1].split()
    #print("3", msg_arr3)
    msg_num = msg_arr3[1]
    msg_num = msg_num
    msg = ""
    for i in range(2,len(msg_arr3)) :
        msg += msg_arr3[i] + " "

    if msg_num != "200" :
        print(msg_num + " " +msg)
        exit()
    #print(msg_num)
    #print(msg)


    print("Total Size",cl, "bytes")
    with open(fileName, "wb") as file :
        check = 10
        present = len(arr[1])
        file.write(arr[1])
        while True :
            modifiedSentence = clientSocket.recv(1024)
            present += len(modifiedSentence)
            #print(len(modifiedSentence))
            file.write(modifiedSentence)
            if 100 * (present/cl) >= check :
                check += 10
                print("Current Downloading ",str(present)+"/"+str(cl)," (bytes) ",str(int(100 * round((present/cl),1)))+"%")
            if present == cl :
                print("Download Complete: "+fileName+",",str(present)+"/"+str(cl) )
                break


    #print('From Server:', modifiedSentence)

    clientSocket.close()

if __name__ == "__main__" :
    main(sys.argv)