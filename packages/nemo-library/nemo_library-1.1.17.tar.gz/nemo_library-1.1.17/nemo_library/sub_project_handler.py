import pandas as pd
import requests
import json

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_symbols import (
    ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES,
    ENDPOINT_URL_PROJECTS_ALL,
)


def getProjectList(config: ConfigHandler):
    """
    Retrieves a list of projects from the server and returns it as a DataFrame.

    Args:
        config: Configuration object that contains necessary connection settings.

    Returns:
        pd.DataFrame: DataFrame containing the list of projects.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)

    response = requests.get(
        config.config_get_nemo_url() + ENDPOINT_URL_PROJECTS_ALL, headers=headers
    )
    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )
    resultjs = json.loads(response.text)
    df = pd.json_normalize(resultjs)
    return df


def getProjectID(config: ConfigHandler, projectname: str):
    """
    Retrieves the project ID for a given project name.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the ID.

    Returns:
        str: The ID of the specified project.

    Raises:
        Exception: If the project name is not found or if multiple projects match the given name.
    """
    df = getProjectList(config)
    crmproject = df[df["displayName"] == projectname]
    if len(crmproject) != 1:
        raise Exception(f"could not identify project name {projectname}")
    project_id = crmproject["id"].to_list()[0]
    return project_id


def getProjectProperty(config: ConfigHandler, projectname: str, propertyname: str):
    """
    Retrieves a specified property for a given project from the server.

    Args:
        config: Configuration object that contains necessary connection settings.
        projectname (str): The name of the project for which to retrieve the property.
        propertyname (str): The name of the property to retrieve.

    Returns:
        str: The value of the specified property for the given project.

    Raises:
        Exception: If the request to the server fails.
    """
    headers = connection_get_headers(config)
    project_id = getProjectID(config, projectname)

    ENDPOINT_URL = (
        config.config_get_nemo_url()
        + ENDPOINT_URL_PERSISTENCE_PROJECT_PROPERTIES.format(
            projectId=project_id, request=propertyname
        )
    )

    response = requests.get(ENDPOINT_URL, headers=headers)

    if response.status_code != 200:
        raise Exception(
            f"request failed. Status: {response.status_code}, error: {response.text}"
        )

    return response.text[1:-1]  # cut off leading and trailing "
