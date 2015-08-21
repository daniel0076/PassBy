#!/usr/bin/env python3

import asyncio
import pymysql
import json

class MainServer(asyncio.Protocol):
    def __init__(self):
        asyncio.Protocol.__init__(self)
        self.conn = pymysql.connect(unix_socket="/run/mysqld/mysqld.sock", user='passby', passwd='howbangbang', db='passby')
        self.cur = self.conn.cursor()

    def Connect(self,BT_Addr):
        self.cur.execute("SELECT * FROM `users` WHERE `BT_Addr`=%s",(BT_Addr,))
        result=self.cur.fetchone()
        if result is None:
            response={'type':'conn_response','success':'false'}
        else:
            response={'type':'conn_response','success':'true'}
        response=json.dumps(response)
        return response.encode()

    def Register(self,request):
        succ_msg=json.dumps({'type':'register_response','success':'true'})
        fail_msg=json.dumps({'type':'register_response','success':'false'})
        try:
            self.cur.execute("INSERT INTO `users` (BT_Addr,name,identity,fb,line_id,ig,twitter) VALUES (%s,%s,%s,%s,%s,%s,%s)",(request.get('BT_Addr'),request.get('name'),request.get('identity'),request.get('fb'),request.get('line_id'),request.get('ig'),request.get('twitter'),))
            self.conn.commit()
            print('Register Succeed')
            return succ_msg.encode()
        except:
            print('Register Failed')
            return fail_msg.encode()

    def Query(self,BT_Addr):
        self.cur.execute("SELECT * FROM `users` WHERE `BT_Addr`=%s",(BT_Addr,))
        result=self.cur.fetchone()
        if result is None:
            response={'type':'query_response','success':'false'}
        else:
            response=result
        response=json.dumps(response)
        return response.encode()


    def inputHandler(self,json_request):
        request=json.loads(json_request)
        if request['type'] == 'conn':
            return self.Connect(request['mac'])
        elif request['type'] == 'register':
            return self.Register(request)
        elif request['type'] == 'query':
            return self.Query(request['mac'])
        else:
            print('resuest=',request['type'])
            return None

    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self,exc):
        print('Close the client socket')
        self.transport.close()

    def data_received(self, data):
        print(data)
        message = data.decode()
        res=self.inputHandler(message)
        print('Data received: {!r}'.format(message))
        #self.transport.write(data)
        self.transport.write(res)


loop = asyncio.get_event_loop()
# Each client connection will create a new protocol instance
coro = loop.create_server(MainServer, '0.0.0.0', 8888)
server = loop.run_until_complete(coro)

# Serve requests until CTRL+c is pressed
print('Serving on {}'.format(server.sockets[0].getsockname()))
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass

# Close the server
server.close()
loop.run_until_complete(server.wait_closed())
loop.close()
