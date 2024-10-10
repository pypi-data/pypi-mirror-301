"""
    Generate CLI commands
"""
import base64
from binascii import Error as BinasciiError
import json
import os
from typing import Union, List
from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SNAPCTL_INPUT_ERROR, \
    SNAPCTL_GENERATE_GENERIC_ERROR, SNAPCTL_GENERATE_PROFILE_ERROR, \
    SNAPCTL_GENERATE_CREDENTIALS_ERROR
from snapctl.config.hashes import BYOSNAP_TEMPLATE
from snapctl.utils.helper import get_composite_token, snapctl_error, snapctl_success


class Generate:
    """
        Generate CLI commands
    """
    SUBCOMMANDS = ['byosnap-profile', 'profile', 'credentials']
    DEPRECATED_SOON_SUBCOMMANDS = ['byosnap-profile']
    BYOSNAP_PROFILE_FN = 'snapser-byosnap-profile.json'
    ECR_TOKEN_FN = 'snapser-ecr-credentials.json'
    CATEGORIES = {
        'profile': ['byosnap'],
        'credentials': ['ecr']
    }

    def __init__(
        self, subcommand: str, base_url: str, api_key: Union[str, None],
        category: Union[str, None],
        out_path: Union[str, None]
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.category: Union[str, None] = category
        self.out_path: Union[str, None] = out_path
        # Validate input
        self.validate_input()

    # Private methods
    @staticmethod
    def _get_token_values(token: str) -> Union[None, List]:
        """
            Get the token values
        """
        try:
            input_token = base64.b64decode(token).decode('ascii')
            token_parts = input_token.split('|')
            # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
            if len(token_parts) >= 3:
                return token_parts
        except BinasciiError:
            pass
        return None
    # Validator

    def validate_input(self) -> None:
        """
          Validator
        """
        if self.subcommand not in Generate.SUBCOMMANDS:
            snapctl_error(
                f"Invalid command {self.subcommand}. Valid command are " +
                f"{Generate.SUBCOMMANDS}",
                SNAPCTL_INPUT_ERROR
            )
        # Check path
        if self.subcommand == 'profile':
            if self.category not in Generate.CATEGORIES['profile']:
                snapctl_error(
                    f"Invalid category {self.category}. Valid category are " +
                    f"{Generate.CATEGORIES['profile']}",
                    SNAPCTL_INPUT_ERROR
                )
            if not self.out_path:
                snapctl_error(
                    "Path is required for profile generation",
                    SNAPCTL_INPUT_ERROR
                )
        elif self.subcommand == 'credentials':
            if self.category not in Generate.CATEGORIES['credentials']:
                snapctl_error(
                    f"Invalid category {self.category}. Valid category are " +
                    f"{Generate.CATEGORIES['credentials']}",
                    SNAPCTL_INPUT_ERROR
                )
            if not self.out_path:
                snapctl_error(
                    "Path is required for token generation",
                    SNAPCTL_INPUT_ERROR
                )
        # Now confirm that out-path is valid
        if self.out_path and not os.path.isdir(self.out_path):
            snapctl_error(
                f"Invalid path {self.out_path}. Wont be able to " +
                "store the output file",
                SNAPCTL_INPUT_ERROR
            )

    def byosnap_profile(self) -> None:
        """
            Generate snapser-byosnap-profile.json
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Generating BYOSnap profile...', total=None)
        try:
            if self.out_path is not None:
                file_save_path = os.path.join(
                    self.out_path, Generate.BYOSNAP_PROFILE_FN)
            else:
                file_save_path = os.path.join(
                    os.getcwd(), Generate.BYOSNAP_PROFILE_FN)
            file_written = False
            with open(file_save_path, "w") as file:
                json.dump(BYOSNAP_TEMPLATE, file, indent=4)
                file_written = True
            if file_written:
                snapctl_success(
                    "BYOSNAP Profile generation successful. " +
                    f"{Generate.BYOSNAP_PROFILE_FN} saved at {file_save_path}",
                    progress
                )
        except (IOError, OSError) as file_error:
            snapctl_error(f"File error: {file_error}",
                          SNAPCTL_GENERATE_PROFILE_ERROR, progress)
        except json.JSONDecodeError as json_error:
            snapctl_error(f"JSON error: {json_error}",
                          SNAPCTL_GENERATE_PROFILE_ERROR, progress)
        snapctl_error(
            "Failed to generate BYOSNAP Profile",
            SNAPCTL_GENERATE_PROFILE_ERROR,
            progress
        )

    def profile(self) -> None:
        """
            Generate profile
        """
        if self.category == 'byosnap':
            self.byosnap_profile()

    def ecr_credentials(self) -> None:
        """
            Generate credentials
        """

        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Generating ECR credentials...', total=None)
        try:
            composite_token: Union[str, None] = get_composite_token(
                self.base_url, self.api_key, 'byogs', {'service_id': 'byogs'}
            )
            token_parts = Generate._get_token_values(composite_token)
            # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
            if token_parts is None or len(token_parts) != 4:
                snapctl_error(
                    "Unable to retrieve token.",
                    SNAPCTL_GENERATE_GENERIC_ERROR,
                    progress
                )
            token_details = {
                'ecr_repo_url': token_parts[0],
                'ecr_repo_username': token_parts[1],
                'ecr_repo_token': token_parts[2],
                'ecr_repo_platform': token_parts[3]
            }
            if self.out_path is not None:
                file_save_path = os.path.join(
                    self.out_path, Generate.ECR_TOKEN_FN)
            else:
                file_save_path = os.path.join(
                    os.getcwd(), Generate.ECR_TOKEN_FN)
            file_written = False
            with open(file_save_path, "w") as file:
                json.dump(token_details, file, indent=4)
                file_written = True
            if file_written:
                snapctl_success(
                    "ECR Token generation successful. " +
                    f"{Generate.ECR_TOKEN_FN} saved at {file_save_path}",
                    progress
                )
        except (IOError, OSError) as file_error:
            snapctl_error(f"File error: {file_error}",
                          SNAPCTL_GENERATE_CREDENTIALS_ERROR, progress)
        except json.JSONDecodeError as json_error:
            snapctl_error(f"JSON error: {json_error}",
                          SNAPCTL_GENERATE_CREDENTIALS_ERROR, progress)
        snapctl_error(
            "Failed to generate Token",
            SNAPCTL_GENERATE_CREDENTIALS_ERROR,
            progress
        )

    def credentials(self):
        """
            Generate credentials
        """
        if self.category == 'ecr':
            self.ecr_credentials()
