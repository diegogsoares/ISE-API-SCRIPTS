import requests
import json
import sys
import math
from optparse import OptionParser
from optparse import OptionGroup

sys.path.append('../')
from config import config

requests.packages.urllib3.disable_warnings()
########################################################################
#####################################
######## Required Variables
#####################################
ise_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
network_devices_url = "https://"+config.ise_host+":9060/ers/config/networkdevice"

#####################################
######## List Network Devices
#####################################
def list_network_devices (net_device):

    if net_device == "ALL":
        network_devices = requests.get(network_devices_url+"?size=10", auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
        if network_devices.status_code != 200:
            print("ISE Connection Failed! " + str(network_devices.status_code))
            sys.exit()

        devices_json = network_devices.json()
        total_devices = devices_json.get('SearchResult').get('total')
        pages = math.ceil(total_devices/100)
        i=1
        while i <= pages:
            network_devices = requests.get(network_devices_url + "?size=100&page="+str(i), auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
            if network_devices.status_code != 200:
                print("ISE Connection Failed! " + str(network_devices.status_code))
                sys.exit()

            devices_json = network_devices.json()
            for device in devices_json['SearchResult']['resources']:
                network_device = requests.get(network_devices_url+"/"+device['id'], auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
                if network_device.status_code != 200:
                    print("ISE Connection Failed! " + str(network_device.status_code))
                    sys.exit()

                network_device = network_device.json()
                device_ip_list = network_device['NetworkDevice']['NetworkDeviceIPList']
                device_ip = ""
                for device_ip_info in device_ip_list:
                    device_ip_address = device_ip_info.get('ipaddress')
                    device_ip_mask = device_ip_info.get('mask')
                    device_ip += device_ip_address+"/"+str(device_ip_mask)+"  "
                print ("Found "+device['name']+" - IP: "+device_ip)
            i += 1
    else:
        id = get_device_id_by_name(net_device, "-")
        network_device = requests.get(network_devices_url + "/" + id, auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
        if network_device.status_code != 200:
            print("ISE Connection Failed! " + str(network_device.status_code))
            sys.exit()

        network_device = network_device.json()
        device_ip_list = network_device['NetworkDevice']['NetworkDeviceIPList']
        device_ip = ""
        for device_ip_info in device_ip_list:
            device_ip_address = device_ip_info.get('ipaddress')
            device_ip_mask = device_ip_info.get('mask')
            device_ip += device_ip_address + "/" + str(device_ip_mask) + "  "
        print ("Found " + net_device + " - IP: " + device_ip)


    return ()


#####################################
######## Create Network Devices
#####################################
def create_network_devices (file):

    #Load File values in a parsable variable
    for devices in file:
        devices = devices.replace('\n', '')
        devices_var = devices.split(',')

        create_payload = {}
        # Test if line is not the Header Line and if it contain required fields!
        if (devices_var[0] != "" and devices_var[2] != "" and devices_var[3] != "") and (devices_var[0].find("Required") == -1 and devices_var[2].find("Required") == -1 and devices_var[3].find("Required") == -1):
            create_payload['NetworkDevice'] = {}
            create_payload['NetworkDevice']['name'] = devices_var[0]
            create_payload['NetworkDevice']['profileName'] = "Cisco"
            ip_info = {
                "ipaddress": devices_var[2],
                "mask": devices_var[3]
            }
            create_payload['NetworkDevice']['NetworkDeviceIPList'] = []
            create_payload['NetworkDevice']['NetworkDeviceIPList'].append(ip_info)
            # Update description
            if devices_var[1] != "":
                create_payload['NetworkDevice']['description'] = devices_var[1]
            else:
                create_payload['NetworkDevice']['description'] = ""
            # Update CoA Port
            if devices_var[5] != "":
                create_payload['NetworkDevice']['coaPort'] = devices_var[5]
            else:
                create_payload['NetworkDevice']['coaPort'] = "1700"
            # Update RADIUS Secret
            if devices_var[4] != "":
                radius_info = {
                    'networkProtocol': "RADIUS",
                    'radiusSharedSecret': devices_var[4]
                }
                create_payload['NetworkDevice']['authenticationSettings'] = radius_info
            # Update TACACS Secret
            if devices_var[6] != "":
                tacacs_info = {
                    'connectModeOptions': "OFF",
                    'sharedSecret': devices_var[6]
                }
                create_payload['NetworkDevice']['tacacsSettings'] = tacacs_info
            # Update SNMP
            if devices_var[7] != "" and devices_var[8] != "":
                if devices_var[7] == "2c":
                    snmp_info = {
                        'pollingInterval': "28800",
                        'linkTrapQuery': "true",
                        'macTrapQuery': "true",
                        'originatingPolicyServicesNode': "Auto",
                        'version': "TWO_C",
                        'roCommunity': devices_var[8]
                    }
                    create_payload['NetworkDevice']['snmpsettings'] = snmp_info
                elif devices_var[7] == "3":
                    snmp_info = {
                        'pollingInterval': "28800",
                        'linkTrapQuery': "true",
                        'macTrapQuery': "true",
                        'originatingPolicyServicesNode': "Auto",
                        'version': "THREE",
                        'roCommunity': devices_var[8]
                    }
                    create_payload['NetworkDevice']['snmpsettings'] = snmp_info
            # Update Location
            if devices_var[9] != "":
                create_payload['NetworkDevice']['NetworkDeviceGroupList'] = []
                create_payload['NetworkDevice']['NetworkDeviceGroupList'].append("Location#"+devices_var[9])
            # Update Device Type
            if devices_var[10] != "":
                if create_payload['NetworkDevice']['NetworkDeviceGroupList']:
                    create_payload['NetworkDevice']['NetworkDeviceGroupList'].append("Device Type#"+devices_var[10])
                else:
                    create_payload['NetworkDevice']['NetworkDeviceGroupList'] = []
                    create_payload['NetworkDevice']['NetworkDeviceGroupList'].append("Device Type#"+devices_var[10])

            #Uncomment to Troubleshoot
            #print(json.dumps(create_payload, indent=4, sort_keys=True))

            create_payload_json = json.dumps(create_payload)
    
            network_devices = requests.post(network_devices_url, auth=(config.ise_username, config.ise_password), data=create_payload_json, headers=ise_header, verify=False)
            if network_devices.status_code != 201:
                print("Creating "+devices_var[0]+" device Failed! " + str(network_devices.status_code))
                print(network_devices.content)
            else:
                print(devices_var[0]+" - Created Successfully!")

    return ()


#####################################
######## Get Network Device ID
#####################################
def get_device_id_by_name (device_name,device_ip):

    if device_ip != "-":
        url = network_devices_url+"?filter=name.EQ."+device_name+"&ipaddress.EQ."+device_ip
    else:
        url = network_devices_url + "?filter=name.EQ." + device_name

    network_devices = requests.get(url, auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
    if network_devices.status_code != 200:
        print("Failed to find "+device_name+"! " + str(network_devices.status_code))
        id = "NONE"
    else:
        device_json = network_devices.json()
        if device_json['SearchResult']['total'] == 0:
            print("Failed to find " + device_name + "! ")
            id = "NONE"
        else:
            id = device_json['SearchResult']['resources'][0]['id']

    return (id)

#####################################
######## Delete Network Devices
#####################################
def delete_network_devices (file):

    #Load File values in a parsable variable
    for devices in file:
        devices = devices.replace('\n', '')
        devices_var = devices.split(',')

        # Test if line is not the Header Line and if it contain required fields!
        if (devices_var[0] != "" and devices_var[2] != "" and devices_var[3] != "") and (devices_var[0].find("Required") == -1 and devices_var[2].find("Required") == -1 and devices_var[3].find("Required") == -1):
            # Get Device id
            device_id = get_device_id_by_name(devices_var[0],devices_var[2])
            if device_id != "NONE":
                # Delete Device
                network_devices = requests.delete(network_devices_url+"/"+device_id, auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
                if network_devices.status_code != 204:
                    print("Device Deletion Failed! " + str(network_devices.status_code))
                    print(network_devices.content)
                else:
                    print("Device "+devices_var[0]+" deleted Successfully! ")


    return ()


#####################################
######## MAIN Function
#####################################
def main ():

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("-l", "--list", action="store", dest="list", help="List Network Device, if keyword \"ALL\" is used all devices will be listed.")
    parser.add_option("-c", "--create",action="store_true", dest="create", default=False, help="Create Network Devices in ISE based on devices.csv or file path if provided")
    parser.add_option("-d", "--delete", action="store_true", dest="delete", default=False, help="Delete Network Devices from ISE based on devices.csv or file path if provided")
    parser.add_option("-f", "--file", action="store", dest="file", help="file path, if none provided default is devices.csv")

    options, args = parser.parse_args()

    if len(args) != 0 or not (options.list or options.create or options.delete):
        parser.error("Required arguments have not been supplied.\tUse -h to get more information.\n")
        sys.exit()

    if options.list:
        list_network_devices(options.list)

    if options.create:
        if options.file:
            file_path = options.file
        else:
            file_path = "devices.csv"

        try:
            file = open(file_path, 'r', encoding='utf-8').readlines()

        except:
            print("Could not open File! ")
            sys.exit()

        create_network_devices(file)

    if options.delete:
        if options.file:
            file_path = options.file
        else:
            file_path = "devices.csv"

        try:
            file = open(file_path, 'r', encoding='utf-8').readlines()

        except:
            print("Could not open File! ")
            sys.exit()

        delete_network_devices(file)

    return


#####################################
######## BEGINNING
#####################################
main()
