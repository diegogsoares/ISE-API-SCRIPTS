# Cisco ISE Basic API Calls Scripts

This project is a collection of Scripts that leverage ISE APIs (ISE 2.4 and above) for basic tasks. This will save a lot of repetitive clicks

## Getting Started

%%%%%%
These instructions will get you a copy of the project up and running on your local machine for development and testing purposes. See deployment for notes on how to deploy the project on a live system.
%%%%%%

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
```

## Deployment

Edit the config file for ISE IP/Hostname and Credentials.

```
ise_host = "10.10.10.10"
ise_username = "iseUsername"
ise_password = "isePassword"
```

## Running the tests

Explain how to run the automated tests for this system

```
Give an example
```

## Built With

* [PyCharm CE](https://www.jetbrains.com/pycharm/) - Python IDE

## Contributing

Diego Soares

## Authors

* **Diego Soares** - *Initial work* - [diegogsoares](https://github.com/diegogsoares)

See also the list of [contributors] who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* BIG THANK YOU for all my CISCO customers that challenged me with use cases.

