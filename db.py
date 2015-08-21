#!/usr/bin/env python3
import pymysql

conn = pymysql.connect(unix_socket="/run/mysqld/mysqld.sock", user='passby', passwd='howbangbang', db='passby')
cur = conn.cursor()

cur.execute("SELECT * FROM users")

print(cur)

cur.close()
conn.close()
