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
                blocked_list = self.get_blocked_links()
                incoming_packet = str()
                parsed_packet = dhcppython.packet.DHCPPacket.from_bytes(
                    incoming_packet)
                sender_ip = parsed_packet.ciaddr
                print(sender_ip)
