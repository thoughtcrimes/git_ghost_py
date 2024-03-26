# file: git_ghost/utils.py

"""Utils to help separate scripts for readability and organization."""

import random
import string
import git

import enum
# class syntax
class GhostMethod(enum.Enum):
    EMPTY = 1
    CHAOS = 2

class ConfigLevel(enum.Enum):
    GLOBAL = 1
    LOCAL = 2


def get_remote_by_name(repo:git.Repo,remote_name:str) -> git.Remote:
    """
    Get a remote by name from a repo.

    :param repo: The repo object.
    :param remote_name: The name of the remote to get.
    """
    remote = next((remote for remote in repo.remotes if remote.name == remote_name), None)
    if remote is not None:
        return remote
    return None

def set_remote_url(repo:git.Repo,remote:git.Remote,url:str):
    """
    Set the url of a git remote.

    :param repo: The repo object.
    :param remote_name: The name of the remote to get.
    :param remote_url: The url to add to the remote.
    """
    with repo.config_writer() as cw:
        cw.set_value(f"remote \"{remote.name}\"", "url", url)


def make_random_string(min_length: int = 4,
                       max_length: int = 10,
                       allow_numeric: bool = True,
                       first_must_be_alpha: bool = True
                       ) -> str:
    """
    Generates a random alpha_numeric string.

    :param min_length: Minimum length of the string.
    :param max_length: Maximum length of the string.
    :param allow_numeric: Can the string have numeric characters.
    :param first_must_be_alpha: Does the first character have to be alpha.
    """
    length = random.randint(min_length, max_length)

    if first_must_be_alpha:
        # Ensure the first character is alphabetic
        characters = string.ascii_lowercase
    else:
        # The first character can be anything based on allow_numeric
        if allow_numeric:
            characters = string.ascii_lowercase + string.digits
        else:
            characters = string.ascii_lowercase

    # Generate the first character
    first_char = random.choice(characters)

    # Choose the character set for the rest of the string based on allow_numeric
    if allow_numeric:
        rest_characters = string.digits
    else:
        rest_characters = string.ascii_lowercase

    # Generate the rest of the string
    rest_of_string = ''.join(random.choice(rest_characters) for i in range(length - 1))

    return first_char + rest_of_string

def make_random_email(
        min_name: int=3,
        max_name: int=10,
        min_domain:int = 3,
        max_domain: int = 10,
        allow_numeric: bool = True,
        first_must_be_alpha: bool = True
        ) -> str:
    """
    Generates random alpha_numeric resembling an email address.

    :param min_name: Minimum length of the name portion.
    :param max_name: Maximum length of the name portion.
    :param min_domain: Minimum length of the domain portion.
    :param max_domain: Maximum length of the domain portion.
    :param allow_numeric: Can the string have numeric characters.
    :param first_must_be_alpha: Does the first character have to be alpha.
    """
    name = make_random_string(min_name, max_name, allow_numeric, first_must_be_alpha)
    domain = make_random_string(min_domain, max_domain, allow_numeric, first_must_be_alpha)
    return f"{name}@{domain}.com"
