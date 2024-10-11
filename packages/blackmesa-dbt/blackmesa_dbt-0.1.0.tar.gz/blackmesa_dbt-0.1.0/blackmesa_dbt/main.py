from pathlib import Path

import boto3
import os
import pkg_resources

from prefect_dbt_flow import dbt_flow
from prefect_dbt_flow.dbt import DbtDagOptions, DbtProfile, DbtProject

_PKG_NAME = "blackmesa_dbt"

# Prefect work flow
blackmesa_dbt_flow = dbt_flow(
    project=DbtProject(
        name="blackmesa",
        project_dir=Path(__file__).parent,
        profiles_dir=Path(__file__).parent,
    ),
    profile=DbtProfile(
        target="dev",
    ),
    dag_options=DbtDagOptions(
        run_test_after_model=True,
    ),
)


def _sync_seeds(bucket_name, file_keys, download_dir):
    """
    Sync seed files from an S3 bucket to a local directory.

    :param bucket_name: Name of the S3 bucket
    :param file_keys: List of keys (paths) to the files in the S3 bucket
    :param download_dir: Local directory to save the downloaded files
    """
    # Create an S3 client
    s3 = boto3.client('s3')
    
    # Ensure the download directory exists
    os.makedirs(download_dir, exist_ok=True)

    for file_key in file_keys:
        download_path = os.path.join(download_dir, os.path.basename(file_key))
        try:
            s3.download_file(bucket_name, file_key, download_path)
            print(f"Successfully downloaded {file_key} from bucket {bucket_name} to {download_path}.")
        except Exception as e:
            print(f"Error downloading file {file_key}: {e}")

def _get_package_location(package_name):
    """
    Get the installation location of a package.

    :param package_name: Name of the package
    :return: Installation location of the package
    """
    try:
        package = pkg_resources.get_distribution(package_name)
        return package.location
    except pkg_resources.DistributionNotFound:
        print(f"Package {package_name} is not installed.")
        return None


def sync_seeds(bucket_name):
    """
    Sync seed files from an S3 bucket to the local dbt project directory.
    """

    file_keys = [
        "blackmesa_dbt/seeds/cases.csv",
    ]

    # Get the installation location of the package
    package_location = _get_package_location(_PKG_NAME)
    if package_location is None:
        return

    # Define the local directory to save the downloaded seed files
    download_dir = os.path.join(package_location, "seeds")

    # Sync seed files from S3 to the local directory
    _sync_seeds(bucket_name, file_keys, download_dir)

if __name__ == "__main__":
    blackmesa_dbt_flow()