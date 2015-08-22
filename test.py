import socket
import json

addr=('140.113.27.54',8888)

conn={'type':'conn','mac':'test'}
query={'type':'query','mac':'test9'}
reg={'type':'register','BT_Addr':'test5','identity':'user','fb':'fb11','line_id':'0098','ig':'gg','twitter':'tei','name':'gg'}
tags={'type':'tags'}
addtag={'type':'addtag','tag':'tennis'}
usertags={'type':'usertags'}

tests={'tags':tags,'query':query,'reg':reg,'addtag':addtag,'usertags':usertags}

sock=socket.socket()
sock.connect(addr)

print("connecting...")
sock.send(json.dumps(conn).encode())
print("result:{}\n".format(sock.recv(1024)))

for k,v in tests.items():
    print("testing:{}".format(k))
    sock.send(json.dumps(v).encode())
    print("result:{}\n".format(sock.recv(1024)))
print("end of test")
