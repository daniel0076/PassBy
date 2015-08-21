import socket
import json

addr=('140.113.27.54',8888)
payload={'type':'conn','mac':'test'}
reg={'type':'register','BT_Addr':'test2','identity':'user','fb':'fb11','line_id':'0098','ig':'gg','twitter':'tei','name':'gg'}

sock=socket.socket()
sock.connect(addr)
sock.send(json.dumps(reg).encode())
print(sock.recv(200))

