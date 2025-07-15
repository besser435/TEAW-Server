The path of the server is
`/var/opt/minecraft/crafty/crafty-4/servers/e97c3311-4330-4fb8-be4a-b74cfa6b734b`

## Timezone
In order for Crafty to pickup on timezone changes, you must run `sudo dpkg-reconfigure tzdata`. Just changing
the timezone with some other command won't let it pickup on changes. This can prevent things like scheduled tasks from
running. `timedatectl` is helpful.

The server is set to `Europe/Helsinki`, as the server is in Hetzner's Finland location. Finland observes DST, so this
may affect schedules from running at a different time through the year.

## Crafty Service
Crafty is a service. The following commands are helpful for services:
- `sudo systemctl status crafty` status
- `sudo systemctl start crafty` start
- `sudo systemctl stop crafty` stop
- `sudo systemctl enable crafty` starts Crafty at boot (already done)
- `systemctl is-enabled crafty` view status if it's enabled on boot

## TEAW Backups
Backups are handled with Crafty. It runs a few minutes after the server restart and takes several minutes to complete.
Ignore the `bluemap` directory, as its huge and does not need to be backed up, as it can be rebuilt from the world.

> [!NOTE]
> Crafty Docs recommends shutting the server down for backups due to how it works. This kind of sucks for players though, since
backups take about 5 minutes.
> 
> Perhaps in addition to the daily backups, we have a weekly maintenance period where the server stops to perform
> a stopped backup. Could also get rid of the daily reboots and do it then.

Backups are stored at `/var/opt/minecraft/crafty/crafty-4/backups/e97c3311-4330-4fb8-be4a-b74cfa6b734b` (maybe change this
to not be in the Crafty directory)

> [!CAUTION]
> Do NOT enable the "Compress Backup" option. The warning for this sounds like it enables some kind of world trimming or non-filesystem
leve compression, which could break the world. 

## Crafty TEAW Config
This section is for the server config options in the panel.
- The IP should be set to the actual server IP of `157.180.15.120`. The loopback address didn't work I don't think.
- RAM launch flags of `-Xms18432M -Xmx18432M` for 18GB of RAM (further optimization could be done here).
- Java Version: "Do not override" OpenJDK 21.0.7 is installed (but Arclight 1.0.6 breaks with anything > 17, what???????)
- Enable server auto start
- Enable restart on crash

## Crafty File Permissions
Crafty needs certain perms for files. For Crafty to do something on a file or directory, it generally needs to be owned
by the crafty user and have rwx perms. Here are some helpful commands for that:
- `sudo chown -R crafty:crafty /var/opt/minecraft` gives ownership to the crafty user for all files/directories in the 
crafty directory. Can also run it on individual files/directories.
- `sudo chmod -R 2755 ./(directory or file)` lets crafty and other users rwx. [Difference between 2755 and 755](https://unix.stackexchange.com/questions/52707/difference-between-chmod-775-and-chmod-2755)
- `ls -l ./(directory or file)` shows the perms of a file or directory.
- `sudo su crafty` switch to the crafty user. Will need to close the session to get back to the original user.

## Crafty Panel Multi-factor Authentication

## Firewall
close bluemap port when migrating to cloudflare tunnel

## Cloudflare Tunnels

## DNS Records

## SSH
Fail2ban would be poggers, set up key based auth before deploying

https://www.reddit.com/r/homelab/comments/5pydet/so_youve_got_ssh_how_do_you_secure_it/
scary!

## Maintenance
- Verify backups. This includes downloading them on a separate computer and ensuring the server starts and there are
  no missing files.
- Verify the health of the RAID array with `cat /proc/mdstat` and its disks `smartctl -a /dev/nvme0n1`, `smartctl -a /dev/nvme1n1`.
  Also check general resource usage with `btop`.
- Update the OS and its packages.