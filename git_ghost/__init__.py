# file: git_ghost/__init__.py

"""Package for git_ghost."""

import sys
import subprocess
import logging
import git
from . import utils

logging.basicConfig(format='%(levelname)s | %(message)s', level=logging.INFO)

logger = logging.getLogger(__name__)

def make_user_based_on_ghost_method(ghost_method:utils.GhostMethod):
    """
    Creates ghost credentials.

    :param ghost_method: GhostMethod - GhostMethod to use.

    :returns: ghosted username, ghosted useremail
    """
    user_name = ""
    user_email = ""

    if ghost_method == utils.GhostMethod.CHAOS:
        user_name = utils.make_random_string(10)
        user_email = utils.make_random_email()

    return user_name,user_email


def ghost_user(
        scope_or_path:str,
        ghost_method:utils.GhostMethod=utils.GhostMethod.EMPTY,
        confirm_prompt:bool = False
        ):
    """
    Assign ghost credentials to a global or local user.

    :param scope_or_path: str - GLOBAL or a directory with a .git repo in it.
    :param ghost_method: GhostMethod - GhostMethod to use.
    :param confirm_prompt: bool - should show configm prompt.
    """

    user_name, user_email = make_user_based_on_ghost_method(ghost_method)

    is_global = False
    if scope_or_path == "GLOBAL":
        is_global = True

    print("\nSUMMARY-------------------")
    logger.info("config_lvl:   %s", "GLOBAL" if is_global else "LOCAL")
    if not is_global:
        logger.info("path:         %s", scope_or_path)
    logger.info("user_name:    %s", user_name)
    logger.info("user_email:   %s\n", user_email)

    if confirm_prompt:
        accepted = input("\nType Y to proceed: ")
        if accepted not in ('Y', 'y', 'Yes', 'yes',"YES"):
            logger.warning("Push canceled by user input.")
            sys.exit(1)


    if is_global:
        subprocess.run(['git', 'config', '--global', 'user.name', user_name], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', user_email], check=True)
    else:
        repo = git.Repo(scope_or_path)
        config_writer = repo.config_writer(config_level='repository')
        config_writer.set_value("user", "name", user_name)
        config_writer.set_value("user", "email", user_email)
        config_writer.release()


    logger.info("Success! GIT global config has been updated with anon user meta data.")




def commit(
        repo_dir:str,
        commit_message:str = "",
        message_prompt:bool = False,
        ghost_method:utils.GhostMethod=utils.GhostMethod.EMPTY,
        confirm_prompt:bool = False,
        show_diffs:bool=True
        ):

    """
    Assign ghost credentials to a global or local user.

    :param repo_dir: str - Directory with a .git repo in it.
    :param commit_message: str - The commit message to use.
    :param message_prompt: bool - Prompt for a commit message.
    :param ghost_method: GhostMethod - GhostMethod to use.
    :param confirm_prompt: bool - should show configm prompt.
    :param show_diffs: bool - print a list of the diffs being commited.
    """

    logger.info("****** Starting git-ghost anon-commit******\n")
    print(repo_dir)
    repo = git.Repo(repo_dir)

    diffs = repo.index.diff("HEAD")
    if not diffs:
        logger.info("No files were changed since last commit. Exiting...")
        sys.exit(0)

    if show_diffs:
        for diff in diffs:
            logger.info(diff)

    if message_prompt:
        print("\n")
        commit_message = input('Enter commit message: ')

    user_name, user_email = make_user_based_on_ghost_method(ghost_method)

    print("\nSUMMARY-------------------")
    print(f"message:    {commit_message}")
    print(f"user_name:  {user_name}")
    print(f"user_email: {user_email}\n")

    if confirm_prompt:
        # Print confirmation settings
        print("Commit Settings:\n")

        accepted = input("Type Y to proceed: ")
        if accepted.lower() not in ['y', 'yes']:
            logger.warning("Commit canceled by user input.")
            return

    actor = git.Actor(user_name, user_email)
    author = actor
    committer = actor

    repo.index.commit(commit_message, author=author, committer=committer)
    logger.info("Commit complete")
