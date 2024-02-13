from __init__ import *
from scapy.all import sniff, TCP


class blocker():
    def __init__(self, db) -> None:
        self.db = db

    def get_blocked_links(self):
        return self.db.return_links()

    def packet_filter(self, packet):
        blocked_list = self.get_blocked_links()
        if blocked_list == False:
            return
        if packet.haslayer(TCP):
            for blocked in blocked_list:
                if blocked in str(packet[TCP].payload):
                    return True
                else:
                    continue

    def blocker_loop(self):
        while True:
            running = self.db.should_blocker_run()
            if running:
                incoming_packet = sniff(
                    filter="tcp", stop_filter=self.packet_filter)
                self.db.logger(str(incoming_packet))
            sleep_time.sleep(0.01)


if __name__ == "__main__":
    try:
        db = mongodb()
        block = blocker(db)
        block.blocker_loop()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        print("Exiting...")
