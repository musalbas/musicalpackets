#!/bin/bash

stdbuf -oL tcpdump -i wlan0 | python musicalplayback.py
