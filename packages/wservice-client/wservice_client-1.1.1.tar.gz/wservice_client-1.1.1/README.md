# WServiceClient

**WServiceClient** is a Python package designed for easy communication with web services. It allows you to send data, ping servers, perform HTTP requests, and extract IP addresses from URLs.

## Features

- Send JSON data to a web service
- Perform GET requests for specific web service endpoints
- Ping servers to check their availability
- Extract IP addresses from URLs
- Handle HTTP errors, timeouts, and connection errors gracefully

## Installation

You can install `wservice_client` directly from PyPI:

```bash
pip install wservice-client
```
Alternatively, if you want to install it from the source, clone the repository and install it locally:

```bash
git clone git@github.com:mnedev-cell/wservice_client.git
cd wservice_client
pip install .
```

## Usage
Here’s how to use the WServiceClient in your project:

Initialize the Client
You can initialize the WServiceClient with the URL of the web service you want to communicate with:
```bash
from wservice_client import WServiceClient

# Initialize the client with the base URL of the web service
ws_client = WServiceClient("http://example.com/webservice")

```

# Send Data to the Web Service
You can send JSON data to the web service using the send_data method:

```bash
data = {"key": "value"}
response = ws_client.send_data(data)
print("Response:", response)
```

# Ping a Server
You can check if a server is online by using the ping method:
```bash
is_online = ws_client.ping("example.com")
print("Server online:", is_online)
```
# Extract IP Address from URL
You can extract the IP address from a URL using the extract_ip method:

```bash
ip_address = ws_client.extract_ip()
print("Extracted IP:", ip_address)
```

# Perform a GET Request with MAJ_PASSAGE_TICKET
You can use the MAJ_PASSAGE_TICKET method to perform a GET request to update ticket status with custom parameters

```bash
response, status = ws_client.MAJ_PASSAGE_TICKET(
    cb="codebarre", 
    mode_prg="N", 
    user_agent="Agent", 
    sBadge_Ticket_Type="BILLET", 
    stypeCRTL="SAL"
)
print("Response:", response, "Status:", status)
```

# Running Tests
To ensure everything works properly, run the unit tests provided in the tests folder:

```bash
python -m unittest discover tests
```
This will execute all test cases for the WServiceClient class.

# Contributing
Contributions are welcome! If you find any bugs or have any suggestions for improvements, please feel free to open an issue or submit a pull request on GitHub.

Fork the repository
Create your feature branch (git checkout -b feature/AmazingFeature)
Commit your changes (git commit -m 'Add some AmazingFeature')
Push to the branch (git push origin feature/AmazingFeature)
Open a pull request
License
This project is licensed under the MIT License. See the LICENSE file for details.

# Acknowledgements
This package uses the requests library to handle HTTP requests. For more information about requests, check out the documentation.Usage
Here’s how to use the WServiceClient in your project:
### Breakdown of the Sections:

1. **Features**: Lists the main capabilities of the `WServiceClient`.
2. **Installation**: Instructions for installing the package from PyPI or from source via GitHub.
3. **Usage**: Sample code to help users quickly understand how to use the client.
4. **Running Tests**: Instructions on how to run unit tests.
5. **Contributing**: Guidelines for contributing to the project.
6. **License**: Information about the project's licensing.

This `README.md` is comprehensive and serves as both your PyPI project description and GitHub repository guide.

```bash
wservice_client/              # Project root directory
│
├── wservice_client/          # Main package folder
│   └── __init__.py           # Initialize the package
│   └── wservice_client.py    # The WServiceClient class (your main module)
├── tests/                    # Unit tests
│   └── test_wservice_client.py
├── README.md                 # Project README with instructions and usage
├── setup.py                  # Setup script for PyPI
└── requirements.txt          # Dependencies (like `requests`)
```
