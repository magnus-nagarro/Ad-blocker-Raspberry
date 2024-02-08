from __init__ import *


class blocker():
    def __init__(self, db) -> None:
        self.db = db

    def get_blocked_links(self):
        return self.db.return_links()

    def packet_filter(self, packet):
        if packet.haslayer(TCP):
            return "google.com" in str(packet[TCP].payload)

    def blocker_loop(self):
        while True:
            running = self.db.should_blocker_run()
            if running:
                incoming_packet = sniff(
                    filter="tcp", stop_filter=self.packet_filter)
                blocked_list = self.get_blocked_links()
                buff = {
                    "packet": incoming_packet
                }
                self.db.logger(buff)
            sleep_time.sleep(0.01)
