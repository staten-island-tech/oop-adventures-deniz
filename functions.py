import sys
import time


def colored(r, g, b, text):
    return "\033[38;2;{};{};{}m{} \033[38;2;255;255;255m".format(r, g, b, text)


def incP(txt, speed=0.03):
    for i in txt:
        sys.stdout.write(i)
        sys.stdout.flush()
        time.sleep(speed)
    sys.stdout.write(f"\n")


def italic(txt):
    return "\x1B[3m" + txt + "\x1B[0m"
