"""
Main entrypoint scm policy package.
"""

import os
import urllib3

from gitlaw.base.parser import Yamlloader
from gitlaw.base.backend import BackendManager

# For development only, enforce ssl when finished
urllib3.disable_warnings()

try:
    SERVER_URL = os.environ['SERVER_URL']
    SERVER_AUTH_TOKEN = os.environ['SERVER_AUTH_TOKEN']
except KeyError as e:
    raise KeyError(f'Environment variable {e} not found') from e
CONFIG_FILE = 'examples/example.yml'

def main():
    """Main method."""

    config_data = Yamlloader().read_file(CONFIG_FILE)

    # Just for testing to read full rendered file
    # import yaml
    # with open('/tmp/dumped.yaml', 'w') as file:
    #     yaml.dump(config_data, file)

    BackendManager(config_data.get('organization')).handle_backend_type(SERVER_URL,
                                                                        SERVER_AUTH_TOKEN)

if __name__=="__main__":
    main()
