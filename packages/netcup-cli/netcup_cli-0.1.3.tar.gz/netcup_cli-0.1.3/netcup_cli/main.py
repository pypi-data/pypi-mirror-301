import argparse
import sys
import os
import json
import base64
from getpass import getpass
from netcup_webservice import NetcupWebservice

# Get the directory where the current script is located
SCRIPT_DIR = os.path.dirname(os.path.realpath(__file__))
CREDENTIALS_FILE = os.path.join(SCRIPT_DIR, "netcup_credentials.json")

class CLI:
    def __init__(self):
        self.parser = argparse.ArgumentParser(
            description="CLI tool for interacting with the Netcup Webservice"
        )

        subparsers = self.parser.add_subparsers(dest="command", help="Available commands")

        # Login command
        login_parser = subparsers.add_parser("login", help="Login and store credentials")
        login_parser.add_argument('--user', required=False, help="Login name for Netcup Webservice")
        login_parser.add_argument('--password', required=False, help="Password for Netcup Webservice")

        # Get subcommand
        get_parser = subparsers.add_parser("get", help="Retrieve a resource")
        get_parser.add_argument('resource', choices=[
            'vserver_nickname', 'vserver_state', 'vserver_uptime', 
            'vserver_update_notification', 'vserver_stat_token', 
            'vserver_traffic_of_day', 'vserver_traffic_of_month', 
            'vserver_information', 'vserver_ips', 'vservers'
        ], help="Resource to retrieve")
        get_parser.add_argument('--vserver_name', required=False, help="Name of the vServer")
        get_parser.add_argument('--year', type=int, required=False, help="Year (required for traffic commands)")
        get_parser.add_argument('--month', type=int, required=False, help="Month (required for monthly traffic)")
        get_parser.add_argument('--day', type=int, required=False, help="Day (required for daily traffic)")

        # Set subcommand
        set_parser = subparsers.add_parser("set", help="Set a resource")
        set_parser.add_argument('resource', choices=[
            'vserver_nickname', 'password', 'panel_settings'
        ], help="Resource to set")
        set_parser.add_argument('--vserver_name', required=False, help="Name of the vServer")
        set_parser.add_argument('--nickname', required=False, help="New nickname for the vServer")
        set_parser.add_argument('--new_password', required=False, help="New password for the user")
        set_parser.add_argument('--panel_settings', required=False, help="New panel settings")

        # Start/Stop/Poweroff subcommands
        start_parser = subparsers.add_parser("start", help="Start a vServer")
        start_parser.add_argument('--vserver_name', required=True, help="Name of the vServer to start")

        stop_parser = subparsers.add_parser("stop", help="Stop a vServer")
        stop_parser.add_argument('--vserver_name', required=True, help="Name of the vServer to stop")

        poweroff_parser = subparsers.add_parser("poweroff", help="Power off a vServer")
        poweroff_parser.add_argument('--vserver_name', required=True, help="Name of the vServer to power off")

    def save_credentials(self, loginname, password):
        encoded_loginname = base64.b64encode(loginname.encode()).decode()
        encoded_password = base64.b64encode(password.encode()).decode()

        credentials = {
            "loginname": encoded_loginname,
            "password": encoded_password
        }

        with open(CREDENTIALS_FILE, 'w') as f:
            json.dump(credentials, f)

        print(f"Login credentials saved successfully to {CREDENTIALS_FILE}.")

    def load_credentials(self):
        if not os.path.exists(CREDENTIALS_FILE):
            return None

        with open(CREDENTIALS_FILE, 'r') as f:
            credentials = json.load(f)

        decoded_loginname = base64.b64decode(credentials['loginname']).decode()
        decoded_password = base64.b64decode(credentials['password']).decode()

        return decoded_loginname, decoded_password

    def ensure_login(self):
        credentials = self.load_credentials()
        if not credentials:
            print("[!] Login credentials not set. Please run the login command first.")
            sys.exit(1)
        return credentials

    def run(self):
        args = self.parser.parse_args()

        if args.command == "login":
            loginname = args.user if args.user else input("Login name: ")
            password = args.password if args.password else getpass("Password: ")
            self.save_credentials(loginname, password)
            sys.exit(0)

        loginname, password = self.ensure_login()

        netcup_ws = NetcupWebservice(loginname=loginname, password=password)

        if args.command == "get":
            resource_map = {
                'vserver_nickname': netcup_ws.get_vserver_nickname,
                'vserver_state': netcup_ws.get_vserver_state,
                'vserver_uptime': netcup_ws.get_vserver_uptime,
                'vserver_update_notification': netcup_ws.get_vserver_update_notification,
                'vserver_stat_token': netcup_ws.get_vserver_stat_token,
                'vserver_traffic_of_day': netcup_ws.get_vserver_traffic_of_day,
                'vserver_traffic_of_month': netcup_ws.get_vserver_traffic_of_month,
                'vserver_information': netcup_ws.get_vserver_information,
                'vserver_ips': netcup_ws.get_vserver_ips,
                'vservers': netcup_ws.get_vservers
            }

            if args.resource == 'vserver_traffic_of_day':
                # Ensure year, month, and day are provided
                if not (args.year and args.month and args.day):
                    print("Please provide year, month, and day for daily traffic.")
                    sys.exit(1)
                result = netcup_ws.get_vserver_traffic_of_day(
                    vserver_name=args.vserver_name,
                    year=args.year,
                    month=args.month,
                    day=args.day
                )
            
            elif args.resource == 'vserver_traffic_of_month':
                # Ensure year and month are provided
                if not (args.year and args.month):
                    print("Please provide year and month for monthly traffic.")
                    sys.exit(1)
                result = netcup_ws.get_vserver_traffic_of_month(
                    vserver_name=args.vserver_name,
                    year=args.year,
                    month=args.month
                )
            
            else:
                method = resource_map[args.resource]
                if args.vserver_name:
                    result = method(vserver_name=args.vserver_name)
                else:
                    result = method() if args.resource == 'vservers' else method(None)
                print(result)

        elif args.command == "set":
            if args.resource == "vserver_nickname":
                result = netcup_ws.set_vserver_nickname(vserver_name=args.vserver_name, nickname=args.nickname)
            elif args.resource == "password":
                result = netcup_ws.change_user_password(new_password=args.new_password)
            elif args.resource == "panel_settings":
                show_nickname = True if args.panel_settings.lower() == 'true' else False
                result = netcup_ws.set_panel_settings(show_nickname=show_nickname)
            else:
                result = f"Unknown resource: {args.resource}"
            print(result)

        elif args.command == "start":
            result = netcup_ws.start_vserver(vserver_name=args.vserver_name)
            print(result)

        elif args.command == "stop":
            result = netcup_ws.stop_vserver(vserver_name=args.vserver_name)
            print(result)

        elif args.command == "poweroff":
            result = netcup_ws.poweroff_vserver(vserver_name=args.vserver_name)
            print(result)

        else:
            print(f"Unknown command: {args.command}")
            self.parser.print_help()

def main():
    cli = CLI()
    cli.run()
