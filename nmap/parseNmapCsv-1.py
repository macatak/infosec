import csv


# input file
# filename ="/home/bikeride/vscode/h2g2.csv"
filename ="/home/zaphod/vscode/nmap/metasploitable2.csv"
# services setup


perfdIPs = []
rpcbindIPs = []
rpcbindPorts = []
sshIPs = []
sshPorts = []

perfdPort = '5227'

with open(filename) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    line_count = 0
    for row in csv_reader:
        if line_count == 0:
            print(f'Column names are {", ".join(row)}')
            line_count += 1
        elif row[2] == '5227':
            # print(f'perfd on {row[0]}')
            perfdIPs.append(row[0])
            line_count += 1
        elif row[4] == 'ssh':
            sshIPs.append(row[0])
            line_count += 1
        elif row[4] == 'rpcbind':
            rpcbindIPs.append(row[0])
            rpcbindPorts.append(row[2])
            line_count += 1
        else:
            #print(f'IP - {row[0]} \t port: {row[2]} \t protocol: {row[3]} \t version: {row[4]}')
            print(f'{row[4]}')
            line_count += 1
    print(f'Processed {line_count} lines.')

 
print("IP's running rpcbind")
# rpcIpCount = rpcbindIPs.count()
rpcIpCount = len(rpcbindIPs)
for i in range(0, rpcIpCount):
    print('IP: {} : port: {}'.format(rpcbindIPs[i],rpcbindPorts[i]))

 

'''

for item in rpcbindIPs:
    print(IP = rpcbindIPs[]


print("IP's running SSH")
for item in sshIPs:
    print(item)
 

print("IP's running perfd")
for item in perfdIPs:
    print(item)
'''
 