#!/usr/bin/env python3

import asyncio
import pymysql
import json

class MainServer(asyncio.Protocol):
    def __init__(self):
        #call the origin constructor
        asyncio.Protocol.__init__(self)
        self.mac=""
        try:
            self.conn = pymysql.connect(unix_socket="/run/mysqld/mysqld.sock", user='passby', passwd='howbangbang', db='passby')
            self.cur = self.conn.cursor()
        except :
            print("Fatal Error!! Cannot connect to database")


    #user establish connnection
    def Connect(self,BT_Addr):
        self.cur.execute("SELECT * FROM `users` WHERE `BT_Addr`=%s",(BT_Addr,))
        result=self.cur.fetchone()
        if result is None:
            response={'type':'conn_response','success':'false'}
            print("user '{}' not in db, connect failed".format(self.mac))
        else:
            response={'type':'conn_response','success':'true'}
            self.mac=BT_Addr
            print("user '{}' connected successfully".format(self.mac))
        response=json.dumps(response)
        return response.encode()

    #user register
    def Register(self,request):
        succ_msg=json.dumps({'type':'register_response','success':'true'})
        fail_msg=json.dumps({'type':'register_response','success':'false'})
        try:
            self.cur.execute("INSERT INTO `users` (BT_Addr,name,identity,fb,line_id,ig,twitter) VALUES (%s,%s,%s,%s,%s,%s,%s)",(request.get('BT_Addr'),request.get('name'),request.get('identity'),request.get('fb'),request.get('line_id'),request.get('ig'),request.get('twitter'),))
            #need to commit the db
            self.conn.commit()
            print("user '{}' register succeed".format(request.get('BT_Addr')))
            return succ_msg.encode()
        except pymysql.err.IntegrityError as e:
            print("Register Failed!! DB error {}".format(e));
            return fail_msg.encode()
        except :
            print("user '{}' register failed".format(request.get('BT_Addr')))
            return fail_msg.encode()

    #query user data, return all data from the db
    def Query(self,BT_Addr):
        self.cur.execute("SELECT * FROM `users` WHERE `BT_Addr`=%s",(BT_Addr,))
        result=self.cur.fetchone()
        if result is None:
            response={'type':'query_response','success':'false'}
            print("user '{}' not found".format(BT_Addr))
        else:
            response=result
        response=json.dumps(response)
        return response.encode()

    def ReturnTags(self):
        fail_msg=json.dumps({'type':'tags_response','success':'false'})
        succ_response={'type':'tags_response','success':'true'}
        try:
            self.cur.execute("SELECT * FROM `tags` ORDER BY `class` ASC")
            result=self.cur.fetchall()
            succ_response['tags']=result
            succ_response=json.dumps(succ_response)
            return succ_response.encode()
        except:
            print("ERROR!! ReturnTags is not happy")
            return fail_msg.encode()

    def AddTag(self,tag):
        fail_msg=json.dumps({'type':'addtag_response','success':'false'})
        succ_msg=json.dumps({'type':'addtag_response','success':'true'})
        try:
            self.cur.execute("INSERT INTO `passby`.`user_tags` (`mac`, `tag`) VALUES ( %s, %s)",(self.mac,tag,))
            self.conn.commit()
            print("Tag {}-{} added".format(self.mac,tag));
            return succ_msg.encode()
        except pymysql.err.IntegrityError as e:
            print("AddTag Failed!! DB error {}".format(e));
            return fail_msg.encode()

    #parse the input request
    def inputHandler(self,json_request):
        fail_msg=json.dumps({'type':'input_response','success':'false'})
        reparse_msg=json.dumps({'type':'input_response','success':'reparse'})
        try:
            request=json.loads(json_request)
        except:
            print("WARNING!! input {} parse error, reparse".format(json_request))
            splited=json_request.split('\n')[:-1]
            print(splited)
            for item in splited:
                print("{} reparsed".format(item))
                self.inputHandler(item)
            return reparse_msg.encode()

        try:
            if request['type'] == 'conn':
                return self.Connect(request['mac'])
            elif request['type'] == 'register':
                return self.Register(request)
            elif request['type'] == 'query':
                return self.Query(request['mac'])
            elif request['type'] == 'tags':
                return self.ReturnTags()
            elif request['type'] == 'addtag':
                return self.AddTag(request['tag'])
            else:
                print("ERROR!! unknow request {}".format(request['type']))
                return fail_msg.encode()
        except KeyError as e:
                print("ERROR!! index '{}' not found".format(e))
                return fail_msg.encode()


    def connection_made(self, transport):
        peername = transport.get_extra_info('peername')
        print('Connection from {}'.format(peername))
        self.transport = transport

    def connection_lost(self,exc):
        print('Close the client socket')
        self.transport.close()

    def data_received(self, data):
        message = data.decode()
        print('Data received: {!r}'.format(message))
        res=self.inputHandler(message)
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
