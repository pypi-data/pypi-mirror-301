from setuptools import setup, find_packages

setup(
    name="IntegrationTestRig",
    version="0.0.4",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            # Add any command-line scripts here
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)