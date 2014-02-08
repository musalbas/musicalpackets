#!/bin/bash

stdbuf -oL tcpdump -i wlan0 | python musicalpackets.py
