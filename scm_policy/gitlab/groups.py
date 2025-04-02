"""Manages configuration at /groups gitlab API."""
from gitlab.exceptions import GitlabGetError

class Groups:
    """Groups class."""
    def __init__(self, gl, config) -> None:
        """Init method.

        Args:
        gl: Object with gitlab auth
        config: Groups config data
        """
        self.gl = gl
        if config is not None:
            self.config = config
        else:
            self.config = {}

    def manager(self, auto_create_groups=True) -> None:
        """Orchestrates the other class methods.

        Args:
        auto_create_groups: Boolean defaults to True
        """
        user_group = self._set_defaults(self.config.get('name', None),
                                        self.config.get('description', ""),
                                        self.config.get('policy', None))
        server_object = self.get_groups(auto_create_groups)
        self.eval_changes(user_group, server_object)
        print(f"Configuring members of group {self.config.get('name', None)}...")
        self.configure_members(members=self.config.get('members', None), server_obj=server_object)

    def get_groups(self, auto_create_groups) -> dict:
        """Query config data from the API.

        Args:
        auto_create_groups: Boolean defaults to True

        Returns: dict
        """
        try:
            group = self.gl.groups.get(self.config.get('name'))
        except GitlabGetError as exc:
            if auto_create_groups:
                group = self.gl.groups.create({'name': self.config.get('name'),
                                               'path': self.config.get('name')})
            else:
                raise GitlabGetError(f"Group {self.config.get('name')} does not exists "
                                f"and auto_create_groups is disabled") from exc
        return group

    def _set_defaults(self, name, description, policy):
        """Set default values if not defined in the yaml config file.
        
        Args:
        name: Group name
        description: Group description
        policy: Group policy config data
        """
        defaults = {}
        defaults['name'] = name
        defaults['description'] = description
        defaults['visibility'] = policy.get('visibility', "private")
        defaults['auto_devops_enabled'] = policy.get('auto_devops_enabled', False)
        defaults['default_branch'] = policy.get('default_branch', "main")
        defaults['enabled_git_access_protocol'] = self.config.get('enabled_git_access_protocol', None)

        defaults['lfs_enabled'] = policy.get('lfs_enabled', True)
        defaults['project_creation_level'] = policy.get('project_creation_level', "maintainer")
        defaults['subgroup_creation_level'] = policy.get('subgroup_creation_level', "maintainer")
        defaults['wiki_access_level'] = policy.get('wiki_access_level', "private")
        defaults['request_access_enabled'] = policy.get('request_access_enabled', True)
        defaults['require_two_factor_authentication'] = policy.get('require_two_factor_authentication', False)
        defaults['default_branch_protection_defaults'] = policy.get(
            'default_branch_protection_defaults', {'allowed_to_push': [{'access_level': 40}], 
                                                   'allow_force_push': False, 
                                                   'allowed_to_merge': [{'access_level': 40}], 
                                                   'developer_can_initial_push': False})

        return defaults

    def eval_changes(self, user_group, server_obj):
        """Checks for changes on group api.

        Evaluate if the config file data provided match with data in GitLab group API,
        if does not match, set value with the user data and store changes in the API"""
        for key, value in user_group.items():
            try:
                # Some user provided data might me None and continuing the loop will fail.
                if value is not None and getattr(server_obj, key) != value:
                    print(f"Expected value `{key}: {value}` does not match with remote "
                          f"`{getattr(server_obj, key)}`")
                    setattr(server_obj, key, value)
                server_obj.save()
            except AttributeError:
                # When some attribute is only present in licensed servers, the attribute
                # does not exists in the API and raises this exception.
                pass

    def configure_members(self, members, server_obj):
        """Add or update members of a group.

        """
        try:
            for member in members:
                existing_user = self.gl.users.list(username=member.get('name'))[0]
                user_id = existing_user.id
                try:
                    group_member = server_obj.members.get(user_id)
                    if member.get('access_level') != group_member.access_level:
                        print(f"Expected access_level for member `{member.get('name')}: {member.get('access_level')}` "
                          f"does not match with remote `{group_member.access_level}`")
                        group_member.access_level = member.get('access_level')
                        group_member.save()
                except GitlabGetError:
                    print(f"Creating group member {member.get('name')}")
                    server_obj.members.create({'user_id': user_id,
                                            'access_level': member.get('access_level')})
        except IndexError as exc:
            raise IndexError(f"User {member.get('name')} does not exists") from exc
