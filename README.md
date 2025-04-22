# Gitlaw - SCM policy as Code

Gitlaw is a project which aim is to manage SCMs configuration as code.
This means the user can configure the groups and project definition such as merge request rules, default branches, etc within a configuration file, allowing to keep a shared configuration between instances and be able to replicate along different stages of the software supply chain.


## Installation

Install the package provided in github releases.

TBD: Publish to pypi.

```sh
pip install https://github.com/egongu90/gitlaw/releases/download/0.0.1/gitlaw-0.0.1-py3-none-any.whl
```

## Usage

```sh
export GITLAW_URL="https://gitlab.example.com"
export GITLAW_TOKEN="1234"

gitlaw --config config.yml
```

Server url and token can be provided as command arguments.

```sh
gitlaw --config config.yml --url https://gitlab.example.com --token "1234"
```


### Config file

Example configuration file with all default values can be found at [example.yml](./examples/example.yml).

Not all values need to be added to the config file, just the minimal and the paramenters to be changed/verified.

YAML file support anchors, so better re-use everything as possible

```yaml
---
organization:
  groups:
    - name: Example
      description: "Example description"
```

### Examples

#### Global config

```yaml
organization:
  service:
    can_create_group: false
    allow_account_deletion: true
    default_group_visibility: private
  groups:
    - name: Example
      description: "Example description"
```

#### Disable configuration of groups or projects

```yaml
organization:
  configure_service: true
  configure_groups: true  
  auto_create_groups: true
  configure_projects: true
  service:
    can_create_group: false
    allow_account_deletion: true
    default_group_visibility: private
  groups:
    - name: Example
      description: "Example description"

```

#### Group members

```yaml
---
example_members: &example_members
  - name: user1
    access_level: 40
  - name: user2
    access_level: 30

organization:
  groups:
    - name: Example
      description: "Example description"
      members: *example_members
```

#### Group policy

```yaml
---
organization:
  groups:
    - name: Example
      description: "Example description"
      policy:
        visibility: private
        merge_request:
          allow_author_approval: True
```

#### Project policy

```yaml
---
organization:
  groups:
    - name: Example
      description: "Example description"
      projects:
      - name: test1
        policy:
          visibility: "private"
          merge_method: merge
          default_branch: main
          squash_option: default_on
```

#### branch defaults

```yaml
---
branch_defaults: &branch_defaults
  - name: main
    allow_force_push: False
    code_owner_approval_required: False

organization:
  groups:
    - name: Example
      description: "Example description"
      projects:
      - name: test1
        policy:
          branch: *branch_defaults
```

#### Complete example

```yaml
---
default_service_policy: &default_service_policy
  can_create_group: false
  allow_account_deletion: true
  default_group_visibility: private

default_group_policy: &default_group_policy
  visibility: private
  merge_request:
  allow_author_approval: True

branch_defaults: &branch_defaults
  - name: main
    allow_force_push: False
    code_owner_approval_required: False

default_project_policy: &default_project_policy
  visibility: "private"
  merge_method: merge
  default_branch: main
  squash_option: default_on
  branch: *branch_defaults

example_members: &example_members
  - name: user1
    access_level: 40
  - name: user2
    access_level: 30

organization:
  groups:
    - name: Example
      description: "Example description"
      policy: *default_group_policy
      members: *example_members
      projects:
      - name: test1
        policy: *default_project_policy
```

### Command arguments
```sh
$ gitlaw --help
usage: gitlaw [-h] [--url URL] [--token TOKEN] [--config CONFIG] [--scm {gitlab}] [--dry-run] [--render-config] [--render-file RENDER_FILE] [--tls-verify TLS_VERIFY]

GitLaw SCM policy as code.

optional arguments:
  -h, --help            show this help message and exit
  --url URL             Server URL to configure, defaults to environment variable GITLAW_URL.
  --token TOKEN         Server auth token, defaults to environment variable GITLAW_TOKEN.
  --config CONFIG       Configuration file to read values, defaults to config.yml.
  --scm {gitlab}        SCM backend type, defaults to gitlab.
  --dry-run             Not change values, only check for changes.
  --render-config       Only render configuration file YAML.
  --render-file RENDER_FILE
                        Output file to write rendered YAML, defaults to rendered.yml.
  --tls-verify TLS_VERIFY
                        TLS certificate verification, defaults to True
```

## Roadmap

List of expected/wanted features [roadmap.md](roadmap.md)