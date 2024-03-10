# Docker #

Normally, the Docker containers should start automatically when you start your Raspberry Pi. If this is not the case, please use the following commands in the project folder:

### START ###

```
docker compose up -d
```

### STOP ###

```
docker compose down
```

### RESTART ###

```
docker compose restart
```

# ABOUT #

Adblocker running in a docker container on a Raspberry PI

# Related Project #
https://github.com/magnus-nagarro/Ad-blocker-Raspberry-Ui

# Configuration #

Please note: The path your/projectfolder is often mentioned in this documentation. This refers to the path to the "Ad-blocker-Raspberry" folder, including this folder itself.

## SQUID Installation and Configuration ##

To be able to block the links later, we use the Raspberry Pi as a proxy server. We implement this with squid. Squid must be configured correctly to ensure smooth operation. 

Important: If problems occur during configuration, you can follow the complete configuration in this video. The audio of this video is in German, but the steps should still be easy to follow. 

https://www.youtube.com/watch?v=-GsJQ-EnYJ0


### Install SQUID ##

```cmd
sudo apt install squid
```

### Configure SQUID ###

Squid does not support the functions that our blocker needs in the standard configuration, which is why we have to configure a little more. 

You can either change the data listed below in the respective file or use our supplied files in the "configuration-files" folder. 

!Please note that you need sudo rights to change the files in Linux!


Now we change suqid.conf in the folder etc/squid. 

If you want to use our file, please change your host Ip (e.g. 192.168.178.0/24) and the path to bad-links.acl
This is located in the project folder under /blocker/bad-sites.acl
Then replace the suqid.conf under etc/squid on your PI with our supplied .conf file

Alternatively, execute the following:

```cmd
sudo nano etc/suqid/squid.conf
```
Edit the configuration like this:

1. comment out all alc localnet entries
2. add the following line (Replace your.host.ip with your host Ip (e.g. 192.168.178)): 
    ```
    alc localnet src your.host.ip.0/24 
    ```
3. after the heading # INSERT YOUR OWN RULE(S) HERE TO ALLOW ACCESS FROM YOUR CLIENTS please insert the following lines (replace your/projectfolder with the   path to this project):
    ```
    acl bad_url dstdomain "your/projectfolder/blocker/badlinks-acl"
    http_access deny bad_url 
    ```
4. Replace the line "http_access deny all" with:
    ```	
    http_access allow all
    ```
5. Now you can save (ctrl+S) and close (ctrl+X) the file

Now start squid and add it to autostart:
```
sudo systemctl start squid
sudo systemctl enable squid
```

Squid is now running and should start automatically when restarting the PI.

## Blocker Configuration ##

To ensure a smooth process here too, it is best to add our blocker script to the autostart. 

Again, you can use the rc.local file we have created, which you only need to copy into the etc folder with sudo rights

Alternatively, carry out the following steps:

```
sudo nano /etc/rc.local
```

Now insert these lines before "exit 0" and again replace your/projectfolder with the path to this project:
```
cd your/projectfolder/blocker
sudo python Blocker.py
```

Now safe (ctrl+S) and close (ctrl+X) the file and restart your PI.

The Blocker should now be able to start automatically when restarting the PI.

## Configure Devices ##

Now you only have to set the correct proxy for the devices in the network to benefit from the blocker:

Ip: Ip address of the Raspberry PI
Port: 3128 (or the port you have specified in squid.conf)
