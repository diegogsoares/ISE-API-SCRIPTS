import requests
import json
import sys
from optparse import OptionParser

sys.path.append('../')
from config import config

requests.packages.urllib3.disable_warnings()
########################################################################
#####################################
######## Required Variables
#####################################
ise_header = {'Accept': 'application/json', 'Content-Type': 'application/json'}
authz_profile_url = "https://"+config.ise_host+":9060/ers/config/authorizationprofile"

#####################################
######## List Authorization Profiles
#####################################
def list_authz_profile (authz_profile_name):

    if authz_profile_name == "ALL":
        authz_profiles = requests.get(authz_profile_url, auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
        if authz_profiles.status_code != 200:
            print("ISE Connection Failed! " + str(authz_profiles.status_code))
            sys.exit()

        authzs_json = authz_profiles.json()
        for authz in authzs_json['SearchResult']['resources']:
            network_authz = requests.get(authz_profile_url+"/"+authz['id'], auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
            if network_authz.status_code != 200:
                print("ISE Connection Failed! " + str(network_authz.status_code))
                sys.exit()

            network_authz = network_authz.json()
            print ("Found "+authz['name']+" Authorization Profile. - Description: "+network_authz.get('AuthorizationProfile').get('description'))

    else:
        authz_profiles = requests.get(authz_profile_url + "/name/" + authz_profile_name, auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
        if authz_profiles.status_code != 200:
            print("ISE Connection Failed! " + str(authz_profiles.status_code))
            sys.exit()

        authz_profiles = authz_profiles.json()
        print ("Found " + authz_profiles.get('AuthorizationProfile').get('name') + " Authorization Profile. - Description: " + authz_profiles.get('AuthorizationProfile').get('description'))


    return ()


#####################################
######## Create Authorization Profiles
#####################################
def create_authz_profile (file):

    #Load File values in a parsable variable
    for profiles in file:
        profiles = profiles.replace('\n', '')
        profiles_var = profiles.split(',')

        create_payload = {}
        # Test if line is not the Header Line and if it contain required fields!
        if (profiles_var[0] != "" and profiles_var[2] != "") and (profiles_var[0].find("Required") == -1 and profiles_var[2].find("Required") == -1):
            create_payload['AuthorizationProfile'] = {}
            create_payload['AuthorizationProfile']['name'] = profiles_var[0]
            create_payload['AuthorizationProfile']['accessType'] = profiles_var[2]
            # Update description
            if profiles_var[1] != "":
                create_payload['AuthorizationProfile']['description'] = profiles_var[1]
            # Update Vlan id
            if profiles_var[3] != "":
                vlan_info = {
                    "tagID": "1",
                    "nameID": profiles_var[3]
                }
                create_payload['AuthorizationProfile']['vlan'] = vlan_info
            # Update Voice Vlan
            if profiles_var[4].lower != "yes":
                create_payload['AuthorizationProfile']['voiceDomainPermission'] = "true"
            # Update dACL
            if profiles_var[5] != "":
                create_payload['AuthorizationProfile']['daclName'] = profiles_var[5]
            # Update Reauth Timer
            if profiles_var[6] != "":
                timer_info = {
                    'connectivity': "RADIUS_REQUEST",
                    'timer': profiles_var[6]
                }
                create_payload['AuthorizationProfile']['reauth'] = timer_info
            # Update Interface Template
            if profiles_var[7] != "":
                create_payload['AuthorizationProfile']['interfaceTemplate'] = profiles_var[7]

            #Uncomment to Troubleshoot
            #print(json.dumps(create_payload, indent=4, sort_keys=True))

            create_payload_json = json.dumps(create_payload)
    
            authz_profiles = requests.post(authz_profile_url, auth=(config.ise_username, config.ise_password), data=create_payload_json, headers=ise_header, verify=False)
            if authz_profiles.status_code != 201:
                print("Creating "+profiles_var[0]+" Authorization Profile Failed! " + str(authz_profiles.status_code))
                print(authz_profiles.content)
            else:
                print(profiles_var[0]+" - Created Successfully!")

    return ()


#####################################
######## Delete Authorization Profile
#####################################
def delete_authz_profile (file):

    #Load File values in a parsable variable
    for profiles in file:
        profiles = profiles.replace('\n', '')
        profiles_var = profiles.split(',')

        # Test if line is not the Header Line and if it contain required fields!
        if (profiles_var[0] != "" and profiles_var[2] != "") and (profiles_var[0].find("Required") == -1 and profiles_var[2].find("Required") == -1):
            # Get Authorization Profile id
            authz_profiles = requests.get(authz_profile_url + "/name/" + profiles_var[0], auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
            if authz_profiles.status_code != 200:
                print("Failed to find "+profiles_var[0]+"! " + str(authz_profiles.status_code))
                continue

            authzs_json = authz_profiles.json()
            authz_id = authzs_json.get('AuthorizationProfile').get('id')
            # Delete Authorization Profile
            authz_profiles = requests.delete(authz_profile_url+"/"+authz_id, auth=(config.ise_username, config.ise_password), headers=ise_header, verify=False)
            if authz_profiles.status_code != 204:
                print("Failed to delete "+profiles_var[0]+"! " + str(authz_profiles.status_code))
                print(authz_profiles.content)
            else:
                print("Authorization Profile "+profiles_var[0]+" deleted Successfully! ")


    return ()


#####################################
######## MAIN Function
#####################################
def main ():

    parser = OptionParser(usage="usage: %prog [options]", version="%prog 1.0")
    parser.add_option("-l", "--list", action="store", dest="list", help="List Authorization Profiles, if keyword \"ALL\" is used all Authorization Profiles will be listed.")
    parser.add_option("-c", "--create",action="store_true", dest="create", default=False, help="Create Authorization Profiles in ISE based on auth_profile.csv or file path if provided")
    parser.add_option("-d", "--delete", action="store_true", dest="delete", default=False, help="Delete NAuthorization Profiles from ISE based on auth_profile.csv or file path if provided")
    parser.add_option("-f", "--file", action="store", dest="file", help="file path, if none provided default is auth_profile.csv")

    options, args = parser.parse_args()

    if len(args) != 0 or not (options.list or options.create or options.delete):
        parser.error("Required arguments have not been supplied.\tUse -h to get more information.\n")
        sys.exit()

    if options.list:
        list_authz_profile(options.list)

    if options.create:
        if options.file:
            file_path = options.file
        else:
            file_path = "auth_profile.csv"

        try:
            file = open(file_path, 'r', encoding='utf-8').readlines()

        except:
            print("Could not open File! ")
            sys.exit()

        create_authz_profile(file)

    if options.delete:
        if options.file:
            file_path = options.file
        else:
            file_path = "auth_profile.csv"

        try:
            file = open(file_path, 'r', encoding='utf-8').readlines()

        except:
            print("Could not open File! ")
            sys.exit()

        delete_authz_profile(file)

    return


#####################################
######## BEGINNING
#####################################
main()
