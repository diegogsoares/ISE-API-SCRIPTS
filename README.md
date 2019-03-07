# Cisco ISE Basic API Calls Scripts

This project is a collection of Scripts that leverage ISE APIs (ISE 2.4 and above) for basic tasks. This will save a lot of repetitive clicks

## Getting Started

This folder contains sub-folders named according to specific ISE configuration components. Inside each folder there is a script that allow operations like List, Create, Delete and Update. Some folders will have a template csv file that will be used as the input of information.

AuthoZ Profile Folder - Contains the script and template to List, Create and Delete Authorization Profiles.

config - Where configuration file is.

Network Devices Folder - Contains the script and template to List, Create and Delete Network Devices.


### Prerequisites

   - MAC, Linux (not supported on Windows)
   - python 3.x
   - pip package manager (https://pip.pypa.io/en/stable/installing/)
```bash
   If already installed, make sure that pip / setuptools are upto date (commands may vary)
   
   pip install --upgrade pip
   
   Ubuntu: sudo pip install --upgrade setuptools
```
   - virtualenv (recommended)
```bash
   Ubuntu: sudo apt-get install python-virtualenv
   Fedora: sudo dnf install python-virtualenv
   MAC: sudo pip install virtualenv
```

### Installing

Clone git repository
```bash
   git clone https://github.com/diegogsoares/ISE-API-SCRIPTS.git
   cd ISE-API-SCRIPTS
   python3 -m pip install -r requirements.txt 
```

## Deployment

Edit the config file inside config folder with proper ISE IP/Hostname and Credentials.

```
ise_host = "10.10.10.10"
ise_username = "iseUsername"
ise_password = "isePassword"
```

## Running ISE-API-SCRIPTS

#### Authorization Profiles 

Use -h option on each script to be presented with help.
```
cd AuthoZ Profile
python3 authorization_profile.py -h
```
Use -l option to List all Authorization Profiles.
```
cd AuthoZ Profile
python3 authorization_profile.py -l
```

Use -c option to create Authorization Profiles based on the template file or -d to delete.

Note: When create or delete is selected the -f option is a requirement to indicate the file to be used as input for the script.
```
cd AuthoZ Profile
python3 authorization_profile.py -c -f authz_profile_template.csv 
```

#### Network Devices

Use -h option on each script to be presented with help.
```
cd Network Devices
python3 network_device.py -h
```
Use -l option to List all Network Devices.
```
cd Network Devices
python3 network_device.py -l
```

Use -c option to create Network Devices based on the template file or -d to delete.

Note: When create or delete is selected the -f option is a requirement to indicate the file to be used as input for the script.
```
cd Network Devices
python3 network_device.py -c -f network_devices_template.csv 
```
## Built With

* [PyCharm CE](https://www.jetbrains.com/pycharm/) - Python IDE

## Contributing

none

## Authors

* **Diego Soares** - *Initial work* - [diegogsoares](https://github.com/diegogsoares)

See also the list of [contributors] who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details

## Acknowledgments

* BIG THANK YOU to all my CISCO customers that challenged me with use cases.

