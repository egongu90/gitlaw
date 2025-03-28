"""
Main entrypoint scm policy package.
"""

import os

from scm_policy.base.parser import Yamlloader

try:
    SERVER_URL = os.environ['SERVER_URL']
    SERVER_AUTH_TOKEN = os.environ['SERVER_AUTH_TOKEN']
except KeyError as e:
    raise KeyError(f'Environment variable {e} not found') from e
CONFIG_FILE = 'minimum.yml'

def main():
    """Main method."""

    config_data = Yamlloader().read_file(CONFIG_FILE)
    print(SERVER_AUTH_TOKEN)
    print(SERVER_URL)
    print("Setting Instance config")
    for group in config_data.get('organization').get('groups'):
        print(group.get('policy').get('group_protected_branch_settings'))

    # print(config_data['organization']['groups'][2]['name'])

    # Just for testing to read full rendered file
    # import yaml
    # with open('/tmp/dumped.yaml', 'w') as file:
    #     yaml.dump(config_data, file)

if __name__=="__main__":
    main()
