from __init__ import *


class blocker():
    def __init__(self, db) -> None:
        self.db = db
        self.already_blocked = list()
        self.logged_packets = dict()

    def get_blocked_links(self):
        return self.db.return_links()

    def should_run(self):
        return self.db.should_blocker_run()

    def blocker_loop(self):
        while True:
            running = self.should_run()
            current_path = os.getcwd()
            if running:
                blocked = self.get_blocked_links()
                to_block = str()
                counter = int()
                if not blocked:
                    continue
                with (open(f'{current_path}/bad-sites.acl', 'r') as file):
                    buff = file.read()
                    already_blocked = buff.split('\n')
                for link in blocked:
                    if link in already_blocked:
                        counter += 1
                        to_block += link + '\n'
                    else:
                        to_block += link + '\n'
                for link in already_blocked:
                    if link == "":
                        continue
                    if link not in blocked:
                        counter -= 1
                if counter == blocked.__len__():
                    continue
                with (open(f'{current_path}/bad-sites.acl', 'w') as file):
                    file.write(str(to_block))
                    subprocess.run(["sudo", "systemctl", "restart", "squid"])
            else:
                with (open(f'{current_path}/bad-sites.acl', 'r') as file):
                    buff = file.read()
                    if buff == "":
                        continue
                open(f'{current_path}/bad-sites.acl', 'w').close()
                subprocess.run(["sudo", "systemctl", "restart", "squid"])


if __name__ == "__main__":
    try:
        db = mongodb()
        block = blocker(db)
        block.blocker_loop()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        print("Exiting...")
