"""
     Initalize the dependencies
"""

from utils.Azlogger import AzLogger
from utils.gitfunctions import (
    acquire_token_user_id_password,
    commit_all_items_to_git,
    get_git_status,
    update_workspace_from_git,
)
