"""
Main entrypoint scm policy package.
"""

import os
import sys
from argparse import ArgumentParser

import urllib3
import yaml

from gitlaw.base.parser import Yamlloader
from gitlaw.base.backend import BackendManager


parser = ArgumentParser(description="GitLaw SCM policy as code.")

parser.add_argument("--url", default=os.environ.get('GITLAW_URL'),
                    help="Server URL to configure, defaults to environment variable GITLAW_URL.")
parser.add_argument("--token", default=os.environ.get('GITLAW_TOKEN'),
                    help="Server auth token, defaults to environment variable GITLAW_TOKEN.")
parser.add_argument("--config", default="config.yml",
                    help="Configuration file to read values, defaults to config.yml.")
parser.add_argument("--scm", default="gitlab", choices=["gitlab"],
                    help="SCM backend type, defaults to gitlab.")
parser.add_argument("--dry-run", action="store_true",
                    help="Not change values, only check for changes.")
parser.add_argument("--render-config", action="store_true",
                    help="Only render configuration file YAML.")
parser.add_argument("--render-file", default="rendered.yml",
                    help="Output file to write rendered YAML, defaults to rendered.yml.")
parser.add_argument("--tls-verify", default=True, type=lambda x: (str(x).lower() in ['true','1', 'yes']),
                    help="TLS certificate verification, defaults to True")


args = parser.parse_args()
if not (args.url and args.token):
    sys.exit(parser.print_usage())

if not args.tls_verify:
    urllib3.disable_warnings()


def main():
    """Main method."""

    config_data = Yamlloader().read_file(args.config)

    if args.render_config:
        with open(args.render_file, encoding="utf8", mode='w') as file:
            yaml.dump(config_data, file)
        sys.exit(0)

    BackendManager(config_data.get('organization')).handle_backend_type(args.url,
                                                                        args.token,
                                                                        args.scm,
                                                                        args.tls_verify,
                                                                        args.dry_run)

if __name__=="__main__":
    main()
