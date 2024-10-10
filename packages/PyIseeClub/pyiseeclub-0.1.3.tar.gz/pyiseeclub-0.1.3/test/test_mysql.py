# -*- coding: utf-8 -*-
import pymysql

from PyIseeClub.SSHTunnel import SshTunnel
from PyIseeClub.mysql_club import mysql_tools


def get_conn():
    kwargs = {"group": "vaymobi", "hostname": "159.138.140.74", "username": "test", "password": "test#%76Ap3O",
              "hostport": "3306", "database": "vn_vaymobi_test"}
    hostname = kwargs.get('hostname', 'localhost')
    username = kwargs.get('username')
    password = kwargs.get('password')
    hostport = int(kwargs.get('hostport', 3306))
    database = kwargs.get('database')
    try:
        return pymysql.connect(host=hostname,
                               user=username,
                               passwd=password,
                               port=hostport,
                               db=database)
    except:
        ssh = {
            'ssh_ip': 'jumpserver.xinzhengkeji.net',
            'ssh_port': 2234,
            'ssh_username': 'hewanyun',
            'ssh_password': 'hewanyun#%4vCv53fSN'
        }
        s = SshTunnel(**ssh, remote_ip=hostname, remote_port=hostport)
        s.start()
        return pymysql.connect(host='127.0.0.1',
                               user=username,
                               passwd=password,
                               port=s.local_bind_port,
                               db=database)


mysql_conn = get_conn()
mt = mysql_tools(mysql_conn)
result = mt.fetch_all("select * from customer where id=1")
print(result)
result = mt.fetch_all("select * from customer where id=1")
print(result)
result = mt.db_name()
print(result)
mt.connect_close()
