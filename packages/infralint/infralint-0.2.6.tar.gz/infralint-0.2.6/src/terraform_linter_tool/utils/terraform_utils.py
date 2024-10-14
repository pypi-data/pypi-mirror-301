import logging
import os

logger = logging.getLogger(__name__)


def validate_terraform_directory(directory_path: str) -> bool:
    """
    Check if the given directory contains a valid Terraform configuration by checking for a 'main.tf' file.
    
    :param directory_path: Path to the directory to check.
    :return: True if the directory contains a valid Terraform file, False otherwise.
    """
    main_tf_path = os.path.join(directory_path, 'main.tf')

    # Check if main.tf exists
    if os.path.exists(main_tf_path):
        logger.info(f"'main.tf' found in {directory_path}")
        return True
    else:
        logger.error(f"No 'main.tf' found in {directory_path}. Invalid Terraform directory.")
        return False