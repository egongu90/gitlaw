"""Manages configuration at application/settings gitlab API."""

class Settings:
    """Settings class."""
    def __init__(self, gl, config) -> None:
        """Init method.

        Args:
        gl: Object with gitlab auth
        config: Service Settings config data
        """
        self.gl = gl
        if config is not None:
            self.config = config
        else:
            self.config = {}

    def manager(self, dry_run) -> None:
        """Orchestrates the other class methods."""
        user_settings = self._set_defaults()
        server_object = self.get_settings()
        self.eval_changes(user_settings, server_object, dry_run)

    def get_settings(self) -> dict:
        """Query config data from the API.
        
        Returns: dict
        """
        settings = self.gl.settings.get()
        return settings

    def _set_defaults(self):
        """Set default values if not defined in the yaml config file."""
        defaults = {}
        defaults['auto_devops_enabled'] = self.config.get('auto_devops_enabled', False)
        defaults['bulk_import_enabled'] = self.config.get('bulk_import_enabled', False)
        defaults['can_create_group'] = self.config.get('can_create_group', False)
        defaults['updating_name_disabled_for_users'] = self.config.get('updating_name_disabled_for_users', False)
        defaults['allow_account_deletion'] = self.config.get('allow_account_deletion', True)
        defaults['default_artifacts_expire_in'] = self.config.get('default_artifacts_expire_in', "30 days")
        defaults['default_branch_name'] = self.config.get('default_branch_name', "main")
        defaults['default_group_visibility'] = self.config.get('default_group_visibility', "private")
        defaults['default_project_visibility'] = self.config.get('default_project_visibility', "private")
        defaults['default_snippet_visibility'] = self.config.get('default_snippet_visibility', "private")
        defaults['restricted_visibility_levels'] = self.config.get('restricted_visibility_levels', None)
        defaults['default_projects_limit'] = self.config.get('default_projects_limit', 100000)
        defaults['default_project_deletion_protection'] = self.config.get('default_project_deletion_protection',
                                                                               False)
        defaults['disable_personal_access_tokens'] = self.config.get('disable_personal_access_tokens', False)
        defaults['enabled_git_access_protocol'] = self.config.get('enabled_git_access_protocol', None)
        defaults['enforce_terms'] = self.config.get('enforce_terms', False)
        defaults['terms'] = self.config.get('terms', None)
        defaults['group_owners_can_manage_default_branch_protection'] = \
            self.config.get('group_owners_can_manage_default_branch_protection', True)
        defaults['max_artifacts_size'] = self.config.get('max_artifacts_size', 100)
        defaults['password_authentication_enabled_for_git'] = \
            self.config.get('password_authentication_enabled_for_git', True)
        defaults['password_authentication_enabled_for_web'] = \
            self.config.get('password_authentication_enabled_for_web', True)
        defaults['prevent_merge_requests_author_approval'] = \
            self.config.get('prevent_merge_requests_author_approval', True)
        defaults['prevent_merge_requests_committers_approval'] = \
            self.config.get('prevent_merge_requests_committers_approval', True)
        defaults['signup_enabled'] = self.config.get('signup_enabled', True)
        defaults['import_sources'] = self.config.get('import_sources',
                                                          ['github',
                                                           'bitbucket',
                                                           'bitbucket_server',
                                                           'git',
                                                           'gitlab_project',
                                                           'gitea',
                                                           'manifest'])
        defaults['default_branch_protection_defaults'] = self.config.get(
            'default_branch_protection_defaults', {'allowed_to_push': [{'access_level': 40}], 
                                                   'allow_force_push': False, 
                                                   'allowed_to_merge': [{'access_level': 40}], 
                                                   'developer_can_initial_push': False})
        return defaults

    def eval_changes(self, user_settings, server_obj, dry_run):
        """Checks for changes.
        
        Evaluate if the config file data provided match with data in GitLab API,
        if does not match, set value with the user data and store changes in the API"""
        for key, value in user_settings.items():
            try:
                # Some user provided data might me None and continuing the loop will fail.
                if value is not None and getattr(server_obj, key) != value:
                    print(f"Expected value `{key}: {value}` does not match with remote "
                          f"`{getattr(server_obj, key)}`")
                    setattr(server_obj, key, value)
                if not dry_run:
                    server_obj.save()
            except AttributeError:
                # When some attribute is only present in licensed servers, the attribute
                # does not exists in the API and raises this exception.
                pass
