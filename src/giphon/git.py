from logging import Logger
from pathlib import Path

import git

def call_handle(params) -> str:
    """
    Used for the multiprocessing

    Args:
        params: arguments of handle_project function

    Returns:
        str: the repository url just cloned
    """

    return handle_project(*params)

def handle_project(
    repository_path: Path,
    repository_url: str,
    fetch: bool,
    logger: Logger,
) -> str:
    """
    Clone or fetch remotes for a project.

    Args:
        repository_path (Path): the path on which the project should exist
        repository_url (str): the git URL for the repository
        fetch (bool): whether to fetch all remotes if the project already
          exists locally
        logger (Logger): the logger to use to generate logs

    Returns:
        str: the repository url just cloned

    Raises:
        git.exc.GitCommandError: Git error when cloning
    """

    if not repository_path.is_dir():
        while "Trying to clone the repo":
            try:
                repo = git.repo.Repo.clone_from(
                    repository_url, repository_path, no_single_branch=True
                )
                break
            except git.GitCommandError as e:
                if e.status == 128:
                    logger.warning(e, exc_info=True)
                    return ""
                else:
                    raise e

    else:
        if fetch:
            repo = git.repo.Repo(repository_path)
            _fetch_repository(repo)

    return repository_path.__str__()


def _fetch_repository(repository: git.repo.Repo) -> None:
    for remote in repository.remotes:
        remote.fetch()
