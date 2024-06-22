#!/bin/bash

/bin/perl /back/back.pl

/bin/ls | /bin/grep -P "^[^.]*$" | /bin/xargs -d"\n" rm -r

/bin/rclone -v sync /back/ avz_bck:back
