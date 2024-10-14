import winzy
from dateutil import parser as dp
from datetime import timedelta, datetime
import os

def create_parser(subparser):
    parser = subparser.add_parser("days", description="Gives days till a provided date")
    # Add subprser arguments here.
    parser.add_argument("datetext", nargs="*", type=str, help="Date text that is passed by the user.")
    parser.add_argument("-s", "--say", action="store_true", help="Announce the days till that date")
    return parser


class HelloWorld:
    name = "days"

    @winzy.hookimpl
    def register_commands(self, subparser):
        self.parser = create_parser(subparser)
        self.parser.set_defaults(func=self.daystill)
    
    def daystill(self, args):
        try:
            parsed_date = dp.parse(" ".join(args.datetext), fuzzy=True)
            daysremaining = (parsed_date - datetime.today()).days
            if args.say:
                os.system("say {0} days remaining to {1}".format(daysremaining, parsed_date))
            print(daysremaining)
        except Exception as ex:
            print(ex)
            self.parser.print_help()


    def hello(self, args):
        # this routine will be called when "winzy "days is called."
        print("Hello! This is an example ``winzy`` plugin.")

days_plugin = HelloWorld()
