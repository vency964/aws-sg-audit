#!/usr/bin/python3 #proba

import sys, getopt, os

if sys.version_info < (3, 0):
    sys.stdout.write("Sorry, requires Python 3.x, not Python 2.x")
    sys.exit()

import ipaddress, socket
import csv


def cmd_args():
    network = ''
    port = ''
    out = ''

    try:
        opts, args = getopt.getopt(sys.argv[1:], "hn:p:o:", ["network=", "port=", "out="])
    except getopt.GetoptError:
        print('net-scan.py --network <IP/CIDR> --port <Port> --out <outputfile>')
        sys.exit()
    for opt, arg in opts:
        if opt in ("-h"):
            print('net-scan.py --network <IP/CIDR> --port <Port> --out <outputfile>')
            sys.exit()
        elif opt in ("-n", "--network"):
            network = arg
        elif opt in ("-p", "--port"):
            port = arg
        elif opt in ("-o", "--out"):
            out = arg
    return network, port, out


def net_check(network):
    try:
        ipaddress.ip_network(network).hosts()
    except ValueError:
        print('address/netmask is invalid')
        sys.exit()
    return


def port_check(port):
    try:
        if int(port) not in range(1, 65535):
            print('Port must be from 1 to 65535')
            sys.exit()
    except ValueError:
        print('Port must be a number between 1 and 65535')
        sys.exit()
    return;


def outfile_check(out):
    if os.path.isfile(out):
        print('File ', out, ' exist!')
        sys.exit()


def main():
    network, port, out = cmd_args()

    # Basic checks
    net_check(network)
    port_check(port)
    outfile_check(out)

    print('-' * 30)
    print('Network is : ', network)
    print('Port is : ', port)
    print('Output files is : ', out)
    print('-' * 30)
    print('Scanning ...')

    iplist = ipaddress.ip_network(network).hosts()
    aliveips = []
    for ipaddr in iplist:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(1)
        result = sock.connect_ex((str(ipaddr), int(port)))
        sock.close()
        if result == 0:
            aliveips.append(str(ipaddr).strip())

    file = open(out, "w")
    writer = csv.writer(file, delimiter=',')
    writer.writerow([aliveips])
    file.close()

    print('Done.')


if __name__ == "__main__":
    main()
