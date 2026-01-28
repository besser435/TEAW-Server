The path of TEAW is
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
level compression, which could break the world. 

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

> [!NOTE]
> The chown and chmod commands should be run anytime a file is added to the server directory manually, so that Crafty
> and Minecraft can interact with it.

## Crafty Users
There are three user accounts. besser and Theeno have superuser accounts. Game masters have a more limited account.
When creating new users, ensure they reset their passwords, and have as few permissions as possible. 

<sub>why the hell does crafty not have a "reset password on next logon" feature like AD or AMP</sub>

## Firewall
Only open port is 25565/TCP in for Minecraft, and 22000 for SSH.
- `ufw status verbose` status, or `ufw status numbered`
- `sudo ufw allow 25565/tcp` open a port
- `ufw delete` delete a rule

## Cloudflare Tunnels
Le tunnels:
- Bluemap on port 8100 at [map.toendallwars.org]([map.toendallwars.org) for HTTP `localhost:8100`
- TEAW API on port 1850 at [tapi.toendallwars.org]([tapi.toendallwars.org) for HTTP `localhost:1850`
- Crafty Panel on port 8443 for HTTPS `localhost:8443`

For the Crafty tunnel to work, `socks` in the tunnel connection settings needs to be enabled, along with `No TLS Verify` under
TLS.

## OS and RAID
This was configured with Hetzner's [installimage](https://docs.hetzner.com/robot/dedicated-server/operating-systems/installimage/) script.

## SSH
SSH uses an Ed25519 key, password auth is disabled.
SSH is on port 22000 to stop naive attackers from spamming port 22, as seen by `cat /var/log/auth.log`

Config file is `sudo nano /etc/ssh/sshd_config`. 

See enabled auth methods with `sshd -T | grep -i authentication`

For changes to take effect, use`systemctl daemon-reload; systemctl restart ssh.socket`
Restart SSH with `sudo systemctl restart ssh`

(sometimes you have to use one or the other, so if one doesn't work to apply the changes, try the other method.)

Note that when generating a key from PuTTYgen, use the "Public key for pasting into OpenSSH authorized_keys file" 
(top of the window) key, rather than exporting the public key.

[Scary!](https://www.reddit.com/r/homelab/comments/5pydet/so_youve_got_ssh_how_do_you_secure_it/)

## Maintenance
- Verify backups (RAID is not a backup 😔). This includes downloading them on a separate computer and ensuring the server starts and there are
  no missing files.
- Verify the health of the RAID array with `cat /proc/mdstat` and its disks `smartctl -a /dev/nvme0n1`, `smartctl -a /dev/nvme1n1`.
  Also check general resource usage with `btop`.
- Update the OS and its packages. This may restart the Crafty service!
