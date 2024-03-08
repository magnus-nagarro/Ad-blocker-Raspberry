from __init__ import *

# IMPORTANT: This script runs outside of docker because we need to execute commands on the raspberry


class blocker():
    def __init__(self) -> None:
        self.db = mongodb()
        self.already_blocked = list()

    # A wrapper for the return_links() function in mongodb -> bool(if unsuccessful)/list
    def get_blocked_links(self):
        return self.db.return_links()

    # A wrapper for the should_run() function in mongodb -> bool
    def should_run(self):
        return self.db.should_blocker_run()

    # This is the main blocker loop, all the blocker logic runs here, which means it
    # edits the bad-sites.acl file, corresponding to what we have in our database and whether
    # the blocker should run or not.
    def blocker_loop(self):
        while True:
            # Should the blocker even run?
            running = self.should_run()
            # Getting the current working directory because we need that later to open the bad-sites.acl file
            current_path = os.getcwd()
            if running:
                # First we get all links that should be added to the file and declare some variables that we need later
                blocked = self.get_blocked_links()
                to_block = str()
                counter = int()
                # If getting the blocked links failed for some reason, we just continue
                if not blocked:
                    continue
                # Now we check which links are already getting blocked
                with (open(f'{current_path}/bad-sites.acl', 'r') as file):
                    buff = file.read()
                    already_blocked = buff.split('\n')
                # We iterate through all the links that are in the database
                for link in blocked:
                    # If they are already in bad-sites.acl we increment counter by one, and append it to to_block which is
                    # later written into bad-sites.acl
                    if link in already_blocked:
                        counter += 1
                        to_block += link + '\n'
                    else:
                        to_block += link + '\n'
                # Checking if any links that are in bad-sites.acl got removed and are not in the database(blocked) anymore
                for link in already_blocked:
                    if link == "":
                        continue
                    if link not in blocked:
                        counter -= 1
                # If counter and blocked.__len__() are equal nothing changed
                if counter == blocked.__len__():
                    continue
                # If something changed we write to_block to the bad-sites.acl file and restart squid to apply the changes
                with (open(f'{current_path}/bad-sites.acl', 'w') as file):
                    file.write(str(to_block))
                    subprocess.run(["sudo", "systemctl", "restart", "squid"])
            # If the blocker should not run we clear bad-sites.acl and restart squid if needed
            else:
                with (open(f'{current_path}/bad-sites.acl', 'r') as file):
                    buff = file.read()
                    if buff == "":
                        continue
                open(f'{current_path}/bad-sites.acl', 'w').close()
                subprocess.run(["sudo", "systemctl", "restart", "squid"])
            sleep_time.sleep(0.01)


if __name__ == "__main__":
    try:
        block = blocker()
        block.blocker_loop()
    except Exception as e:
        print(f"Error occured: {e}")
    finally:
        print("Exiting...")
