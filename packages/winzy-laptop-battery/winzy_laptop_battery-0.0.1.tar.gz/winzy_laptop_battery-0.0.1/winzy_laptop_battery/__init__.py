import winzy
import psutil
import os

def create_parser(subparser):
    parser = subparser.add_parser("battery", description="Get laptop battery info")
    # Add subprser arguments here.
    parser.add_argument("-w", "--warn", action="store_true", help="If true warns about low battery")
    parser.add_argument("-wat", "--warn-at", type=int, default=30, help="Warn if battery is bellow this number ")
    return parser


class HelloWorld:
    name = "battery"

    @winzy.hookimpl
    def register_commands(self, subparser):
        parser = create_parser(subparser)
        parser.set_defaults(func=self.battery)

    def battery(self, args):
        # this routine will be called when "winzy "battery is called."               
        psutil.sensors_battery()
        a = psutil.sensors_battery()
        if not a.power_plugged:
            percent = a.percent
            if percent <= args.warn_at:
                if args.warn:
                    _ = os.system("say 'Battery is at {}'".format(percent))
            print(percent)

    
    def hello(self, args):
        # this routine will be called when "winzy "battery is called."
        print("Hello! This is an example ``winzy`` plugin.")

battery_plugin = HelloWorld()
