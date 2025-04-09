"""Backend manager."""
from gitlaw.gitlab_base.backend import GitlabBackend


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

    def handle_backend_type(self, server_url, server_auth_token, scm, tls_verify, dry_run) -> None:
        """Call inner backend services depending on the config.

        Args:
        server_url: GitLab server URL.
        server_auth_token: Gitlab auth token
        """
        if scm == "gitlab":
            GitlabBackend(self.config, server_url, server_auth_token, tls_verify).entrypoint(dry_run)
        elif scm == "github":
            raise NotImplementedError("Github not implemented yet.")

    # Just for pylint, add exception if no more methods are created for this class
    def handle_auth(self):
        """handle auth."""
        print("pass")
