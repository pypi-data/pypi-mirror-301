"""
  BYOSnap CLI commands
"""
import base64
from binascii import Error as BinasciiError
import json
import os
import re
import subprocess
import platform as sys_platform
from sys import platform
from typing import Union, List
import requests
from requests.exceptions import RequestException

from rich.progress import Progress, SpinnerColumn, TextColumn
from snapctl.config.constants import SERVER_CALL_TIMEOUT
from snapctl.config.constants import HTTP_ERROR_SERVICE_VERSION_EXISTS, \
    HTTP_ERROR_TAG_NOT_AVAILABLE, HTTP_ERROR_ADD_ON_NOT_ENABLED, SNAPCTL_INPUT_ERROR, \
    SNAPCTL_BYOSNAP_DEPENDENCY_MISSING, SNAPCTL_BYOSNAP_ECR_LOGIN_ERROR, \
    SNAPCTL_BYOSNAP_BUILD_ERROR, SNAPCTL_BYOSNAP_TAG_ERROR, SNAPCTL_BYOSNAP_PUBLISH_IMAGE_ERROR, \
    SNAPCTL_BYOSNAP_PUBLISH_IMAGE_DUPLICATE_TAG_ERROR, \
    SNAPCTL_BYOSNAP_CREATE_DUPLICATE_NAME_ERROR, SNAPCTL_BYOSNAP_CREATE_PERMISSION_ERROR, \
    SNAPCTL_BYOSNAP_CREATE_ERROR, SNAPCTL_BYOSNAP_PUBLISH_VERSION_DUPLICATE_TAG_ERROR, \
    SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR
from snapctl.utils.echo import success, info, warning
from snapctl.utils.helper import get_composite_token, snapctl_error, snapctl_success, \
    check_dockerfile_architecture


