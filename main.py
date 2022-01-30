import argparse
from console.console import Console
from initializer.initializer import Initializer
from healthcare.storage import Storage
from healthcare.appointment_schedule import AppointmentSchedule
from test.doctor_test import TestDoctor

# a convenient main to call the application

# TODO clean
def run_test():
    from test.receptionist_test import TestReceptionist
    TestDoctor().test_issue_prescription()

if __name__ == "__main__":
    # TODO clean
    run_test()
    parser = argparse.ArgumentParser(description='Manage a Clinic')
    # TODO fix defaults
    parser.add_argument('-r','--reset', action='store_true', help='starts with a clean database')
    parser.add_argument('-i','--init', action='store_false', help='resets the database and starts with a preloaded clinic')
    parser.add_argument('-q','--quick', action='store_false', help='speeds up loading time')
    args = parser.parse_args()

    clinic = None
    
    db = Storage(args.reset or args.init)
    schedule = AppointmentSchedule(db)

    if args.init:
        print('initializing')
        Initializer(db = db, schedule = schedule, quick = args.quick).initialize()

    console = Console(storage=db, schedule=schedule, quick=args.quick)
    console.loop()
