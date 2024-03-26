# file: git_ghost/__main__.py

"""__main__ functionality and provides a CLI interface."""

import os
import click
from . import commit, ghost_user, utils

@click.group()
def cli():
    """Git Cloud CLI"""


#@cli.command(name='cloud-sync')
#@click.option('--lab', 'sync_to_gitlab', flag_value=True, help='Sync with GitLab.')
#@click.option('-l', 'sync_to_gitlab', flag_value=True, hidden=True)  # Hidden alias for --lab
#@click.option('--hub', 'sync_to_github', flag_value=True, help='Sync with GitHub.')
#@click.option('-h', 'sync_to_github', flag_value=True, hidden=True)  # Hidden alias for --hub
#def multi_push(sync_to_gitlab, sync_to_github, add, commit):
#    """Sync command."""
#    click.echo('Syncing...')
#    sync_cloud.run_command(os.getcwd(), push_to_github=sync_to_github, push_to_gitlab=sync_to_gitlab)



@click.option('-gm', '--ghost-method', type=click.Choice(['empty','chaos'], case_sensitive=False), default='empty', help='Signature method to use.')
@click.option('-cl', '--config-level', type=click.Choice(['global','local'], case_sensitive=False), required=True, help='Global or Local.')
@click.option('-y', '--no-confirm', flag_value=True, help="No confirm prompts")
@cli.command(name='ghost-user')
def ghost_user_cli(ghost_method,config_level,no_confirm):
    """Ghost global or local user meta data."""

    ghost_method_enum = utils.GhostMethod[ghost_method.upper()]
    if config_level == 'global':
        anon_user("GLOBAL",ghost_method_enum,not no_confirm)
    else:
        ghost_user(os.getcwd(),ghost_method_enum,not no_confirm)

@click.option('-gm', '--ghost-method', type=click.Choice(['empty','chaos'], case_sensitive=False), default='empty', help='Signature method to use.')
@click.option('--message', '-m', 'message', default='', help="Commit message.")
@click.option('--message_prompt', '-mp', 'message_prompt', flag_value=True, help="Prompt for message.")
@click.option('--verbose', '-v', 'verbose_log', flag_value=True, help="Increase verbosity to show detailed logs.")
@click.option('-y', '--no-confirm', flag_value=True, help="No confirm prompts")
@cli.command(name='commit')
def commit_cli(ghost_method:str, message:str, message_prompt:bool, verbose_log:bool, no_confirm:bool):
    """Commit with unique ghosted author meta-data."""
    ghost_method_enum = utils.GhostMethod[ghost_method.upper()]
    commit(os.getcwd(),message,message_prompt,ghost_method_enum,not no_confirm,verbose_log)

if __name__ == '__main__':
    cli()
