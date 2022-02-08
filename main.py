import argparse
import os
from console.console import Console
from initializer.initializer import Initializer
from healthcare.storage import Storage
from healthcare.appointment_schedule import AppointmentSchedule

# a convenient main to call the application

# TODO clean
def run_test():
    from test.end_to_end_testing import TestEndToEnd
    from test.doctor_test import TestDoctor
    #TestEndToEnd().test_register_patients()
    TestDoctor().test_dont_issue_same_prescription_twice()

if __name__ == "__main__":
    # TODO clean
    # run_test()
    parser = argparse.ArgumentParser(description='Manage a Clinic')
    # TODO fix defaults
    parser.add_argument('-k','--keep', action='store_false', help='keeps existing db, with no initialization')
    # parser.add_argument('-r','--reset', action='store_true', help='starts with a clean database')
    # parser.add_argument('-i','--init', action='store_false', help='resets the database and starts with a preloaded clinic')
    # parser.add_argument('-i','--init', action='store_true', help='resets the database and starts with a preloaded clinic')
    # parser.add_argument('-q','--quick', action='store_false', help='speeds up animations')
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
