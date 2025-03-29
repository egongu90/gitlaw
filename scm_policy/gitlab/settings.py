class Settings:
    def __init__(self, gl, config):
        self.gl = gl
        self.config = config

    def manager(self):
        self._set_defaults()
        self.settings = self.get_settings()
                # self.config.get('auto_devops_enabled')
        # print(self.settings.auto_devops_enabled)
        # print(self.auto_devops_enabled)
        self.eval_changes()

    def get_settings(self) -> dict:
        settings = self.gl.settings.get()
        return settings
    
    def _set_defaults(self):
        self.defaults = {}
        self.defaults['auto_devops_enabled'] = self.config.get('auto_devops_enabled', False)
        self.defaults['bulk_import_enabled'] = self.config.get('bulk_import_enabled', False)

    def eval_changes(self):
        for key, value in self.defaults.items():
            if getattr(self.settings, key) != value:
                print(f"Expected value `{key}: {value}` does not match with remote `{getattr(self.settings, key)}`")
                setattr(self.settings, key, value)
            self.settings.save()