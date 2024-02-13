from __init__ import *
from scapy.all import sniff, TCP


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
            print("running...")
            running = self.db.should_blocker_run()
            if running:
                incoming_packet = sniff(
                    filter="tcp", stop_filter=self.packet_filter)
                blocked_list = self.get_blocked_links()
                buff = {
                    "packet": incoming_packet
                }
                # self.db.logger(buff)
                print(buff)
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
