### README

## Integration Test Rig

This project provides an `IntegrationTestRig` class to facilitate integration testing of services. The rig sets up and tears down a service process for testing purposes.

### Prerequisites

- Python 3.x
- `requests` library
- `unittest` framework

### Setup

1. **Clone the repository**:
    ```sh
    git clone <repository-url>
    cd <repository-directory>
    ```

2. **Create and activate a virtual environment**:
    ```sh
    python -m venv .venv
    source .venv/bin/activate
    ```

3. **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```

### Usage

1. **Define a test class** that inherits from `IntegrationTestRig` and specify the `resource_file` and optionally `seconds_to_wait`:

    ```python
    import requests
    from src.IntegrationTestRig import IntegrationTestRig

    class TestExample(IntegrationTestRig):
        resource_file = "tests/ExampleService.py"
        # seconds_to_wait is optional, defaults to 5 if not set

        def test_example(self):
            response = requests.get("http://127.0.0.1:8000/")
            self.assertEqual(response.text, "Hello, World!")
    ```

2. **Run the test** using the `unittest` framework:

    ```sh
    python -m unittest tests/test_example.py
    ```

### Example

An example test class `TestExample` is provided in `tests/test_example.py`. This class uses the `IntegrationTestRig` to start a service defined in `tests/ExampleService.py` and tests its response.
