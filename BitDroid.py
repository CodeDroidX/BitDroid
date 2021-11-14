import socket
import os
import hashlib
import base64
import time
import pyperclip
from colorama import Fore, init
from progress.bar import IncrementalBar
init(autoreset=True)

IP = '192.168.88.15' #Свой айпи
PORT = 8080 #не трогать

hasher = hashlib.new('sha512_256')
hasher.update(str(time.ctime(time.time())).encode("utf-8"))
hsh=hasher.hexdigest()
token=base64.b64encode(str([hsh[0]+hsh[1]+hsh[2]+hsh[3],IP,PORT]).encode("UTF-8")).decode("utf-8")

print(Fore.YELLOW+"Welcome to the BitDroid")

role = input("You are Client(1) or server(2)?")
if role=="1":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    print(Fore.CYAN+"Client Started!")
    token=input("Enter Server-Token>")
    token=token.encode("utf-8")
    token=base64.b64decode(token)
    token=token.decode("utf-8")
    token=eval(token)
    FIP=token[1]
    PORT=token[2]
    sock.connect((FIP, PORT))
    print(Fore.CYAN+str(FIP),'connected!')
    sock.settimeout(10)
if role=="2":
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.bind((IP, PORT))
    print(Fore.CYAN+"Server Started!")
    #print(Fore.GREEN+"Your Token is",token)
    print(Fore.GREEN+"Your token copied!")
    pyperclip.copy(token)
    sock.listen()
    sock, addr = sock.accept()
    print(Fore.CYAN+str(addr),'connected!')
    sock.settimeout(10)
    
print()
print(Fore.YELLOW+"Channel Opened")

role = input("You want to send(1) or get(2) file?")

def getSize(filename):
    st = os.stat(filename)
    return st.st_size



if role == "2":
    dir=input("Downloading Folder path:").strip("\"").strip("/").strip("\\")
    print()
    n=sock.recv(1024).decode("utf-8").strip(" ")
    """
    if os.path.isfile(dir+"\\"+n):
        sock.send(str(2).encode("utf-8"))
        maxblocks=int(sock.recv(1024).decode("utf-8").strip(" "))
        checklist=[]
        for hsh_num in range(maxblocks+1):
            checklist.append(sock.recv(64).decode("utf-8"))
        while 1:
            f = open(dir+"\\"+n, 'rb')
            f.seek(0)
            fn = open(dir+"\\"+n+"part", 'ab')
            mylist=[]
            for hsh_num in range(maxblocks+1):
                hasher = hashlib.new('sha512_256')
                f.seek(1000000*hsh_num, 0)
                block=f.read(1000000)
                hasher.update(block)
                mylist.append(hasher.hexdigest())
                
            if mylist==checklist:
                break
            else:
                print()
                print(mylist)
                print()
                print(checklist)
            for i in range(len(checklist)):
                my_hash=mylist[i]
                tr_hash=checklist[i]
                if my_hash==tr_hash:
                    fn.write(block)
                else:
                    sock.send(str(1).encode("utf-8"))
                    sock.send(str(i).ljust(32).encode("utf-8"))
                    fn.write(sock.recv(1000000))
                    sock.recv(64)
            f.close()
            fn.close()
            os.remove(dir+"\\"+n)
            os.rename(dir+"\\"+n+"part", dir+"\\"+n)
            """
    f = open(dir+"\\"+n, 'wb')
    sock.send(str(0).encode("utf-8"))
    maxblocks=int(sock.recv(1024).decode("utf-8").strip(" "))
    bar=IncrementalBar('Downloading', max = maxblocks+1)
    for block_num in range(maxblocks+1):
        while 1:
            hasher = hashlib.new('sha512_256')
            sock.send(str(1).encode("utf-8"))
            sock.send(str(block_num).ljust(32).encode("utf-8"))
            block=sock.recv(1000000)
            hasher.update(block)
            my_hash=hasher.hexdigest()
            tr_hash=sock.recv(64).decode("utf-8")
            if my_hash==tr_hash:
                f.write(block)
                bar.next()
                break
    sock.send(str(5).encode("utf-8"))
    f.close()
    
if role == "1":
    pth=input("File to send path:").strip("\"")
    print()
    sock.send(str(os.path.basename(pth)).ljust(1024).encode("utf-8"))
    f = open(pth, 'rb')
    while 1:
        task=sock.recv(1).decode("utf-8")
        if task=="0":
            sz=int(int(getSize(pth))/1000000)
            sock.send(str(sz).encode("utf-8").ljust(1024))
            bar=IncrementalBar('Sharing', max = sz+1)
        if task=="2":
            checklist=[]
            sz=int(int(getSize(pth))/1000000)
            sock.send(str(sz).encode("utf-8").ljust(1024))
            for block_num in range(sz+1):
                hasher = hashlib.new('sha512_256')
                f.seek(1000000*int(block_num), 0)
                block=f.read(1000000)
                hasher.update(block)
                checklist.append(hasher.hexdigest())
            for hsh in checklist:
                sock.send(hsh.encode("utf-8"))
        if task=="1":
            f.seek(1000000*int(sock.recv(32).decode("utf-8").strip(" ")), 0)
            block=f.read(1000000)
            if block:
                sock.send(block)
                hasher = hashlib.new('sha512_256')
                hasher.update(block)
                sock.send(hasher.hexdigest().ljust(64).encode("utf-8"))
                try:
                    bar.next()
                except:
                    pass
        if task=="5":
            break
    f.close()
print()
print(Fore.YELLOW+"Work Finished!")
        