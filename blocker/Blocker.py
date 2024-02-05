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
                s = socket.socket(
                    socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_TCP)
                incoming_packet = s.recvfrom(1024)
                blocked_list = self.get_blocked_links()
                buff = {
                    "packet": incoming_packet
                }

                self.db.logger(buff)
            sleep_time.sleep(0.01)
