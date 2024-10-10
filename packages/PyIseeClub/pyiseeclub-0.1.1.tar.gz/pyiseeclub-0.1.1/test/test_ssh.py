# -*- coding: utf-8 -*-
import pymysql

from isee_club.SSHTunnel import SshTunnel


def test_ssh():
    ssh = {
        'ssh_ip': 'jumpserver.net',
        'ssh_port': 2222,
        'ssh_username': '111',
        'ssh_password': '222'
    }
    s = SshTunnel(**ssh, remote_ip='127.0.0.1', remote_port=3306)
    s.start()
    return pymysql.connect(host='127.0.0.1',
                           user='root',
                           passwd='q111111',
                           port=s.local_bind_port,
                           db='isee')