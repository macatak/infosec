import csv

# functions
# move to a util file
def file2list(fileName, ListName):
    # open a file and return a list of the objects
    tmpList = {}
    tmpFile = open(fileName, 'r')
    tmpList.append(tmpFile.line)
    return(tmpList)
    

# map results in csv format
# uses this command to create CSV, from PyPl
# python nmaptocsv.py -d "," --script -n -x metasploitable2.xml -o metasploitable2.csv
csvNmapIn ="/home/zaphod/vscode/nmap/metasploitable2.csv"

# services setup
services = ["ajp13", "bindshell", "distccd", "domain", "drb", "exec", "ftp", "http", "irc", "java-rmi", "login", "mountd", "mysql", "netbios-ssn", "nfs", "nlockmgr", "postgresql", "shell", "smtp", "status", "telnet", "vnc", "X11", "unknown"]

# set the row values 
rowIp = 0
rowHostname = 1
rowPort = 2
rowProtocol = 3
rowService = 4
rowVersion = 5
rowScript = 6

with open(csvNmapIn) as csv_file:
    # create csv reader
    csv_reader = csv.reader(csv_file, delimiter=',')
    # set a counter
    line_count = 0
    # serviceCount = 0
    # read in the csv file
    for row in csv_reader:
        if line_count == 0:
            # helps in rev
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        else:
            for service in services:
                # sanity check
                # print('ip: {} checking for: {} reported port: {}'.format(row[0], service, row[2]))
                if service == row[4]:
                    # full version
                    # print('ip: {} service: {} port: {} version: {} script: {}'.format(row[rowIp],row[rowService],row[rowPort], row[rowVersion], row[rowScript]))
                    # goal is to write this to a file
                    print('csv out : {},{}'.format(row[rowIp],row[rowPort]))
            line_count += 1
