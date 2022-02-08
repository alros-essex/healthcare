import argparse
import os
from console.console import Console
from initializer.initializer import Initializer
from healthcare.storage import Storage
from healthcare.appointment_schedule import AppointmentSchedule

# a convenient main to call the application

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Manage a Clinic')
    parser.add_argument('-k','--keep', action='store_true', help='keeps existing db, with no initialization')
    args = parser.parse_args()

    if not args.keep:
        Storage.reset()
        AppointmentSchedule.reset()

    db = Storage.instance()
    schedule = AppointmentSchedule.instance()

    if not args.keep:
        print('initializing')
        Initializer(db = db, schedule = schedule, quick = True).initialize()

    console = Console(storage=db, schedule=schedule, quick=True)
    console.loop()
