#!/usr/bin/python
import os
import socket
from threading import Thread
from SocketServer import ThreadingMixIn

TCP_IP = '192.168.1.1'
TCP_PORT = 9001
BUFFER_SIZE = 1024*1024*10

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print " New thread started for "+ip+":"+str(port)

    def run(self):
        fname=self.sock.recv(1024)
        print "client Requested:",fname
        if (os.path.isfile(fname)==False):
            #print"no file"
            msgstr="-1"
            self.sock.send(msgstr)
        else:
            try:
                #print "file exist"
                msgstr=str(os.path.getsize(fname))
                #print "size=",msgstr
                self.sock.send(msgstr)
                fsize=int(self.sock.recv(1024))
                f = open(fname,'rb')
                f.seek(fsize)
                while True:
                    l = f.read(BUFFER_SIZE)
                    while (l):
                        self.sock.send(l)
                        #print('Sent ',repr(l))
                        l = f.read(BUFFER_SIZE)
                    if not l:
                        f.close()
                        self.sock.close()
                        break
            except IOError:
                pass  

tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcpsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
tcpsock.bind((TCP_IP, TCP_PORT))
threads = []

while True:
    tcpsock.listen(1)
    print "Waiting for incoming connections..."
    (conn, (ip,port)) = tcpsock.accept()
    print 'Got connection from ', (ip,port)
   
    newthread = ClientThread(ip,port,conn)
    newthread.start()
    threads.append(newthread)

for t in threads:
    t.join()


