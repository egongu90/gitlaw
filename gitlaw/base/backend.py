"""Backend manager."""
from gitlaw.gitlab.backend import GitlabBackend


class BackendManager:
    """BackendManager class.

    Manages interactions with backend services APIs.
    """
    def __init__(self, config) -> None:
        """Init class.
        
        Args:
        config: Config data.
        """
        self.config = config

    def handle_backend_type(self, server_url, server_auth_token) -> None:
        """Call inner backend services depending on the config.

        Args:
        server_url: GitLab server URL.
        server_auth_token: Gitlab auth token
        """
        if self.config.get('type') == "gitlab":
            GitlabBackend(self.config, server_url, server_auth_token).entrypoint()
        elif self.config.get('type') == "github":
            pass

    # Just for pylint, add exception if no more methods are created for this class
    def handle_auth(self):
        """handle auth."""
        print("pass")
