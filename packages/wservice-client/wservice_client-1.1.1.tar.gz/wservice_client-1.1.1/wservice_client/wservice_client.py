import requests
from urllib.parse import urlparse
import logging
import os

class WServiceClient:
    """Class responsible for communication with the web service."""

    def __init__(self, url):
        self.url = url

    def send_data(self, data):
        """Send data to the web service and return the response."""
        print(f"Sending request to {self.url} with data {data}")
        try:
            response = requests.post(self.url, json=data, timeout=5)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error: {timeout_err}")
            return None
        except requests.exceptions.RequestException as err:
            logging.error(f"An error occurred: {err}")
            return None
        else:
            try:
                return response.json()
            except ValueError:
                logging.error("Error: The response was not valid JSON.")
                return None

    def ping(self, ping_url):
        """Ping the specified server and return True if it's online, False otherwise."""
        try:
            response = os.system("ping -c 1 " + ping_url)
            return response == 0
        except Exception as e:
            logging.error(f"Ping error: {e}")
            return False

    def extract_ip(self):
        """Extract the IP address from the URL."""
        try:
            parsed_url = urlparse(self.url)
            domain = parsed_url.netloc.split(":")[0]
            parts = domain.split('.')
            if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                return domain
            else:
                raise ValueError("The domain does not appear to be an IP address.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def ping_get(self, ping_url):
        """Send a GET request to the given URL and return True if successful, False otherwise."""
        try:
            response = requests.get(ping_url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as err:
            logging.error(f"Error in GET request: {err}")
            return False

    def MAJ_PASSAGE_TICKET(self, cb, timeout=3, mode_prg="T",
                           user_agent="default_user_agent", sBadge_Ticket_Type="BILLET", stypeCRTL="SAL"):
        """Send a request to update ticket status."""
        headers = {'User-Agent': user_agent, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        httprequrl = f"{self.url}/{cb}/TODAY/{user_agent}/{mode_prg}/{sBadge_Ticket_Type}/{stypeCRTL}"
        try:
            response = requests.get(httprequrl, headers=headers, verify=False, timeout=timeout)
            if response.status_code != 200:
                logging.error(f"Non-200 status code: {response.status_code}")
                return "", "not_200"
            return response, "online"
        except requests.Timeout:
            logging.error("Timeout error in MAJ_PASSAGE_TICKET")
            return "", "timeout"
        except requests.ConnectionError:
            logging.error("Connection error in MAJ_PASSAGE_TICKET")
            return "", "connection_error"
        except requests.HTTPError:
            logging.error("HTTP error in MAJ_PASSAGE_TICKET")
            return "", "http_error"
        except Exception as e:
            logging.error(f"Unexpected error in MAJ_PASSAGE_TICKET: {e}")
            return "", "exception"
import requests
from urllib.parse import urlparse
import logging
import os

class WServiceClient:
    """Class responsible for communication with the web service."""

    def __init__(self, url):
        self.url = url

    def send_data(self, data):
        """Send data to the web service and return the response."""
        print(f"Sending request to {self.url} with data {data}")
        try:
            response = requests.post(self.url, json=data, timeout=5)
            response.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            logging.error(f"HTTP error occurred: {http_err}")
            return None
        except requests.exceptions.ConnectionError as conn_err:
            logging.error(f"Connection error: {conn_err}")
            return None
        except requests.exceptions.Timeout as timeout_err:
            logging.error(f"Timeout error: {timeout_err}")
            return None
        except requests.exceptions.RequestException as err:
            logging.error(f"An error occurred: {err}")
            return None
        else:
            try:
                return response.json()
            except ValueError:
                logging.error("Error: The response was not valid JSON.")
                return None

    def ping(self, ping_url):
        """Ping the specified server and return True if it's online, False otherwise."""
        try:
            response = os.system("ping -c 1 " + ping_url)
            return response == 0
        except Exception as e:
            logging.error(f"Ping error: {e}")
            return False

    def extract_ip(self):
        """Extract the IP address from the URL."""
        try:
            parsed_url = urlparse(self.url)
            domain = parsed_url.netloc.split(":")[0]
            parts = domain.split('.')
            if len(parts) == 4 and all(part.isdigit() and 0 <= int(part) <= 255 for part in parts):
                return domain
            else:
                raise ValueError("The domain does not appear to be an IP address.")
        except Exception as e:
            logging.error(f"An error occurred: {e}")
            return None

    def ping_get(self, ping_url):
        """Send a GET request to the given URL and return True if successful, False otherwise."""
        try:
            response = requests.get(ping_url)
            response.raise_for_status()
            return True
        except requests.exceptions.RequestException as err:
            logging.error(f"Error in GET request: {err}")
            return False

    def MAJ_PASSAGE_TICKET(self, cb, timeout=3, mode_prg="T",
                           user_agent="default_user_agent", sBadge_Ticket_Type="BILLET", stypeCRTL="SAL"):
        """Send a request to update ticket status."""
        headers = {'User-Agent': user_agent, 'Content-Type': 'application/json', 'Accept': 'application/json'}
        httprequrl = f"{self.url}/{cb}/TODAY/{user_agent}/{mode_prg}/{sBadge_Ticket_Type}/{stypeCRTL}"
        try:
            response = requests.get(httprequrl, headers=headers, verify=False, timeout=timeout)
            if response.status_code != 200:
                logging.error(f"Non-200 status code: {response.status_code}")
                return "", "not_200"
            return response, "online"
        except requests.Timeout:
            logging.error("Timeout error in MAJ_PASSAGE_TICKET")
            return "", "timeout"
        except requests.ConnectionError:
            logging.error("Connection error in MAJ_PASSAGE_TICKET")
            return "", "connection_error"
        except requests.HTTPError:
            logging.error("HTTP error in MAJ_PASSAGE_TICKET")
            return "", "http_error"
        except Exception as e:
            logging.error(f"Unexpected error in MAJ_PASSAGE_TICKET: {e}")
            return "", "exception"

