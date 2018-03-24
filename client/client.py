#!/usr/bin/env python
import os
import socket
import sys

TCP_IP = raw_input("Source IP:")
TCP_PORT = 9001
BUFFER_SIZE = 1024	

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
fname=raw_input("Source File Name:")
s.send(fname)
fsize = int(s.recv(BUFFER_SIZE))

if(fsize == -1):
	print "No file found"
else:
	if (os.path.isfile(fname)==False):
		s.send("0")
	else:
		fSeekPtr=str(os.path.getsize(fname))
		s.send(fSeekPtr)	
	with open(fname, 'ab') as f:
	    #print 'file opened'
	    while True:
	        #print('receiving data...')
	        data = s.recv(BUFFER_SIZE)
		        
		if not data:
	            f.close()
	            #print 'file close()'
	            break
	        # write data to a file
	        f.write(data)
	print('Successfully downloaded file')

s.close()
print('connection closed')
