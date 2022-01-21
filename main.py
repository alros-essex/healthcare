import argparse
import sys
from healthcare.clinic import Clinic
from console.console import Console
from initializer.initializer import Initializer

# a convenient main to call the application

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage a Clinic')
    # TODO fix defaults
    parser.add_argument('-i','--init', action='store_false', help='start with a preloaded clinic')
    parser.add_argument('-q','--quick', action='store_false', help='speeds up loading time')
    args = parser.parse_args()

    clinic = Clinic()
    if args.init:
        print('initializing')
        initializer = Initializer()
        initializer.init(clinic, quick=args.quick)

    console = Console()
    console.loop(clinic)
