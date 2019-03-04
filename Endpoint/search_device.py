import requests
from optparse import OptionParser
from optparse import OptionGroup
import validators
import sys
import json
import time
from datetime import datetime

requests.packages.urllib3.disable_warnings()

#ise_host = '10.87.31.46'
#ise_header = {'Authorization': 'Basic ZXJzYWRtaW46Q2lzY28xMjM0NSE=', 'Accept': 'application/json', 'Content-Type': 'application/json'}

ise_host = '10.101.7.250'
ise_header = {'Authorization': 'Basic ZXJzYWRtaW46RFNoYWNrQGRtMW4=', 'Accept': 'application/json', 'Content-Type': 'application/json'}

create_url = 'https://'+ise_host+':9060/ers/config/endpoint/'
check_mac_url = 'https://'+ise_host+':9060/ers/config/endpoint?filter=mac.EQ.'
check_group_url = 'https://'+ise_host+':9060/ers/config/endpointgroup/?filter=name.EQ.'
profile_url = 'https://'+ise_host+':9060/ers/config/profilerprofile/'

bay_min=101
bay_max=336

#####################################
########
#####################################
def check_device(url):

    device = requests.get(url, headers=ise_header, verify=False)
    if device.status_code != 200:
        return "ISE Connection Failed! " + str(device.status_code)

    device_json = device.json()

    return (device_json.get("ERSEndPoint").get("id"))

#####################################
########
#####################################
def check_location (location):

    check_group = requests.get(check_group_url+location, headers=ise_header, verify=False)
    if check_group.status_code != 200:
        return "ISE Connection Failed! " + str(check_group.status_code)

    check_group_json = check_group.json()
    total_groups = check_group_json.get('SearchResult').get('total')

    if (int(total_groups) != 0):
        location_list = check_group_json.get('SearchResult').get('resources')
        location_id = location_list[0].get("id")
    else:
        print ("Group does not exist in ISE!")
        sys.exit()


    return (location_id)


