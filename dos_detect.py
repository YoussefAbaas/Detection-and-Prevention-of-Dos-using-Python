import socket
import struct
from datetime import datetime
import os

def block_ip(IP):
        cmd='sudo route add '+IP+' reject'
        os.system(cmd)
        cmd='sudo iptables -A INPUT -s '+IP+' -j DROP > /dev/null 2>&1'
        os.system(cmd)
        cmd='sudo service iptables save > /dev/null 2>&1'
        os.system(cmd)
        cmd='sudo iptables -L > /dev/null 2>&1'
        os.system(cmd)
        print (IP,' has been blocked')

s=socket.socket(socket.PF_PACKET,socket.SOCK_RAW,8)
Dict=dict()
blocked_IP=set()
white_ip=('127.0.0.1')
file_txt = open("dos.txt","w")
t1 = str(datetime.now())
file_txt.writelines(t1)
file_txt.writelines("\n")
while True:
    pkt = s.recvfrom(2048)
    ipheader = pkt[0][14:34]
    ip_hdr = struct.unpack("!8sB3s4s4s",ipheader)
    IP = socket.inet_ntoa(ip_hdr[3])
    print("The Source of the IP is:", IP)
    if IP in Dict:
       Dict[IP]+=1
       print (Dict[IP])
    else :
       Dict[IP]=0
       print (Dict[IP])
    if(Dict[IP] >= 20):
        file_txt.flush()
        line = "DDOS attack is Detected: "
        file_txt.writelines(line)
        file_txt.writelines(IP)
        file_txt.writelines(" at ")
        file_txt.writelines(str(datetime.now()))
        file_txt.writelines("\n")
        print("DDOS attack is Detected")
        Dict[IP]=0
        block_ip(IP)
        blocked_IP.add(IP)
