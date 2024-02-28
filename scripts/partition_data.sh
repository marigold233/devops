#!/usr/bin/env bash
# 用一整个磁盘格式化使用，不用经过fdisk、parted分区
mkfs.xfs /dev/xvde
mkdir /data
mount /dev/xvde /data
echo '/dev/xvde                /data                    xfs     defaults        0 0' >>/etc/fstab
df -hT
