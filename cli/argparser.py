import argparse


def parse():
    parser = argparse.ArgumentParser(description = "Process NTAG 5 Link sensors")
    parser.add_argument("-r", "--reader", nargs="?", dest="reader", type=int, 
        const=0, default=0, required=False, help="index of the ACR1552 reader to use (default: 0)")
    parser.add_argument("-l", "--list-readers", action="store_true", dest="listreaders", 
        help="list available ACR1552 readers")
    return parser.parse_args()
