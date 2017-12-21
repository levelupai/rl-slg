# -*- coding: utf-8 -*-
import time
import socket
import threading
import json
import ste_pb2 as sp
from Queue import Queue
from struct import pack, unpack

# Sorry, we can not to provide the real server IP here.
SERVER_ADR = ("127.0.0.1", 9527)


class TcpClient(threading.Thread):
    def __init__(self, user_client):
        super(TcpClient, self).__init__()
        self.user_client = user_client
        self.sock = None
        self.opened = False
        self.HEAD_LENGTH = 48

    def open(self):
        self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.sock.connect(SERVER_ADR)
        self.opened = True

    def recv(self):
        head_length = self.HEAD_LENGTH
        recv_af = AppFrame()
        recv_af.message = sp.CsInfo()
        try:
            head = ""
            while True:
                head += self.sock.recv(head_length - len(head))
                if head_length == len(head):
                    break
            if not head:
                return
            recv_af.frame_head_decode(head)
            body_length = int(recv_af.frame_length) - self.HEAD_LENGTH
            if body_length <= 0:
                return
            body = ""
            while True:
                body += self.sock.recv(body_length - len(body))
                if body_length == len(body):
                    break
            if not body:
                return
            recv_af.decode(body)
        except Exception,e:
            logging.debug(e)
            return
        self.user_client.on_message(recv_af.message)

    def send(self, send_af):
        msg = send_af.encode()
        self.sock.send(msg)

    def close(self):
        self.sock.close()
        self.opened = False

    def run(self):
        while True:
            if self.opened:
                self.recv()
            else:
                time.sleep(0.1)


class AppFrame(object):
    def __init__(self):
        self.frame_length = 0
        self.frame_option = 1
        self.frame_command = 0
        self.frame_id = 0
        self.send_service = {'type': 0, 'id': 0}
        self.recv_service = {'type': 0, 'id': 0}
        self.proxy_service = {'type': 0, 'id': 0}
        self.transaction_id = 0
        self.session_id = 1
        self.send_ip_address = 0
        self.client_inst_id = 0
        self.client_use_count = 1
        self.message = None

    def frame_head_encode(self):
        return pack('>4I6H5I', self.frame_length, self.frame_option,
            self.frame_command, self.frame_id, self.send_service['type'],
            self.send_service['id'], self.recv_service['type'],
            self.recv_service['id'], self.proxy_service['type'],
            self.proxy_service['id'], self.transaction_id, self.session_id,
            self.send_ip_address, self.client_inst_id, self.client_use_count
            )

    def frame_head_decode(self, head):
        (self.frame_length, self.frame_option,
            self.frame_command, self.frame_id, self.send_service['type'],
            self.send_service['id'], self.recv_service['type'],
            self.recv_service['id'], self.proxy_service['type'],
            self.proxy_service['id'], self.transaction_id, self.session_id,
            self.send_ip_address, self.client_inst_id, self.client_use_count
        ) = unpack('>4I6H5I',head)

    def encode(self):
        msg = self.message.SerializeToString()
        self.frame_length = 48 + len(msg)
        return self.frame_head_encode() + msg

    def decode(self, body):
        self.message.ParseFromString(body)
