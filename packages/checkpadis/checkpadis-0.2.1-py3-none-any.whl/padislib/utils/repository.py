import subprocess


def get_repo_info():
    try:
        remote_url = (
            subprocess.check_output(
                ["git", "config", "--get", "remote.origin.url"]
            )
            .strip()
            .decode("utf-8")
        )

        if remote_url.endswith(".git"):
            remote_url = remote_url[:-4]

        parts = remote_url.split("/")
        if len(parts) >= 2:
            organization = parts[-2]
            repo_name = parts[-1]
        else:
            raise ValueError(
                "Cannot parse organization and repository name from remote URL"
            )

        return remote_url, organization, repo_name

    except subprocess.CalledProcessError as e:
        raise Exception(f"Error trying to get remote URL: {e}")
    except ValueError as e:
        raise Exception(e)