#####################################
########
#####################################
def build_html (ip_line,mac_line,bay_line,device_type_line):

    #print (bay_line)
    #print (device_type_line)

    code = ''

    if ip_line != '-':
        if ip_line == "NO_IP":
            code = "<h3>IP NOT found!</h3>"
        else:
            ip_line = ip_line.replace('\n', '')
            ip_line_var = ip_line.split(',')
            code = """<h3>IP found!</h3>
            <table class="w3-table-all w3-margin-top" style="width:90%;" id="myTable">
            <tr><th onclick="sortTable(0)">Source</th><th onclick="sortTable(1)">MAC address</th><th onclick="sortTable(2)">IP</th><th onclick="sortTable(3)">Profile</th><th onclick="sortTable(4)">Device Type</th><th onclick="sortTable(5)">Interface</th><th onclick="sortTable(6)">Switch</th><th onclick="sortTable(7)">Vlan</th><th onclick="sortTable(8)">Bay</th><th  onclick="sortTable(9)">QoS Policy</th></tr>
            <tr><td>"""+str(ip_line_var[4])+"""</td><td>"""+str(ip_line_var[0])+"""</td><td>"""+str(ip_line_var[9])+"""</td><td>"""+str(ip_line_var[2])+"""</td>
            <td>"""+str(ip_line_var[3])+"""</td><td>"""+str(ip_line_var[13])+"""</td><td>"""+str(ip_line_var[10])+"""</td><td>"""+str(ip_line_var[11])+"""</td><td>"""+str(ip_line_var[12])+"""</td>
            <td>"""+str(ip_line_var[14])+"""</td></tr></table><br>"""

    if mac_line != '-':
        if mac_line == "NO_MAC":
            code += "<h3>MAC NOT found!</h3>"
        else:
            mac_line = mac_line.replace('\n', '')
            mac_line_var = mac_line.split(',')
            code += """<h3>MAC found!</h3>
            <table class="w3-table-all w3-margin-top" style="width:90%;" id="myTable">
            <tr><th onclick="sortTable(0)">Source</th><th onclick="sortTable(1)">MAC address</th><th onclick="sortTable(2)">IP</th><th onclick="sortTable(3)">Profile</th><th onclick="sortTable(4)">Device Type</th><th onclick="sortTable(5)">Interface</th><th onclick="sortTable(6)">Switch</th><th onclick="sortTable(7)">Vlan</th><th onclick="sortTable(8)">Bay</th><th  onclick="sortTable(9)">QoS Policy</th></tr>
            <tr><td>"""+str(mac_line_var[4])+"""</td><td>"""+str(mac_line_var[0])+"""</td><td>"""+str(mac_line_var[9])+"""</td><td>"""+str(mac_line_var[2])+ """</td>
            <td>"""+str(mac_line_var[3])+"""</td><td>"""+str(mac_line_var[13])+"""</td><td>"""+str(mac_line_var[10])+"""</td><td>"""+str(mac_line_var[11])+"""</td><td>"""+str(mac_line_var[12])+"""</td>
            <td>"""+str(mac_line_var[14])+"""</td></tr></table><br>"""


    if bay_line:
        code += """<h3>Bay found!</h3>
        <table class="w3-table-all w3-margin-top" style="width:90%;" id="myTable">
        <tr><th onclick="sortTable(0)">Source</th><th onclick="sortTable(1)">MAC address</th><th onclick="sortTable(2)">IP</th><th onclick="sortTable(3)">Profile</th><th onclick="sortTable(4)">Device Type</th><th onclick="sortTable(5)">Interface</th><th onclick="sortTable(6)">Switch</th><th onclick="sortTable(7)">Vlan</th><th onclick="sortTable(8)">Bay</th><th  onclick="sortTable(9)">QoS Policy</th></tr>"""
        for line in bay_line:
            line = line.replace('\n', '')
            line_var = line.split(',')
            code +="""<tr><td>"""+str(line_var[4])+"""</td><td>"""+str(line_var[0])+"""</td><td>"""+str(line_var[9])+"""</td><td>"""+str(line_var[2])+ """</td>
            <td>"""+str(line_var[3])+"""</td><td>"""+str(line_var[13])+"""</td><td>"""+str(line_var[10])+"""</td><td>"""+str(line_var[11])+"""</td><td>"""+str(line_var[12])+"""</td>
            <td>"""+str(line_var[14])+"""</td></tr>"""

        code +="</table><br>"

    if device_type_line:
        code += """<h3>Type found!</h3>
        <table class="w3-table-all w3-margin-top" style="width:90%;" id="myTable">
        <tr><th onclick="sortTable(0)">Source</th><th onclick="sortTable(1)">MAC address</th><th onclick="sortTable(2)">IP</th><th onclick="sortTable(3)">Profile</th><th onclick="sortTable(4)">Device Type</th><th onclick="sortTable(5)">Interface</th><th onclick="sortTable(6)">Switch</th><th onclick="sortTable(7)">Vlan</th><th onclick="sortTable(8)">Bay</th><th  onclick="sortTable(9)">QoS Policy</th></tr>"""
        for line in device_type_line:
            line = line.replace('\n', '')
            line_var = line.split(',')
            code +="""<tr><td>"""+str(line_var[4])+"""</td><td>"""+str(line_var[0])+"""</td><td>"""+str(line_var[9])+"""</td><td>"""+str(line_var[2])+ """</td>
            <td>"""+str(line_var[3])+"""</td><td>"""+str(line_var[13])+"""</td><td>"""+str(line_var[10])+"""</td><td>"""+str(line_var[11])+"""</td><td>"""+str(line_var[12])+"""</td>
            <td>"""+str(line_var[14])+"""</td></tr>"""

        code +="</table><br>"

    if device_type_line and bay_line:
        code = """<h3>Devices found!</h3>
        <table class="w3-table-all w3-margin-top" style="width:90%;" id="myTable">
        <tr><th onclick="sortTable(0)">Source</th><th onclick="sortTable(1)">MAC address</th><th onclick="sortTable(2)">IP</th><th onclick="sortTable(3)">Profile</th><th onclick="sortTable(4)">Device Type</th><th onclick="sortTable(5)">Interface</th><th onclick="sortTable(6)">Switch</th><th onclick="sortTable(7)">Vlan</th><th onclick="sortTable(8)">Bay</th><th  onclick="sortTable(9)">QoS Policy</th></tr>"""
        for line in device_type_line:
            line = line.replace('\n', '')
            for line1 in bay_line:
                line1 = line1.replace('\n', '')
                if line == line1:
                    line_var = line.split(',')
                    code += """<tr><td>""" + str(line_var[4]) + """</td><td>""" + str(
                        line_var[0]) + """</td><td>""" + str(line_var[9]) + """</td><td>""" + str(line_var[2]) + """</td>
                    <td>""" + str(line_var[3]) + """</td><td>""" + str(line_var[13]) + """</td><td>"""+str(line_var[10])+"""</td><td>""" + str(
                        line_var[11]) + """</td><td>""" + str(line_var[12]) + """</td>
                    <td>""" + str(line_var[14]) + """</td></tr>"""
        code += "</table><br>"

    return (code)

