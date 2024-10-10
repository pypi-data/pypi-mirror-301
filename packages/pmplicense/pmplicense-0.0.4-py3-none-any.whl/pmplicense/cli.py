import sys
import argparse

from pmplicense import check_license, set_license

def get_parser():
    parser = argparse.ArgumentParser(description="PMP License CLI")
    parser.add_argument('set', help='Command to run')
    parser.add_argument('args', nargs=argparse.REMAINDER)
    return parser.parse_args()


def set_(args):
    return set_license(args[0], args[1])


def check_(args):
    return check_license(args[0])


def get_command(arg):
    commands = {
        'set': set_,
        'check': check_,
    }
    try:
        return commands[arg]
    except Exception as e:
        print(f"Command '{arg}' not found.")


def main():
    parser = get_parser()
    cmd = get_command(sys.argv[1])
    return cmd(parser.args)