#!/bin/bash

###
# killProcesses.sh kills processes by name
###

process=$(ps | grep $1 | awk '{print $1}')
echo $process
kill -9 $process