class ByoSnap:
    """
      CLI commands exposed for a BYOSnap
    """
    ID_PREFIX = 'byosnap-'
    SUBCOMMANDS = [
        'create', 'publish-image', 'publish-version', 'upload-docs',
    ]
    PLATFORMS = ['linux/arm64', 'linux/amd64']
    LANGUAGES = ['go', 'python', 'ruby', 'c#', 'c++', 'rust', 'java', 'node']
    DEFAULT_BUILD_PLATFORM = 'linux/arm64'
    SID_CHARACTER_LIMIT = 47
    TAG_CHARACTER_LIMIT = 80
    VALID_CPU_MARKS = [100, 250, 500, 750, 1000, 1500, 2000, 3000]
    VALID_MEMORY_MARKS = [0.125, 0.25, 0.5, 1, 2, 3, 4]
    MAX_READINESS_TIMEOUT = 30
    MAX_MIN_REPLICAS = 4

    def __init__(
        self, subcommand: str, base_url: str, api_key: Union[str, None], sid: str, name: str,
        desc: str, platform_type: str, language: str, input_tag: Union[str, None],
        path: Union[str, None], resources_path: Union[str, None], dockerfile: str,
        prefix: str, version: Union[str, None], http_port: Union[int, None],
        byosnap_profile: Union[str, None], skip_build: bool = False,
        readiness_path: Union[str, None] = None, readiness_delay: Union[int, None] = None
    ) -> None:
        self.subcommand: str = subcommand
        self.base_url: str = base_url
        self.api_key: str = api_key
        self.sid: str = sid
        self.name: str = name
        self.desc: str = desc
        self.platform_type: str = platform_type
        self.language: str = language
        if subcommand != 'create':
            self.token: Union[str, None] = get_composite_token(
                base_url, api_key,
                'byosnap', {'service_id': sid}
            )
        else:
            self.token: Union[str, None] = None
        self.token_parts: Union[list, None] = ByoSnap._get_token_values(
            self.token) if self.token is not None else None
        self.input_tag: Union[str, None] = input_tag
        self.path: Union[str, None] = path
        self.resources_path: Union[str, None] = resources_path
        self.dockerfile: str = dockerfile
        self.prefix: str = prefix
        self.version: Union[str, None] = version
        self.http_port: Union[int, None] = http_port
        self.byosnap_profile: Union[str, None] = byosnap_profile
        self.skip_build: bool = skip_build
        self.readiness_path: Union[str, None] = readiness_path
        self.readiness_delay: Union[int, None] = readiness_delay
        # Validate the input
        self.validate_input()

    # Protected methods
    @staticmethod
    def _get_token_values(token: str) -> Union[None, List]:
        """
          Method to break open the token
        """
        try:
            input_token = base64.b64decode(token).decode('ascii')
            parts = input_token.split('|')
            # url|web_app_token|service_id|ecr_repo_url|ecr_repo_username|ecr_repo_token
            # url = self.token_parts[0]
            # web_app_token = self.token_parts[1]
            # service_id = self.token_parts[2]
            # ecr_repo_url = self.token_parts[3]
            # ecr_repo_username = self.token_parts[4]
            # ecr_repo_token = self.token_parts[5]
            # platform = self.token_parts[6]
            if len(parts) >= 3:
                return parts
        except BinasciiError:
            pass
        return None

    def _check_dependencies(self) -> None:
        """
          Check application dependencies
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Checking dependencies...', total=None)
        try:
            # Check dependencies
            result = subprocess.run([
                "docker", "info"
            ], stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not result.returncode:
                return snapctl_success('BYOSnap dependencies verified',
                                       progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOSNAP_DEPENDENCY_MISSING, progress)
        snapctl_error('Docker not running. Please start docker.',
                      SNAPCTL_BYOSNAP_DEPENDENCY_MISSING, progress)

    def _docker_login(self) -> None:
        """
          Docker Login
        """
        ecr_repo_url = self.token_parts[0]
        ecr_repo_username = self.token_parts[1]
        ecr_repo_token = self.token_parts[2]
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Logging into Snapser Image Registry...', total=None)
        try:
            # Login to Snapser Registry
            if platform == 'win32':
                response = subprocess.run([
                    'docker', 'login', '--username', ecr_repo_username,
                    '--password', ecr_repo_token, ecr_repo_url
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            else:
                response = subprocess.run([
                    f'echo "{ecr_repo_token}" | docker login ' +
                    f'--username {ecr_repo_username} --password-stdin {ecr_repo_url}'
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not response.returncode:
                return snapctl_success('BYOSnap ECR login successful',
                                       progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOSNAP_ECR_LOGIN_ERROR, progress)
        snapctl_error('BYOSnap ECR login failure',
                      SNAPCTL_BYOSNAP_ECR_LOGIN_ERROR, progress)

    def _docker_build(self) -> None:
        # Get the data
        # image_tag = f'{self.sid}.{self.input_tag}'
        build_platform = ByoSnap.DEFAULT_BUILD_PLATFORM
        if len(self.token_parts) == 4:
            build_platform = self.token_parts[3]
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Building your snap...', total=None)
        try:
            # Build your snap
            if self.resources_path:
                base_path = self.resources_path
            else:
                base_path = self.path
            docker_file_path = os.path.join(base_path, self.dockerfile)

            # Warning check for architecture specific commands
            info(f'Building on system architecture {sys_platform.machine()}')
            check_response = check_dockerfile_architecture(
                docker_file_path, sys_platform.machine())
            if check_response['error']:
                warning(check_response['message'])
            # Build the image
            if platform == "win32":
                response = subprocess.run([
                    # f"docker build --no-cache -t {tag} {path}"
                    'docker', 'build', '--platform', build_platform, '-t', self.input_tag,
                    '-f', docker_file_path,  self.path
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                response = subprocess.run([
                    # f"docker build --no-cache -t {tag} {path}"
                    "docker build --platform " +
                    f"{build_platform} -t {self.input_tag} " +
                    f"-f {docker_file_path} {self.path}"
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if not response.returncode:
                return snapctl_success('BYOSnap build successful',
                                       progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOSNAP_BUILD_ERROR, progress)
        snapctl_error('BYOSnap build failure',
                      SNAPCTL_BYOSNAP_BUILD_ERROR, progress)

    def _docker_tag(self) -> None:
        # Get the data
        ecr_repo_url = self.token_parts[0]
        image_tag = f'{self.sid}.{self.input_tag}'
        full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Tagging your snap...', total=None)
        try:
            # Tag the repo
            if platform == "win32":
                response = subprocess.run([
                    'docker', 'tag', self.input_tag, full_ecr_repo_url
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            else:
                response = subprocess.run([
                    f"docker tag {self.input_tag} {full_ecr_repo_url}"
                ], shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT, check=False)
            if not response.returncode:
                return snapctl_success('BYOSnap tag successful',
                                       progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOSNAP_TAG_ERROR, progress)
        snapctl_error('BYOSnap tag failure',
                      SNAPCTL_BYOSNAP_TAG_ERROR, progress)

    def _docker_push(self) -> bool:
        """
          Push the Snap image
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(description='Pushing your snap...', total=None)
        try:
            # Push the image
            ecr_repo_url = self.token_parts[0]
            image_tag = f'{self.sid}.{self.input_tag}'
            full_ecr_repo_url = f'{ecr_repo_url}:{image_tag}'
            if platform == "win32":
                response = subprocess.run([
                    'docker', 'push', full_ecr_repo_url
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            else:
                response = subprocess.run([
                    f"docker push {full_ecr_repo_url}"
                ], shell=True, check=False)
                # stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            if not response.returncode:
                return snapctl_success('BYOSnap upload successful',
                                       progress, no_exit=True)
        except subprocess.CalledProcessError:
            snapctl_error('Snapctl Exception',
                          SNAPCTL_BYOSNAP_PUBLISH_IMAGE_ERROR, progress)
        snapctl_error('BYOSnap upload failure. Duplicate image error.',
                      SNAPCTL_BYOSNAP_PUBLISH_IMAGE_DUPLICATE_TAG_ERROR, progress)

    def _validate_byosnap_profile(self) -> None:
        """
          Validate the BYOSnap profile
        """
        if not self.byosnap_profile:
            snapctl_error("Missing BYOSnap profile path", SNAPCTL_INPUT_ERROR)
        if not os.path.isfile(self.byosnap_profile):
            snapctl_error(
                "Unable to find BYOSnap profile " +
                f"JSON at path {self.byosnap_profile}",
                SNAPCTL_INPUT_ERROR
            )
        profile_data = None
        with open(self.byosnap_profile, 'rb') as file:
            try:
                profile_data = json.load(file)
            except json.JSONDecodeError:
                pass
        if not profile_data:
            snapctl_error(
                'Invalid BYOSnap profile JSON. Please check the JSON structure',
                SNAPCTL_INPUT_ERROR
            )
        if 'dev_template' not in profile_data or \
            'stage_template' not in profile_data or \
                'prod_template' not in profile_data:
            snapctl_error(
                'Invalid BYOSnap profile JSON. Please check the JSON structure',
                SNAPCTL_INPUT_ERROR
            )
        for profile in ['dev_template', 'stage_template', 'prod_template']:
            # Currently, not checking for 'min_replicas' not in profile_data[profile]
            if 'cpu' not in profile_data[profile] or \
                'memory' not in profile_data[profile] or \
                    'cmd' not in profile_data[profile] or \
                    'args' not in profile_data[profile] or \
                    'env_params' not in profile_data[profile]:
                snapctl_error(
                    'Invalid BYOSnap profile JSON. Please check the JSON structure',
                    SNAPCTL_INPUT_ERROR
                )
            if profile_data[profile]['cpu'] not in ByoSnap.VALID_CPU_MARKS:
                snapctl_error(
                    'Invalid CPU value in BYOSnap profile. Valid values are' +
                    f'{", ".join(map(str, ByoSnap.VALID_CPU_MARKS))}',
                    SNAPCTL_INPUT_ERROR
                )
            if profile_data[profile]['memory'] not in ByoSnap.VALID_MEMORY_MARKS:
                snapctl_error(
                    'Invalid Memory value in BYOSnap profile. Valid values are ' +
                    f'{", ".join(map(str, ByoSnap.VALID_MEMORY_MARKS))}',
                    SNAPCTL_INPUT_ERROR
                )
            if 'min_replicas' in profile_data[profile] and \
                (not isinstance(profile_data[profile]['min_replicas'], int) or
                    int(profile_data[profile]['min_replicas']) < 0 or
                 int(profile_data[profile]['min_replicas']) > ByoSnap.MAX_MIN_REPLICAS):
                snapctl_error(
                    'Invalid Min Replicas value in BYOSnap profile. ' +
                    'Minimum replicas should be between 0 and ' +
                    f'{ByoSnap.MAX_MIN_REPLICAS}',
                    SNAPCTL_INPUT_ERROR
                )

    def _clean_slate(self) -> None:
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Cleaning cache and initializing...', total=None)
        try:
            # Specific ECR repository URL to check against
            ecr_domain = self.token_parts[0].split('/')[0]
            # Perform the Docker logout
            if platform == "win32":
                logout_response = subprocess.run(['docker', 'logout', ecr_domain],
                                                 shell=True, check=False)
            else:
                logout_response = subprocess.run([
                    f"docker logout {ecr_domain}"
                ], shell=True, check=False)
            if not logout_response.returncode:
                return snapctl_success('Cleanup complete.', progress, no_exit=True)
        except subprocess.CalledProcessError:
            warning('Unable to initialize with a clean slate.')
        finally:
            progress.stop()

    # Public methods

    # Validator
    def validate_input(self) -> None:
        """
          Validator
        """
        # Check API Key and Base URL
        if not self.api_key or self.base_url == '':
            snapctl_error("Missing API Key.", SNAPCTL_INPUT_ERROR)
        # Check subcommand
        if not self.subcommand in ByoSnap.SUBCOMMANDS:
            snapctl_error(
                "Invalid command. Valid commands are " +
                f"{', '.join(ByoSnap.SUBCOMMANDS)}.",
                SNAPCTL_INPUT_ERROR
            )
        # Validate the SID
        if not self.sid.startswith(ByoSnap.ID_PREFIX):
            snapctl_error(
                "Invalid Snap ID. Valid Snap IDs start with " +
                f"{ByoSnap.ID_PREFIX}.",
                SNAPCTL_INPUT_ERROR
            )
        if len(self.sid) > ByoSnap.SID_CHARACTER_LIMIT:
            snapctl_error(
                "Invalid Snap ID. Snap ID should be less than " +
                f"{ByoSnap.SID_CHARACTER_LIMIT} characters",
                SNAPCTL_INPUT_ERROR
            )
        # Validation for subcommands
        if self.subcommand == 'create':
            if self.name == '':
                snapctl_error("Missing name", SNAPCTL_INPUT_ERROR)
            if not self.language:
                snapctl_error("Missing language", SNAPCTL_INPUT_ERROR)
            if self.language not in ByoSnap.LANGUAGES:
                snapctl_error(
                    "Invalid language. Valid languages are " +
                    f"{', '.join(ByoSnap.LANGUAGES)}.",
                    SNAPCTL_INPUT_ERROR
                )
            if self.platform_type not in ByoSnap.PLATFORMS:
                snapctl_error(
                    "Invalid platform. Valid platforms are " +
                    f"{', '.join(ByoSnap.PLATFORMS)}.",
                    SNAPCTL_INPUT_ERROR
                )
        else:
            # Check the token
            if self.token_parts is None:
                snapctl_error('Invalid token. Please reach out to your support team.',
                              SNAPCTL_INPUT_ERROR)
            if self.subcommand in ['publish-image']:
                if not self.input_tag:
                    snapctl_error(
                        "Missing required parameter: tag", SNAPCTL_INPUT_ERROR)
                if len(self.input_tag.split()) > 1 or \
                        len(self.input_tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                    snapctl_error(
                        "Tag should be a single word with maximum of " +
                        f"{ByoSnap.TAG_CHARACTER_LIMIT} characters",
                        SNAPCTL_INPUT_ERROR
                    )
                if not self.skip_build and not self.path:
                    snapctl_error("Missing required parameter: path",
                                  SNAPCTL_INPUT_ERROR)
                # Check path
                if self.resources_path:
                    docker_file_path = \
                        f"{self.resources_path}/{self.dockerfile}"
                else:
                    docker_file_path = f"{self.path}/{self.dockerfile}"
                if not self.skip_build and not os.path.isfile(docker_file_path):
                    snapctl_error(
                        "Unable to find " +
                        f"{self.dockerfile} at path {docker_file_path}",
                        SNAPCTL_INPUT_ERROR)
            # elif self.subcommand == 'push':
            #     if not self.input_tag:
            #         error("Missing required parameter: tag", SNAPCTL_INPUT_ERROR)
            #         raise typer.Exit(code=SNAPCTL_INPUT_ERROR)
            elif self.subcommand == 'upload-docs':
                if self.path is None and self.resources_path is None:
                    snapctl_error(
                        "Missing one of: path or resources-path parameter", SNAPCTL_INPUT_ERROR)
            elif self.subcommand == 'publish-version':
                if not self.input_tag:
                    snapctl_error(
                        "Missing required parameter: tag", SNAPCTL_INPUT_ERROR)
                if len(self.input_tag.split()) > 1 or \
                        len(self.input_tag) > ByoSnap.TAG_CHARACTER_LIMIT:
                    snapctl_error(
                        "Tag should be a single word with maximum of " +
                        f"{ByoSnap.TAG_CHARACTER_LIMIT} characters",
                        SNAPCTL_INPUT_ERROR
                    )
                if not self.prefix or self.prefix == '':
                    snapctl_error("Missing prefix", SNAPCTL_INPUT_ERROR)
                if not self.prefix.startswith('/'):
                    snapctl_error("Prefix should start with a forward slash (/)",
                                  SNAPCTL_INPUT_ERROR)
                if self.prefix.endswith('/'):
                    snapctl_error("Prefix should not end with a forward slash (/)",
                                  SNAPCTL_INPUT_ERROR)
                if not self.version:
                    snapctl_error("Missing version", SNAPCTL_INPUT_ERROR)
                pattern = r'^v\d+\.\d+\.\d+$'
                if not re.match(pattern, self.version):
                    snapctl_error("Version should be in the format vX.X.X",
                                  SNAPCTL_INPUT_ERROR)
                if not self.http_port:
                    snapctl_error("Missing Ingress HTTP Port",
                                  SNAPCTL_INPUT_ERROR)
                if not self.http_port.isdigit():
                    snapctl_error("Ingress HTTP Port should be a number",
                                  SNAPCTL_INPUT_ERROR)
                if self.readiness_path is not None:
                    if self.readiness_path.strip() == '':
                        snapctl_error("Readiness path cannot be empty",
                                      SNAPCTL_INPUT_ERROR)
                    if not self.readiness_path.strip().startswith('/'):
                        snapctl_error("Readiness path has to start with /",
                                      SNAPCTL_INPUT_ERROR)
                if self.readiness_delay is not None:
                    if self.readiness_delay < 0 or \
                            self.readiness_delay > ByoSnap.MAX_READINESS_TIMEOUT:
                        snapctl_error(
                            "Readiness delay should be between 0 " +
                            f"and {ByoSnap.MAX_READINESS_TIMEOUT}", SNAPCTL_INPUT_ERROR)
                # Check byosnap_profile path
                self._validate_byosnap_profile()

    # CRUD methods

    def build(self) -> None:
        """
          Build the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
        """
        self._check_dependencies()
        self._docker_build()

    def push(self) -> bool:
        """
          Tag the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Tag the snap
          4. Push your snap
        """
        self._check_dependencies()
        self._docker_tag()
        self._clean_slate()
        self._docker_login()
        self._docker_push()

    # Upper echelon commands
    def upload_docs(self) -> None:
        '''
          Note this step is optional hence we do not raise a typer.Exit
        '''
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Uploading your BYOSnap Docs...', total=None)
        try:
            if self.resources_path:
                base_dir = self.resources_path
            else:
                base_dir = self.path

            swagger_file = os.path.join(base_dir, 'swagger.json')
            readme_file = os.path.join(base_dir, 'README.md')

            if os.path.isfile(swagger_file):
                # Push the swagger.json
                try:
                    attachment_file = open(swagger_file, "rb")
                    url = (
                        f"{self.base_url}/v1/snapser-api/byosnaps/"
                        f"{self.sid}/docs/{self.input_tag}/openapispec"
                    )
                    test_res = requests.post(
                        url, files={"attachment": attachment_file},
                        headers={'api-key': self.api_key},
                        timeout=SERVER_CALL_TIMEOUT
                    )
                    if test_res.ok:
                        success('Uploaded swagger.json')
                    else:
                        info('Unable to upload your swagger.json')
                except RequestException as e:
                    info(
                        'Exception: Unable to find swagger.json at ' +
                        f'{base_dir} {e}'
                    )
            else:
                info(
                    f'No swagger.json found at {base_dir}' +
                    '. Skipping swagger.json upload'
                )

            # Push the README.md
            if os.path.isfile(readme_file):
                # Push the swagger.json
                try:
                    attachment_file = open(readme_file, "rb")
                    url = (
                        f"{self.base_url}/v1/snapser-api/byosnaps/"
                        f"{self.sid}/docs/{self.input_tag}/markdown"
                    )
                    test_res = requests.post(
                        url, files={"attachment": attachment_file},
                        headers={'api-key': self.api_key},
                        timeout=SERVER_CALL_TIMEOUT
                    )
                    if test_res.ok:
                        success('Uploaded README.md')
                    else:
                        info('Unable to upload your README.md')
                except RequestException as e:
                    info(
                        'Exception: Unable to find README.md at ' +
                        f'{base_dir} {str(e)}'
                    )
            else:
                info(
                    f'No README.md found at {base_dir}. Skipping README.md upload')
        except RequestException as e:
            info(f'Exception: Unable to upload your API Json {str(e)}')
        finally:
            progress.stop()
        # snapctl_success('BYOSnap upload successful', no_exit=no_exit)

    def create(self) -> None:
        """
          Creating a new snap
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(description='Creating your snap...', total=None)
        try:
            payload = {
                "service_id": self.sid,
                "name": self.name,
                "description": self.desc,
                "platform": self.platform_type,
                "language": self.language,
            }
            res = requests.post(
                f"{self.base_url}/v1/snapser-api/byosnaps",
                json=payload, headers={'api-key': self.api_key},
                timeout=SERVER_CALL_TIMEOUT
            )
            if res.ok:
                snapctl_success('BYOSNAP create successful', progress)
            response_json = res.json()
            if "api_error_code" in response_json and "message" in response_json:
                if response_json['api_error_code'] == HTTP_ERROR_SERVICE_VERSION_EXISTS:
                    snapctl_error(
                        f'BYOSnap {self.name} already exists. ' +
                        'Please use a different name',
                        SNAPCTL_BYOSNAP_CREATE_DUPLICATE_NAME_ERROR,
                        progress
                    )
                # elif response_json['api_error_code'] == HTTP_ERROR_TAG_NOT_AVAILABLE:
                #     error('Invalid tag. Please use the correct tag')
                if response_json['api_error_code'] == HTTP_ERROR_ADD_ON_NOT_ENABLED:
                    snapctl_error(
                        'Missing Add-on. Please enable the add-on via the Snapser Web app.',
                        SNAPCTL_BYOSNAP_CREATE_PERMISSION_ERROR, progress
                    )
            snapctl_error(
                f'Server error: {json.dumps(response_json, indent=2)}',
                SNAPCTL_BYOSNAP_CREATE_ERROR, progress)
        except RequestException as e:
            snapctl_error(
                f"Exception: Unable to create your snap {e}",
                SNAPCTL_BYOSNAP_CREATE_ERROR, progress)
        snapctl_error('Failed to create snap',
                      SNAPCTL_BYOSNAP_CREATE_ERROR, progress)

    def publish_image(self) -> None:
        """
          Publish the image
          1. Check Dependencies
          2. Login to Snapser Registry
          3. Build your snap
          4. Tag the repo
          5. Push the image
          6. Upload swagger.json
        """
        self._check_dependencies()
        if not self.skip_build:
            self._docker_build()
        else:
            info('--skip-build set. Skipping the build step.')
        self._docker_tag()
        self._clean_slate()
        self._docker_login()
        self._docker_push()
        if self.path is not None or self.resources_path is not None:
            self.upload_docs()
        snapctl_success('BYOSNAP publish successful')

    def publish_version(self) -> None:
        """
          Publish the version
        """
        progress = Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            transient=True,
        )
        progress.start()
        progress.add_task(
            description='Publishing your snap...', total=None)
        try:
            profile_data = {}
            profile_data['dev_template'] = None
            profile_data['stage_template'] = None
            profile_data['prod_template'] = None
            with open(self.byosnap_profile, 'rb') as file:
                profile_data = json.load(file)
            payload = {
                "version": self.version,
                "image_tag": self.input_tag,
                "base_url": f"{self.prefix}/{self.sid}",
                "http_port": self.http_port,
                "readiness_probe_config": {
                    "path": self.readiness_path,
                    "initial_delay_seconds": self.readiness_delay
                },
                "dev_template": profile_data['dev_template'],
                "stage_template": profile_data['stage_template'],
                "prod_template": profile_data['prod_template']
            }
            res = requests.post(
                f"{self.base_url}/v1/snapser-api/byosnaps/{self.sid}/versions",
                json=payload, headers={'api-key': self.api_key},
                timeout=SERVER_CALL_TIMEOUT
            )
            if res.ok:
                snapctl_success('BYOSNAP publish version successful', progress)
            response_json = res.json()
            if "api_error_code" in response_json:
                if response_json['api_error_code'] == HTTP_ERROR_SERVICE_VERSION_EXISTS:
                    snapctl_error(
                        'Version already exists. Please update your version and try again',
                        SNAPCTL_BYOSNAP_PUBLISH_IMAGE_DUPLICATE_TAG_ERROR,
                        progress
                    )
                if response_json['api_error_code'] == HTTP_ERROR_TAG_NOT_AVAILABLE:
                    snapctl_error('Invalid tag. Please use the correct tag',
                                  SNAPCTL_BYOSNAP_PUBLISH_VERSION_DUPLICATE_TAG_ERROR, progress)
            snapctl_error(f'Server error: {json.dumps(response_json, indent=2)}',
                          SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, progress)
        except RequestException as e:
            snapctl_error(f'Exception: Unable to publish a version for your snap {e}',
                          SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, progress)
        snapctl_error('Failed to publish version',
                      SNAPCTL_BYOSNAP_PUBLISH_VERSION_ERROR, progress)
