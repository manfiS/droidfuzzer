from framework.commands.cmd import Run
from blessings import Terminal
import sys
t = Terminal()

if __name__ == "__main__":

    print(t.yellow("""

______           _     _______
|  _  \         (_)   | |  ___|
| | | |_ __ ___  _  __| | |_ _   _ ___________ _ __
| | | | '__/ _ \| |/ _` |  _| | | |_  /_  / _ \ '__|
| |/ /| | | (_) | | (_| | | | |_| |/ / / /  __/ |
|___/ |_|  \___/|_|\__,_\_|  \__,_/___/___\___|_|


    """))

    try:
        run = Run()
        run.prompt = t.yellow("(DroidFuzzer) ")
        run.ruler = t.yellow("-")
        run.cmdloop()
    except KeyboardInterrupt:
        sys.exit(0)
