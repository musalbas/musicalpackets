#!/bin/bash

stdbuf -oL tcpdump -i wlan0 | python main.py live
