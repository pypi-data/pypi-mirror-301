"""Module for uploading docker images to the ECR"""
# Standard
import argparse
from datetime import datetime, timezone
import subprocess  # nosec
import logging
import json
from pathlib import Path
from typing import Union, Optional
# Installed
import docker
from docker import errors as docker_errors
# Local
from libera_utils.logutil import configure_task_logging
from libera_utils.aws import constants, utils

logger = logging.getLogger(__name__)


def login_to_ecr(account_id, region_name):
    """Login to the AWS ECR using commands
    Parameters
    ----------
    account_id : int
        Users AWS account ID

    region_name : string
        String of the region that the users AWS account is in

    Returns
    -------
    result : CompletedProcess
        subproccess object that holds the details of the completed CLI command
    """
    ecr_path = f"{account_id}.dkr.ecr.{region_name}.amazonaws.com"
    logger.debug(f'ECR path is {ecr_path}')

    # Login to ECR using subprocess
    ecr_login_command = f"aws ecr get-login-password --region {region_name} | docker login --username AWS " \
                        f"--password-stdin {ecr_path}"
    result = subprocess.run(ecr_login_command,  # nosec
                            shell=True,
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            text=True, check=False)
    return result


def build_docker_image(
        context_dir: Union[str, Path],
        image_name: str,
        tag: str = "latest",
        target: Optional[str]=None) -> None:
    """
    Build a Docker image from a specified directory and tag it with a custom name.

    Parameters
    ----------
    context_dir : Union[str, Path]
        The path to the directory containing the Dockerfile and other build context.
    image_name : str
        The name to give the Docker image.
    tag : str, optional
        The tag to apply to the image (default is 'latest').
    target : Optional[str]
        Name of the target to build.

    Raises
    ------
    ValueError
        If the specified directory does not exist or the build fails.
    """
    # Check if the directory exists
    if not context_dir.is_dir():
        raise ValueError(f"Directory {context_dir} does not exist.")

    # Initialize the Docker client
    client = docker.from_env()

    # Build the Docker image
    try:
        _, logs = client.images.build(path=context_dir, target=target, tag=f"{image_name}:{tag}")
        for log in logs:
            if 'stream' in log:
                print(log['stream'].strip())  # Print build output to console
        print(f"Image {image_name}:{tag} built successfully.")
    except docker_errors.BuildError as e:
        logger.error("Failed to build docker image.")
        logger.exception(e)
        raise
    except docker_errors.APIError as e:
        logger.error("Docker API error.")
        logger.exception(e)
        raise


def ecr_upload_cli_func(parsed_args: argparse.Namespace) -> None:
    """CLI handler function for ecr-upload CLI subcommand.

    Parameters
    ----------
    parsed_args : argparse.Namespace
        Namespace of parsed CLI arguments

    Returns
    -------
    None
    """
    now = datetime.now(timezone.utc)
    configure_task_logging(f'ecr_upload_{now}',
                           limit_debug_loggers='libera_utils',
                           console_log_level=logging.DEBUG)
    logger.debug(f"CLI args: {parsed_args}")
    verbose: bool = parsed_args.verbose
    image_name: str = parsed_args.image_name
    image_tag = parsed_args.image_tag
    algorithm_name = parsed_args.algorithm_name
    push_image_to_ecr(image_name, image_tag, algorithm_name, verbose=verbose)


def push_image_to_ecr(image_name: str,
                      image_tag: str,
                      algorithm_name: Union[str, constants.ProcessingStepIdentifier],
                      region_name: str = "us-west-2",
                      verbose: bool = False) -> None:
    """Programmatically upload a docker image for a science algorithm to an ECR. ECR name is determined based
    on the algorithm name.

    Parameters
    ----------
    image_name : str
        Name of the image
    image_tag : str
        Tag of the image (often latest)
    algorithm_name : Union[str, constants.ProcessingStepIdentifier]
        Processing step ID string or object. Used to infer the ECR name.
    region_name : str
        AWS region. Used to infer the ECR name.
    verbose : bool
        Enable debug logging

    Returns
    -------
    None
    """
    docker_client = docker.from_env()
    logger.debug(f'Region set to {region_name}')

    account_id = utils.get_aws_account_number()
    logger.debug(f'Account ID is {account_id}')

    algorithm_identifier = constants.ProcessingStepIdentifier(algorithm_name)
    ecr_name = algorithm_identifier.ecr_name
    logger.debug(f'Algorithm name is {ecr_name}')

    # ECR path
    ecr_path = f"{account_id}.dkr.ecr.{region_name}.amazonaws.com"
    logger.debug(f'ECR path is {ecr_path}')

    # Login to ECR using subprocess
    result = login_to_ecr(account_id=account_id, region_name=region_name)
    if result.returncode == 0:
        logger.info(f"Docker Login successful. STDOUT: {result.stdout}")
    else:
        logger.error(f"STDERR: {result.stderr}")
        raise RuntimeError(f"ECR login command: {result.stderr} failed.")

    # # Tag the latest libera_utils image with the ECR repo name
    docker_client.images.get(f"{image_name}:{image_tag}").tag(f"{ecr_path}/{ecr_name}")
    logger.info("Pushing image to ECR.")
    resp = docker_client.images.push(f"{ecr_path}/{ecr_name}", stream=True, decode=True)
    error_message = []
    for line in resp:
        message = json.loads(json.dumps([line]))[0]
        if verbose:
            logger.debug(message)

        if "error" in message:
            error_message.append(message)

    if error_message:
        logger.error(f"Errors were encountered during image push. Error was: \n{error_message}")
        return
    logger.info("Image pushed to ECR successfully.")
