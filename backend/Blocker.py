from __init__ import mongodb


class blocker:
    def __init__(self) -> None:
        self.db = mongodb()

    def get_blocked_links(self):
        return self.db.return_links()

    def should_run(self):
        return self.db.should_blocker_run()

    def blocker_loop(self):
        while True:
            running = self.should_run()
            if running:
                blocked = self.get_blocked_links()
                to_block = str()
                counter = int()
                if not blocked:
                    continue
                with (open('bad-sites.acl', 'r') as file):
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
                with (open('bad-sites.acl', 'w') as file):
                    file.write(str(to_block))
            else:
                open('bad-sites.acl', 'w').close()
