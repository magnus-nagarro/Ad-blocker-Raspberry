from __init__ import *
from scapy.all import sniff, TCP


class blocker():
    def __init__(self, db) -> None:
        self.db = db
        self.already_blocked = list()
        self.logged_packets = dict()

    def get_blocked_links(self):
        return self.db.return_links()

    def should_run(self):
        return self.db.should_blocker_run()

    def packet_filter(self, packet):
        blocked_list = self.get_blocked_links()
        if blocked_list == False:
            return
        if packet.haslayer(TCP):
            for blocked in blocked_list:
                if blocked in str(packet[TCP].payload):
                    if blocked in self.logged_packets:
                        self.logged_packets[blocked] += 1
                    else:
                        self.logged_packets[blocked] = 1
                    return True
                else:
                    continue

    def logger_loop(self):
        while True:
            running = self.db.should_blocker_run()
            if running:
                incoming_packet = sniff(
                    filter="tcp", stop_filter=self.packet_filter)
            sleep_time.sleep(0.01)

    def blocker_loop(self):
        while True:
            running = self.should_run()
            if running:
                blocked = self.get_blocked_links()
                if not blocked:
                    continue
                for link in blocked:
                    if link not in self.already_blocked:
                        try:
                            subprocess.run(
                                ["sudo", "iptables", "-A", "OUTPUT", "-p", "tcp", "-d", link, "-j", "DROP"])
                            print(f"Link {link} added to blacklist!")
                            self.already_blocked.append(link)
                        except Exception as e:
                            print(e)
                            continue
            if not running and self.already_blocked.__len__() != 0:
                for rules in self.already_blocked:
                    try:
                        subprocess.run(
                            ["sudo", "iptables", "-D", "OUTPUT", "-p", "tcp", "-d", rules, "-j", "DROP"])
                        print(f"Link {link} removed from blacklist!")
                    except Exception as e:
                        print(e)
                        continue
                self.already_blocked.clear()

            sleep_time.sleep(1)


if __name__ == "__main__":
    try:
        db = mongodb()
        block = blocker(db)
        logger = threading.Thread(target=block.logger_loop)
        logger.start()
        block.blocker_loop()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        print("Exiting...")
