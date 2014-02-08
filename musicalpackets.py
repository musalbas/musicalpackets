import sys
from mingus.midi import fluidsynth


def parse_tcpdump_line(line):
    words = line.split(" ")
    parsing_params = False
    word_num = 0
    packet = {"params": ""}

    if words[1] != "IP":
        return None

    for word in words:
        if word_num == 0:
            packet['time'] = word
        elif word_num == 1:
            pass
        elif word_num == 3:
            pass
        elif word_num == 2:
            packet['source'] = word
        elif word_num == 4:
            packet['destination'] = word[:-1]
        else:
            packet['params'] += word + " "

        word_num += 1

    packet['params'] = packet['params'][:-2]
    return packet

if __name__ == "__main__":

    fluidsynth.init('/usr/share/sounds/sf2/FluidR3_GM.sf2',"alsa")

    while True:
        line = sys.stdin.readline()
        packet = parse_tcpdump_line(line)

        if packet is None:
            continue

        print packet
