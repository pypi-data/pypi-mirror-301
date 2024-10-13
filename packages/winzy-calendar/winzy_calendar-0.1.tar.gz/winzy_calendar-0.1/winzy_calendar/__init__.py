import winzy
import calendar
import datetime


def _showmonth(year, month):
    c = calendar.TextCalendar(calendar.SUNDAY)
    print(c.formatmonth(year,month))

def _showyear(year):
    c = calendar.TextCalendar(calendar.SUNDAY)
    print(c.formatyear(year))


class HelloWorld:
    __name__ = "cal"

    @winzy.hookimpl
    def register_commands(self, subparser):
        calparser = subparser.add_parser("cal", description="Calendar in windows commandline")
        calparser = subparser.add_parser("cal", description="Calendar for cmd")
        calparser.add_argument("-m","--month" , type=int, help="month", default=-1)
        calparser.add_argument("-y","--year" , type=int, help="year", default=-1)

        calparser.set_defaults(func=self.showcalendar)

    def showcalendar(self, args):
        now = datetime.datetime.today()
        if args.month != -1 and args.year != -1:
            _showmonth(args.year, args.month) 
        elif args.year != -1:
            _showyear(args.year)
        elif args.month != -1:
            _showmonth(now.year, args.month) 
        else:
            _showmonth(now.year, now.month) 

        now = datetime.datetime.today()
        c = calendar.TextCalendar(calendar.SUNDAY)
    
    def hello(self, args):
        # this routine will be called when "winzy "cal is called."
        print("Hello! This is an example ``winzy`` plugin.")

cal_plugin = HelloWorld()
