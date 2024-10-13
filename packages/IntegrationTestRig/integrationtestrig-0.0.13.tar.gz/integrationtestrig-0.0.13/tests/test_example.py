import requests
from IntegrationTestRig.IntegrationTestRig import IntegrationTestRig

class TestExample(IntegrationTestRig):
    resource_file = "ExampleService.py"

    def test_example(self):
        response = requests.get("http://127.0.0.1:8000/")
        self.assertEqual(response.text, "Hello, World!")