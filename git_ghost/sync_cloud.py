# file: git_ghost/sync_cloud.py

"""Runs the sync_cloud command to mangle process user credentials and upload to clouds."""

import sys
import logging
import git
from . import utils

logger = logging.getLogger(__name__)

def run_command(path:str, push_to_github=False, push_to_gitlab=False):
    """
    Synchronize to the git as an obfuscated identity.

    :param path: Path of the directory to git.
    :param push_to_github: Should the script push to github cloud.
    :param push_to_gitlab: Should the script push to gitlab cloud.
    """
    repo = git.Repo(path)

    if 'origin' not in repo.remotes:
        logger.error("The repository does not have an 'origin' remote. Exiting...")
        sys.exit(1)

    random_username = utils.make_random_string(10)
    random_email = utils.make_random_email()

    repo.config_writer().set_value("user", "name", random_username).release()
    repo.config_writer().set_value("user", "email", random_email).release()

    added_remotes = []

    #Origin mode means no cloud provider is given so the origin is used.
    origin_mode = not push_to_gitlab and not push_to_github
    
    if origin_mode:     
        added_remotes.append(repo.remotes.origin)
    else:
        
        url = repo.remotes.origin.ur

        if "/github.com/" not in url and "/gitlab.com/" not in url:
            logger.error("Origin url is not a supported git cloudhost. Exiting...")
            sys.exit(1)
        url = url.replace("/github.com/","{DOMAIN}").replace("/gitlab.com/","{DOMAIN}")

        remote_name_and_urls = []


        if push_to_github:
            domain = url.replace("{DOMAIN}","/github.com/")
            remote_name_and_urls.append({"name":"ghosted_github", "url":domain})
        if push_to_gitlab:
            domain = url.replace("{DOMAIN}","/gitlab.com/")
            remote_name_and_urls.append({"name":"ghosted_gitlab", "url":domain})

        if len(remote_name_and_urls)==0:
            logger.error("No cloudhosts are selected...")
            sys.exit(1)

        for pair in remote_name_and_urls:
            remote = utils.get_remote_by_name(repo, pair['name'])
            if remote is None:
                remote = repo.create_remote(pair['name'], pair['url'])
            else:
                logger.warning("Remote already exists: %s", remote.name)
                utils.set_remote_url(repo,remote, pair['url'])
            added_remotes.append(remote)


    print("\n******* CONFIRM SETTINGS *******")
    print("Cloud Push Settings:\n")
    print("user_name:   %s" % repo.config_reader().get_value("user", "name", default="Not Set"))
    print("user_email:  %s" % repo.config_reader().get_value("user", "email", default="Not Set"))
    print("\n")

    for remote in added_remotes:
        print(f"{remote.name} -> {remote.url}")

    accepted = input("\nType Y to proceed: ")
    if accepted not in ('Y', 'y', 'Yes', 'yes',"YES"):
        logger.warning("Push canceled by user input.")
        sys.exit(1)

    for remote in added_remotes:
        logger.info("Pushing changes to %s...", remote.name)
        remote.push(refspec="main:main", set_upstream=True)
        if not origin_mode:
            repo.delete_remote(remote)
            logger.info("Deleted remote: %s", remote.name)
        