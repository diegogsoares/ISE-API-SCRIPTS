import requests
from optparse import OptionParser
from optparse import OptionGroup
import validators
import sys
import json
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

    try:
        custom_attribites = device_json.get("ERSEndPoint").get("customAttributes").get("customAttributes")

        profile = requests.get(profile_url+device_json.get("ERSEndPoint").get("profileId"), headers=ise_header, verify=False)
        if profile.status_code != 200:
            return "ISE Connection Failed! " + str(profile.status_code)

        profile_json = profile.json()
        profile_name = profile_json.get("ProfilerProfile").get("name")

        html ="""<h3>Device already exist! Device added via Web Portal.</h3><table class="w3-table-all w3-margin-top" style="width:70%;" id="myTable">
        <tr><th style="width:25%;">MAC address</th><th style="width:25%;">Profile</th><th style="width:25%;">Date created</th><th style="width:25%;">Device Type</th></tr>
        <tr><td>"""+str(device_json.get("ERSEndPoint").get("mac"))+"""</td><td>"""+str(profile_name)+"""</td><td>"""+str(device_json.get("ERSEndPoint").get("customAttributes").get("customAttributes").get("Update Date"))+"""</td><td>"""+str(device_json.get("ERSEndPoint").get("customAttributes").get("customAttributes").get("Device Type"))+"""</td></tr></table>"""

        return (html)

    except:
        profile = requests.get(profile_url+device_json.get("ERSEndPoint").get("profileId"), headers=ise_header, verify=False)
        if profile.status_code != 200:
            return "ISE Connection Failed! " + str(profile.status_code)

        profile_json = profile.json()
        profile_name = profile_json.get("ProfilerProfile").get("name")

        html ="""<h3>Device already exist! System Discovered.</h3><table class="w3-table-all w3-margin-top" style="width:70%;" id="myTable">
        <tr><th style="width:50%;">MAC address</th><th style="width:50%;">Profile</th></tr>
        <tr><td>"""+str(device_json.get("ERSEndPoint").get("mac"))+"""</td><td>"""+str(profile_name)+"""</td></tr></table>"""

        return (html)

    return

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
def post_ise (location,mac,bay_number,description,device_type):

    check = requests.get(check_mac_url+mac, headers=ise_header, verify=False)
    if check.status_code != 200:
        return "ISE Connection Failed! " + str(check.status_code)

    check_json = check.json()
    total_devices = check_json.get('SearchResult').get('total')

    if (int(total_devices) != 0):
        device = check_json.get('SearchResult').get('resources')
        device_url = device[0].get('link').get("href")
        return_html = check_device(device_url)
        return (return_html)

    location_id = check_location (location)

    date = datetime.now().strftime("%m/%d/%Y %H:%M")

    create_payload = [
    {
        "ERSEndPoint": {
            "name": mac,
            "description": description,
            "mac": mac,
            "profileId": "",
            "staticProfileAssignment": "false",
            "groupId": location_id,
            "staticGroupAssignment": "true",
            "portalUser": "",
            "identityStore": "",
            "identityStoreId": "",
            "customAttributes": {
                "customAttributes": {
                    "Update Date": date,
                    "BAY Number": bay_number,
                    "Device Type": device_type
                }
            }
        }
    }
    ]

    create_json = json.dumps(create_payload[0])

    post = requests.post(create_url, data=create_json ,headers=ise_header, verify=False)
    if post.status_code != 201:
        return "ISE Connection Failed! " + str(post.status_code)

    return ("Device created Successfully!")

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
    required.add_option("-d", "--description", action="store", dest="description", help="Device description. ")
    required.add_option("-t", "--devicetype", action="store",  dest="device_type", help="Device type from the MAC Address. ")
    parser.add_option_group(required)

    options, args = parser.parse_args()

    if len(args) != 0 or not options.location or not options.mac or not options.bay_number or not options.description  or not options.device_type:
        parser.error("Required arguments have not been supplied.  \n\t\tUse -h to get more information.")
        sys.exit()


    if validators.mac_address(options.mac):
        mac = options.mac
    else:
        print ("Invalid MAC Address! ")
        sys.exit()

    if validators.between(int(options.bay_number), bay_min, bay_max):
        bay_number = options.bay_number
    elif int(options.bay_number) == 0:
        bay_number = options.bay_number
    else:
        print ("Invalid Bay Number! ")
        sys.exit()

    if validators.length(options.description, min=1, max=30):
        description = options.description
    else:
        print ("Description too long! ")
        sys.exit()

    post_result = post_ise(options.location,mac,bay_number,description,options.device_type)

    print (post_result)

    return

main()