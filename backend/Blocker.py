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
                if not blocked:
                    continue
                with (open('bad-sites.acl', 'r') as file):
                    buff = file.read()
                    already_blocked = buff.split('\n')
                for link in blocked:
                    if link in already_blocked:
                        continue
                    else:
                        to_block += link + '\n'
                if to_block == "":
                    continue
                with (open('bad-sites.acl', 'w') as file):
                    file.write(str(to_block))
            else:
                open('bad-sites.acl', 'w').close()
