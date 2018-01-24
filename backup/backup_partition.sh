mount -t nfs ftpback-rbx3-473.ovh.net:/export/ftpbackup/ns6663170.ip-151-80-105.eu /mnt/backup

mount -t cifs -o sec=ntlm,uid=root,gid=100,dir_mode=0700,username=root,password=fVnb79C4rG //ftpback-rbx3-473.ovh.net/ns6663170.ip-151-80-105.eu /mnt/backup

ftp://ns6663170.ip-151-80-105.eu:fVnb79C4rG@ftpback-rbx3-473.ovh.net

#!/bin/sh
dd if=/dev/sda of=/mnt/backup/sda.img conv=noerror
fdisk -l /dev/sda > /mnt/backup/sda.info
dd if=/dev/sdb of=/mnt/backup/sdb.img conv=noerror
fdisk -l /dev/sdb > /mnt/backup/sdb.info
