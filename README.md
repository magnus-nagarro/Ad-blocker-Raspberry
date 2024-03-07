### START ###

docker compose up

### STOP ###

docker compose down

### RESTART ###

docker compose restart

### ABOUT ###

Adblocker running in a docker container on a Raspberry PI

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