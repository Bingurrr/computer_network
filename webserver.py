from socket import *
from os.path import exists
import os
import sys


# ID, Name
print("Student ID : 20181612", flush = True)
print("Name : Byeonggyu Park", flush = True)

def main(argv) :
    serverPort = int(argv[1])
    serverSocket = socket(AF_INET,SOCK_STREAM)
    serverSocket.bind(('',serverPort))
    serverSocket.listen(1)

    while True :
        header = ""
        agent = ""
        content_type = ""
        connectionSocket, addr = serverSocket.accept()

        while True :
            sentence = connectionSocket.recv(1).decode('utf-8')
            header += sentence
            if "\r\n\r\n" in header :
                break
        #print(header)
        # tmp = connectionSocket.recv(1024).decode('utf-8')
        # total_tmp = tmp
        # while tmp :
        #     tmp = connectionSocket.recv(1024).decode('utf-8')
        #     total_tmp += tmp
        # print(total_tmp)
        #print("header: ", header)
        getline =  header.split("\r\n")[0]
        #print(filename)
        arr = header.split('\r\n')
        filename = arr[0].split(' ')[1][1:]
        header_count = len(arr) - 3
        for s in arr :
            if "User-Agent:" in s :
                agent = s.split(' ')[1]
                #print("agent"+agent, flush = True)
            elif "Accept:" in s :
                content_type = s.split(' ')[1].split(',')[0]
        print("Connection : Host IP %s, Port %d, socket %d" %(addr[0], int(addr[1]), connectionSocket.fileno()),flush=True)
        print(getline ,flush=True)
        print("User-Agent: " + agent,flush=True)
        print(f"{header_count} headers",flush=True)


        dsize = 0
        fsize = 0
        
        if exists(filename) :
            fsize = os.path.getsize(filename)
            if '.jpg' in filename : 
                content_type = "image/jpeg"
                response_message = 'HTTP/1.0 200 OK\r\nConncetion: close\r\nContent-Length: %d\r\nContent-Type: %s\r\n\r\n' % (fsize, content_type)
            else :
                response_message = 'HTTP/1.0 200 OK\r\nConncetion: close\r\nContent-Length: %d\r\nContent-Type: %s\r\n\r\n' % (fsize, content_type)
            connectionSocket.sendall(response_message.encode('ascii'))
            with open(filename, 'rb') as f :
                data = f.read(1024)
                total_data = data
                while data :
                    dsize += len(data)
                    #if a == dsize : break
                    connectionSocket.sendall(data)
                    data = f.read(1024)
                    total_data += data
                
                    #a = dsize
                #encoded_img = np.fromstring(total_data, dtype = np.uint8)
                #img = cv2.imdecode(encoded_img, cv2.IMREAD_COLOR)
                #cv2.imshow("image", img)
                #cv2.waitKey()
                #print(type(total_data))
                #print("data", total_data, flush = True)
                #cv2.imshow("image", cv2.imdecode(total_data,1))
        else :
            print(f"Server Error : No such file {filename}!", flush=True)
            response_message = 'HTTP/1.0 404 NOT FOUND\r\nConncetion: close\r\nContent-Length: 0\r\nContent-Type: text/html\r\n\r\n'
            connectionSocket.sendall(response_message.encode('ascii'))


        print(f"finish {dsize} {fsize}", flush = True)
        print("Connection : Host IP %s, Port %d, socket %d" %(addr[0], int(addr[1]), connectionSocket.fileno()), flush = True)

if __name__ == "__main__" :
    main(sys.argv)