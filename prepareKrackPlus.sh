#!/bin/bash

# check whether colorlog is installed
if ! pip show colorlog | grep -q colorlog;
	then
	# install colorlog
	pip install colorlog > /dev/null
fi
