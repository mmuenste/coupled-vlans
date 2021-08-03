import argparse
import re
import sys

parser = argparse.ArgumentParser()

parser.add_argument('log_file', help='Specify the log file')

args = parser.parse_args()

root_ids = {}

# Inhalt des Log-Files in Dictionary einlesen
try:
    log = open(args.log_file)
except FileNotFoundError:
    print(f'File {args.log_file} not found!')
    sys.exit()

for line in log:
    line = line.strip().split()
    if len(line) >= 3 and re.match('^[0-9a-f]{4,4}\.' +
                                   '[0-9a-f]{4,4}\.[0-9a-f]{4,4}$',
                                   line[2]):
        root_ids[line[0]] = {'priority': line[1],
                             'mac': line[2],
                             'root_cost': line[3],
                             'hello_time': line[4],
                             'max_age': line[5],
                             'fwd_dly': line[6]
                             }
        if len(line) == 8:
            root_ids[line[0]]['root_port'] = line[7]
        else:
            root_ids[line[0]]['root_port'] = None
log.close()

# mehrfach auftauchende Root IDs ermittlen:
# Liste mit Root IDs erzeugen
root_id_list = [i['priority'] + ' ' + i['mac'] for i in root_ids.values()]

# Mehrfach vorkommende Root IDs filtern
multiple_root_ids = []
for i in set(root_id_list):
    if root_id_list.count(i) >= 2:
        multiple_root_ids.append(i)

# Ausgabe der mehrfach vorkommenden Root Ids
if multiple_root_ids:
    for i in multiple_root_ids:
        prio_mac = i.split()
        output = f'Root Bridge {prio_mac[0]} {prio_mac[1]} in VLANs: '
        for vlan, data in root_ids.items():
            if data['priority'] == prio_mac[0] and data['mac'] == prio_mac[1]:
                output += f'{vlan} '
        print(output)

else:
    print('No VLANs with the same ROOT ID found.')
