#!/bin/bash

# check whether colorlog is installed
if ! pip show colorlog | grep "colorlog" > /dev/null;
	then
	# install colorlog
	pip install colorlog > /dev/null
fi
