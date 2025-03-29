from scm_policy.gitlab.backend import Gitlab


class BackendManager:
    def __init__(self, config):
        self.config = config

    def handle_backend_type(self, server_url, server_auth_token):
        if self.config.get('type') == "gitlab":
            Gitlab(self.config, server_url, server_auth_token).entrypoint()
        elif self.config.get('type') == "github":
            pass

    def handle_auth(self):
        pass
