# -*- coding: utf-8 -*-
import os

from DDoS import *

databaseParams = {
    'database': '',
    'user': 'django',
    'password': 'django',
    'host': '192.168.0.110',
    'port': 5432
}

ddosDatabaseParams = databaseParams
ddosDatabaseParams['database'] = 'django'

startupScreen = 0


def main():
    if startupScreen:
        with open("sych_logo.txt", 'r') as fin:
            print fin.read()

    try:
        print """Select type of attack:
        1. DDoS
        2. Bruteforce / port scan
        3. Exit"""
        choice = int(raw_input("Choice: "))
    except ValueError:
        print "Incorrect choice"

    if choice == 1:
        dump = DDoS(sys.argv[1], ddosDatabaseParams)
        dump.parse()
        dump.load()

    elif choice == 3:
        sys.exit(1)


if __name__ == "__main__":
    # Файл передаётся как аргумент при запуске скрипта, указывается полный путь.
    # Если файл не открыт или произошла ошибка, срабатывает исключение.
    try:
        if len(sys.argv) < 2:
            raise OSError(
                "Input file is not selected."
                " Use '" + os.path.basename(__file__) + " /path/file.pcap' to select dump."
            )
        elif os.path.exists(sys.argv[1]) is not True:
            raise OSError(
                "Dump " + sys.argv[1] + " are not exist."
                                        " Use '" + os.path.basename(__file__) + " /path/file.pcap' to select dump."
            )
        print "Opened", sys.argv[1]
    except OSError, e:
        print e
        sys.exit(-1)
    main()
