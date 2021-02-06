#!/bin/bash
# Set up RESUME variable
# This happens when one install Ubuntu fresh on the system, but I allow it to pick the install without choosing manual and repartitioning
printf "RESUME=UUID=$(blkid | awk -F\" '/swap/ {print $2}')\n" | sudo tee /etc/initramfs-tools/conf.d/resume

