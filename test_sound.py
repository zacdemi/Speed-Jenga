import lib.sounds
from lib.timer import Timer

def main():
    t = Timer(12)
    t.start()
    while t.get_seconds() > 0:
        print(round(t.get_seconds(),2), end="\r")

if __name__ == "__main__":
    main()