#####################################
########
#####################################
def search_file (location,mac,bay_number,ip,device_type):

    endpoint_file = open('/Users/disoares/src/DS/ISE/device_inventory/endpoint_latest.csv', 'r', encoding='utf-8').readlines()
    profile_file = open('/Users/disoares/src/DS/ISE/device_inventory/profile_mapping.csv', 'r', encoding='utf-8').readlines()
    bay_file = open('/Users/disoares/src/DS/ISE/device_inventory/bay_mapping.csv', 'r', encoding='utf-8').readlines()

    count_ip=count_mac=count_bay=count_type = 0
    ip_return_line=mac_return_line='-'
    bay_return_line =[]
    device_return_line = []

    if ip != '-':
        ip_return_line = "NO_IP"
        for endpoint_line in endpoint_file:
            endpoint_line = endpoint_line.replace('\n', '')
            endpoint_line_var = endpoint_line.split(',')
            if ip == endpoint_line_var[9]:
                ip_return_line = endpoint_line

    if mac != '-':
        mac_return_line = "NO_MAC"
        for endpoint_line in endpoint_file:
            endpoint_line = endpoint_line.replace('\n', '')
            endpoint_line_var = endpoint_line.split(',')
            if mac == endpoint_line_var[0]:
                mac_return_line = endpoint_line

    if bay_number != '-':
        for bay_line in bay_file:
            bay_line = bay_line.replace('\n', '')
            bay_line_var = bay_line.split(',')
            if bay_number == bay_line_var[4]:
                bay_profile = bay_line_var[0]

        for endpoint_line in endpoint_file:
            endpoint_line = endpoint_line.replace('\n', '')
            endpoint_line_var = endpoint_line.split(',')
            if bay_profile == endpoint_line_var[12]:
                bay_return_line.append(endpoint_line)

    if device_type != '-':
        for profile_line in profile_file:
            profile_line = profile_line.replace('\n', '')
            profile_line_var = profile_line.split(',')
            if device_type == profile_line_var[0]:
                device_profile = profile_line_var[1]

        for endpoint_line in endpoint_file:
            endpoint_line = endpoint_line.replace('\n', '')
            endpoint_line_var = endpoint_line.split(',')
            if device_type == endpoint_line_var[3] or (device_profile in endpoint_line_var[2]):
                device_return_line.append(endpoint_line)



    html = build_html(ip_return_line,mac_return_line,bay_return_line,device_return_line)

    return (html)

#####################################
########
#####################################
def main ():

    parser = OptionParser(usage="usage: %prog [options]",
                          version="%prog 1.0")

    required = OptionGroup(parser, "Required Arguments")
    required.add_option("-l", "--location", action="store", dest="location", help="ISE deployment should device be created in. ")
    required.add_option("-m", "--mac",action="store", dest="mac", help="MAC Address of device to be created in ISE. ")
    required.add_option("-b", "--bay", action="store", dest="bay_number", help="Bay Number should device be assigned to. ")
    required.add_option("-i", "--ip", action="store", dest="ip", help="Device IP Address. ")
    required.add_option("-t", "--devicetype", action="store",  dest="device_type", help="Device type from the MAC Address. ")
    parser.add_option_group(required)

    options, args = parser.parse_args()

    if len(args) != 0 or not options.location or not (options.mac or options.bay_number or options.ip  or options.device_type):
        parser.error("Required arguments have not been supplied.  \n\t\tUse -h to get more information.")
        sys.exit()

    device_type = ip = mac = bay_number = '-'

    if options.mac:
        if validators.mac_address(options.mac):
            mac = options.mac
        else:
            print ("Invalid MAC Address! ")
            sys.exit()

    if options.bay_number:
        if validators.between(int(options.bay_number), bay_min, bay_max):
            bay_number = options.bay_number
        elif int(options.bay_number) == 0:
            bay_number = options.bay_number
        else:
            print ("Invalid Bay Number! ")
            sys.exit()

    if options.ip:
        if validators.ipv4(options.ip):
            ip = options.ip
        else:
            print ("Invalid IP! ")
            sys.exit()

    if options.device_type:
        device_type = options.device_type

    update_result = search_file(options.location,mac,bay_number,ip,device_type)
    #time.sleep(1)
    print (update_result)

    return

main()