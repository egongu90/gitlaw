"""Module to orchestrate gitlab interactions."""
import gitlab

from scm_policy.gitlab.settings import Settings

class GitlabBackend:
    """Gitlab class.

    Manages interactions with GitLab APIs.
    """
    def __init__(self, config, server_url, server_auth_token) -> None:
        """Init class.
        
        Args:
        config: Config data.
        server_url: GitLab server URL.
        server_auth_token: Gitlab auth token

        Returns: None
        """
        self.config = config
        self.gl = self.handle_auth(server_url, server_auth_token)

    def entrypoint(self) -> None:
        """Call gitlab methods."""
        Settings(self.gl, self.config.get('service')).manager()

    def handle_auth(self, server_url, server_auth_token) -> object:
        """Init gitlab object with auth.

        Args:
        server_url: GitLab server URL.
        server_auth_token: Gitlab auth token
        ssl_verify: Verify SSL connections, defaults to False
        """
        gl = gitlab.Gitlab(url=server_url, private_token=server_auth_token, ssl_verify=False)
        return gl
