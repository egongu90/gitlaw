import gitlab

from scm_policy.gitlab.settings import Settings

class Gitlab:
    def __init__(self, config, server_url, server_auth_token):
        self.config = config
        self.gl = self.handle_auth(server_url, server_auth_token)

    def entrypoint(self):
        Settings(self.gl, self.config.get('service')).manager()

    def handle_auth(self, server_url, server_auth_token):
        gl = gitlab.Gitlab(url=server_url, private_token=server_auth_token, ssl_verify=False)
        return gl
