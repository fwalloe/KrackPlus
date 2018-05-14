#!/bin/bash

###
# killProcesses.sh kills processes by name
###

process=$(ps | grep $1 | awk '{print $1}')
kill -9 $process &>/dev/null
