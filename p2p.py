from socket import *
import threading
import time
from os.path import exists
import os
import sys
from collections import deque
import select
# import mmh3

# ID, Name
print("Student ID : 20181612", flush = True)
print("Name : Byeonggyu Park", flush = True)

serverPort = int(sys.argv[1])
userid = int(sys.argv[2]) # my id
username = sys.argv[3]
serverSocket = socket(AF_INET,SOCK_STREAM)
serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR,1)
serverSocket.bind(('',serverPort))
serverSocket.listen(1)
info = []
info2 = set()
command_arr = [serverSocket, sys.stdin]
#print(str(sys.stdin))
num = 0
IP_address = "127.0.0.1"
qseq = 0
client_msg = ""


while True :
    read, write, exc = select.select(command_arr, [], [])
    #print(read)
    for c in read :
        # command
        if c == sys.stdin :
            #print(c, type(c))
            #print(sys.stdin)
            cmd = c.readline().split(' ')
            if cmd[0] == "@connect" :
                hostname = cmd[1]
                tcpport = cmd[2]
                print(cmd[0] + hostname +  tcpport)
                clientSocket = socket(AF_INET, SOCK_STREAM)
                clientSocket.connect((hostname, int(tcpport)))
                if clientSocket not in command_arr :
                    command_arr.append(clientSocket)
                if (userid, qseq, clientSocket) not in info :
                    info.append((userid, qseq, clientSocket))
                #info2.add((int(tcpport), qseq, clientSocket))
                print("@Connect", info)
                print("@Connect command_arr", command_arr)
            elif cmd[0] == "@query" :
                print(cmd[0] + cmd[1])
                # 검색을 하고자 하는 사용자 아이디.
                qseq += 1
                hop = 0 # number of forwarding
                visited = ""
                pid = int(cmd[1]) # id"
                if str(userid) == str(pid) :
                    message = "PeerInfo src " + userid + " target " + str(pid) + " name " + username + " IP " + IP_address + " port " + str(serverPort) + " hop " + str(hop) + " " + qseq
                    if (userid, qseq, c) not in info :
                        info.append((userid, qseq, c))
                    continue
                else :
                    hop += 1
                    #query_msg = "QUERY " + str(userid) + " " + str(qseq) + " " + str(hop) + " " + str(pid)
                    for socket in command_arr[2:] :
                        query_msg = "QUERY " + str(userid) + " " + str(qseq) + " " + str(hop) + " " + str(pid)
                        print("query_msg 76:", query_msg)
                        socket.sendall(query_msg.encode('ascii'))
                    if (userid, qseq, c) not in info :
                        info.append((userid, qseq, c))
                    print("send_Query")

            elif cmd[0] == "@quit\n" :
                print(cmd[0])
                #print()
                serverSocket.close()
                exit()
            else :
                print("wrong")
                continue
        # server 
        elif c == serverSocket :
            connectionSocket, addr = serverSocket.accept()
            if connectionSocket not in command_arr :
                command_arr.append(connectionSocket)
            #print("server connect")
        else :
            msg = c.recv(1024).decode('utf-8')
            if len(msg) == 0 :
                print("not send")
                break
            msg_arr = msg.split(' ')
            #print("arr", msg_arr)
                # Query
                # msg_userid = msg_arr[1]
                # msg_qseq = msg_arr[2]
                # msg_hop = msg_arr[3]
                # msg_pid = msg_arr[4]
            if msg_arr[0] == "QUERY" :
                #print("96")
                key1 = msg_arr[1] #10
                key2 = msg_arr[2] # 1
                key_list = []
                for i in range(len(info)) : 
                    key_list.append(str(info[i][0]) + str(info[i][1]))
                if str(msg_arr[1]) + str(msg_arr[2]) not in key_list :
                    if (msg_arr[1], msg_arr[2], c) not in info :
                        info.append((msg_arr[1], msg_arr[2], c))
                    #print("info", info)
                else :
                    #print("break")
                    break
                        
                if str(userid) == msg_arr[4] :
                    #send_msg = "PeerInfo src " + msg_arr[1] + " target " + msg_arr[4]+ " name " + username + " IP " + IP_address + " port " + str(serverPort) + " hop " + msg_arr[3] + " qseq " + msg_arr[2]
                    print("QUERYHIT")
                    client_msg = msg
                    #print("108",send_msg)
                    for x in info:
                        if msg_arr[1] == str(x[0]) and msg_arr[2] == str(x[1]) :
                            send_msg = "PeerInfo src " + msg_arr[1] + " target " + msg_arr[4]+ " name " + username + " IP " + IP_address + " port " + str(serverPort) + " hop " + msg_arr[3] + " qseq " + msg_arr[2]
                            print("send_msg 136", send_msg)
                            x[2].sendall(send_msg.encode('ascii'))
                    break

                    #print("info", info)
                    #sss.sendall(send_msg.encode('ascii'))

                else :
                    #send_msg = "QUERY " + msg_arr[1] + " " + msg_arr[2] + " " + str(int(msg_arr[3])+1) + " " + msg_arr[4]
                    #print("143:", send_msg)
                    for socket in command_arr[2:] :
                        if socket != c :
                            send_msg = "QUERY " + msg_arr[1] + " " + msg_arr[2] + " " + str(int(msg_arr[3])+1) + " " + msg_arr[4]
                            socket.sendall(send_msg.encode('ascii'))
                        else : 
                            continue
            else :
                    # msg_userid = msg_arr[1]
                    # msg_pid = msg_arr[3]
                    # username= msg_arr[5]
                    # IP_address = msg_arr[7]
                    # tcpport = msg_arr[9]
                    # hop = msg_arr[11]
                    # qseq = msg_arr[13]
                    #print("msg",msg)
                #print(msg_arr)
                
                if str(userid) == msg_arr[2] :
                        #print(msg)
                    ttt = msg.find(" qseq")
                    print(msg[:ttt])
                    break
                else :
                    # info qs, qseq find socket
                    #print("142:",msg_arr)
                    for x in info :
                        if str(x[0]) == msg_arr[2] and str(x[1]) == msg_arr[14] :
                            x[2].sendall(msg.encode('ascii'))
                        else :
                            continue
                # except :
                #     # ttt = msg.find(" qseq")
                #     # #print(msg[:ttt])
                #     print("execpt")
                #     continue
                    #pass