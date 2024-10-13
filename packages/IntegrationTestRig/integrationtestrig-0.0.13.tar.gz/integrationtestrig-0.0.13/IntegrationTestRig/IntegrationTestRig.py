import os
import subprocess
import time
import unittest

class IntegrationTestRig(unittest.TestCase):
    seconds_to_wait = 5
    resource_file = None

    @classmethod
    def setUpClass(cls):
        resource_file = cls.find_resource_file(cls.resource_file)
        cls.is_flask_resource(resource_file)
        cls.service_process = subprocess.Popen(["python", resource_file])
        time.sleep(cls.seconds_to_wait)

    @classmethod
    def tearDownClass(cls):
        cls.service_process.terminate()
        cls.service_process.wait()

    @staticmethod
    def find_resource_file(filename):
        for root, _, files in os.walk('.'):
            if filename in files:
                return os.path.join(root, filename)
        raise FileNotFoundError(f"Resource file '{filename}' not found in the project.")

    @staticmethod
    def is_flask_resource(filepath):
        with open(filepath, 'r') as file:
            content = file.read()
            if 'from flask' not in content or 'import Flask' not in content:
                raise ValueError(f"File '{filepath}' is not a valid Flask resource file.")