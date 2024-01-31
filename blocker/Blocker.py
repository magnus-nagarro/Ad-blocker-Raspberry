from __init__ import *


class blocker():
    def __init__(self, db) -> None:
        self.db = db

    def get_blocked_links(self):
        return self.db.return_links()

    def blocker_loop(self):
        while True:
            running = self.db.should_blocker_run()
            if running:
                host = "0.0.0.0"
                port = "8080"
                s.bind(host, port)
                s = socket.socket(
                    socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                incoming_packet = s.recvfrom(1024)
                # blocked_list = self.get_blocked_links()
                parsed_packet = dhcppython.packet.DHCPPacket.from_bytes(
                    incoming_packet)
                sender_ip = parsed_packet.ciaddr
                self.db.insert_one(sender_ip)
