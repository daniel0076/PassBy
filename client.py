import socket
import json

addr=('140.113.27.54',8888)

conn={'type':'conn','mac':'test'}
query={'type':'query','mac':'test9'}
reg={'type':'register','BT_Addr':'test2','identity':'user','fb':'fb11','line_id':'0098','ig':'gg','twitter':'tei','name':'gg'}

tests={'conn':conn,'query':query,'reg':reg}

sock=socket.socket()
sock.connect(addr)

for k,v in tests.items():
    print("testing:{}\n".format(k))
    sock.send(json.dumps(v).encode())
    print("result:{}\n".format(sock.recv(200)))
print("end of test")
