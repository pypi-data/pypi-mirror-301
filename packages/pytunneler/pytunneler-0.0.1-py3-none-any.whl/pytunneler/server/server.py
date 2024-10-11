#!/usr/bin/env python

import asyncio
import socket
import time
from websockets import WebSocketServerProtocol
from websockets.server import serve
import threading
import logging
from queue import Queue

from pytunneler.utils import commands, network, packet, host_hex




class WebsocketServer:
    def __init__(self):
        self.tcp_thread = None
        self.loop = asyncio.new_event_loop()
        asyncio.set_event_loop(self.loop)
        self.tcp_servers: dict[str, TCPServer] = dict()
        self.local_remote: dict[str, str] = dict()
        self.host = "localhost"
        self.port = 8765


    def start_tcp_server(self, websocket, local_ip, local_port, target_ip, target_port):
        thread = TCPServer(websocket, self, local_ip, int(local_port), target_ip, int(target_port))
        self.tcp_servers[f"{target_ip}:{target_port}"] = thread
        self.local_remote[f"{local_ip}:{local_port}"] = f"{target_ip}:{target_port}"
        thread.start()

    def handle_packet(self, raw_packet, websocket: WebSocketServerProtocol):
        packet_ = packet.Packet.bytes2packet(raw_packet)
        if isinstance(packet_, packet.CommandPacket):
            command = packet_.command
            for command_type in commands.CommandTypes:
                if command.split()[0] == command_type.trigger:
                    context = commands.CommandContext(command.split()[1:], websocket, self)
                    message = command_type.on_command(context)
                    command_callback_packet = packet.CommandCallbackPacket(message)
                    network.websocket_send(self.loop, websocket, command_callback_packet.create_packet())
                    break
            else:
                print(f"Unknown command: {command.split()[0]}")
                command_callback_packet = packet.CommandCallbackPacket(f"Unknown command: {command.split()[0]}")
                network.websocket_send(self.loop, websocket, command_callback_packet.create_packet())
        elif isinstance(packet_, packet.BinaryPacket):
            ip, port = host_hex.hex2host(packet_.host).split(":")
            target_ip, target_port = host_hex.hex2host(packet_.target_host).split(":")
            remote_address = self.local_remote[f"{ip}:{port}"]
            network.tcp_send(self.tcp_servers[remote_address].clients[f"{target_ip}:{target_port}"], packet_.data)


    async def process(self, websocket: WebSocketServerProtocol):
        logging.info(f"Connected by {websocket.remote_address[0]}:{websocket.remote_address[1]}")
        while True:
            raw_packet = await network.websocket_recv(websocket)
            if not raw_packet:
                break
            self.handle_packet(raw_packet, websocket)
        for tcp_server in self.tcp_servers.values():
            if tcp_server.websocket == websocket:
                tcp_server.shutdown.set()
                tcp_server.server_socket.close()

    async def main(self):
        async with serve(self.process, self.host, self.port):
            logging.info(f"Websocket server is running on ws://{self.host}:{self.port}")
            await asyncio.get_running_loop().create_future()  # run forever

    def run(self):
        return self.loop.run_until_complete(self.main())

class TCPServer(threading.Thread):
    def __init__(self, websocket: WebSocketServerProtocol, server: WebsocketServer, local_ip, local_port, host, port):
        self.packet_queue = Queue()
        self.local_ip = local_ip
        self.local_port = local_port
        self.host = host
        self.port = port
        self.server = server
        self.server_socket = None
        self.websocket = websocket
        self.clients = {}
        self.shutdown = threading.Event()
        super().__init__()

    def run(self):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
            server_socket.bind((self.host, self.port))
            server_socket.listen(5)
            self.server_socket = server_socket
            self.tcp_socket = server_socket
            logging.info(f"TCP server is running on {self.host}:{self.port}")
            local_hex = host_hex.host2hex(f"{self.local_ip}:{self.local_port}")

            while not self.shutdown.is_set():
                try:
                    client_socket, client_address = server_socket.accept()
                except OSError:
                    print(f"shutdowning TCP server {self.host}:{self.port}")

                client_host, client_port = client_address
                client_hex = host_hex.host2hex(f"{client_host}:{client_port}")
                self.clients[f"{client_host}:{client_port}"] = client_socket
                with client_socket:
                    logging.info(f"Connected by {client_address}")
                    connected_packet = packet.ConnectedPacket(client_hex, local_hex)
                    network.websocket_send(self.server.loop, self.websocket, connected_packet.create_packet())
                    time.sleep(0.5)
                    while not self.shutdown.is_set():
                        data = network.tcp_recv(client_socket)
                        if data is None:
                            logging.info("no data, shutdowning")
                            break
                        binary_packet = packet.BinaryPacket(client_hex, local_hex, data)
                        network.websocket_send(self.server.loop, self.websocket, binary_packet.create_packet())
            print(f"shutdowning TCP server {self.host}:{self.port}")
if __name__ == "__main__":
    server = WebsocketServer()
    server.run()
