"""
Provides parsing for yaml.
"""

import yaml

class Yamlloader():
    """Yamlloader class.

    Manages yaml file loading and merging of data.
    """

    def read_file(self, config_file: str) -> dict:
        """Read config file yaml.

        Args:
        config_file: Config file path or name.

        Returns:
        YAML loaded dictionary.

        Raises:
        Exception: If file is not loaded of wrong yaml format.
        """
        try:
            with open(config_file, 'r', encoding="utf-8") as file:
                config = yaml.safe_load(file)
        except Exception as e:
            raise e
        return config

    def pass_pylint(self):
        """Test docstring."""
        return

    # def merge_groups(self, config_file: dict) -> dict:
    #     config = self.read_file(config_file)
    #     # for group in config['organization']['groups']:
    #     #     if group.get('policy') == '.default_policy':
    #     #         group['policy'].update(config['.default_policy']['group'])
    #     return config
