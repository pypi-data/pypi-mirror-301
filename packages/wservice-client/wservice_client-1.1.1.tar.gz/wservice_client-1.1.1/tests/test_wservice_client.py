import unittest
from wservice_client.wservice_client import WServiceClient

class TestWServiceClient(unittest.TestCase):

    def setUp(self):
        self.client = WServiceClient("http://mockurl.com")

    def test_send_data(self):
        result = self.client.send_data({"key": "value"})
        self.assertIsNone(result)  # Assuming no actual server to test against

    def test_extract_ip(self):
        self.client.url = "http://192.168.0.1:8000"
        ip = self.client.extract_ip()
        self.assertEqual(ip, "192.168.0.1")

    def test_ping(self):
        self.assertFalse(self.client.ping("fakeurl.com"))

    def test_ping_get(self):
        self.assertFalse(self.client.ping_get("http://fakeurl.com"))

if __name__ == '__main__':
    unittest.main()

