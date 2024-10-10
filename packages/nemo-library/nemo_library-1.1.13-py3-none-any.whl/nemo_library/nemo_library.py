import json


import pandas as pd
import requests

import re

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_connection_handler import connection_get_headers
from nemo_library.sub_file_upload_handler import ReUploadFileIngestion
from nemo_library.sub_hubspot_handler import CRM_Activities_handler
from nemo_library.sub_project_handler import (
    getProjectID,
    getProjectList,
    getProjectProperty,
)
from nemo_library.sub_infozoom_handler import synchMetadataWithFocus, exportMetadata

from nemo_library.sub_report_handler import LoadReport
from nemo_library.sub_symbols import (
    ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
    ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS,
    RESERVED_KEYWORDS,
)


class NemoLibrary:

    def __init__(
        self,
        nemo_url=None,
        tenant=None,
        userid=None,
        password=None,
        environment=None,
        hubspot_api_token=None,
        config_file="config.ini",
    ):

        self.config = ConfigHandler(
            nemo_url=nemo_url,
            tenant=tenant,
            userid=userid,
            password=password,
            environment=environment,
            hubspot_api_token=hubspot_api_token,
            config_file=config_file,
        )

        super().__init__()

    def getProjectList(self):
        """
        Retrieves a list of projects from the server.

        Returns:
            pd.DataFrame: DataFrame containing the list of projects.
        """
        return getProjectList(self.config)

    def getProjectID(self, projectname: str):
        """
        Retrieves the project ID for a given project name.

        Args:
            projectname (str): The name of the project for which to retrieve the ID.

        Returns:
            str: The ID of the specified project.
        """
        return getProjectID(self.config, projectname)

    def getProjectProperty(self, projectname: str, propertyname: str):
        """
        Retrieves a specified property for a given project from the server.

        Args:
            projectname (str): The name of the project for which to retrieve the property.
            propertyname (str): The name of the property to retrieve.

        Returns:
            str: The value of the specified property for the given project.

        Raises:
            Exception: If the request to the server fails.
        """
        return getProjectProperty(self.config, projectname, propertyname)

    def ReUploadFile(
        self,
        projectname: str,
        filename: str,
        update_project_settings: bool = True,
        datasource_ids: list[dict] = None,
        global_fields_mapping: list[dict] = None,
        version: int = 2,
        trigger_only: bool = False,
    ):
        """
        Uploads a file to a project and optionally updates project settings or triggers analyze tasks.

        Args:
            projectname (str): Name of the project.
            filename (str): Name of the file to be uploaded.
            update_project_settings (bool, optional): Whether to update project settings after ingestion. Defaults to True.
            datasource_ids (list[dict], optional): List of datasource identifiers for V3 ingestion. Defaults to None.
            global_fields_mapping (list[dict], optional): Global fields mapping for V3 ingestion. Defaults to None.
            version (int, optional): Version of the ingestion process (2 or 3). Defaults to 2.
            trigger_only (bool, optional): Whether to trigger only without waiting for task completion. Applicable for V3. Defaults to False.
        """

        ReUploadFileIngestion(
            config=self.config,
            projectname=projectname,
            filename=filename,
            update_project_settings=update_project_settings,
            datasource_ids=datasource_ids,
            global_fields_mapping=global_fields_mapping,
            version=version,
            trigger_only=trigger_only,
        )

    def synchMetadataWithFocus(self, metadatafile: str, projectId: str):
        """
        Synchronizes metadata from a given CSV file with the NEMO project metadata.

        This method reads metadata from a CSV file, processes it, and synchronizes it with
        the metadata of a specified NEMO project. It handles the creation of groups first
        and then processes individual attributes.

        Args:
            config (ConfigHandler): Configuration handler instance to retrieve configuration details.
            metadatafile (str): Path to the CSV file containing metadata.
            projectId (str): The ID of the NEMO project to synchronize with.

        Raises:
            Exception: If any request to the NEMO API fails or if an unexpected error occurs.
        """
        synchMetadataWithFocus(
            config=self.config, metadatafile=metadatafile, projectId=projectId
        )

    def exportMetadata(self, infozoomexe: str, infozoomfile: str, metadatafile: str):
        """
        Exports metadata from an InfoZoom file using the InfoZoom executable.

        Args:
            infozoomexe (str): Path to the InfoZoom executable.
            infozoomfile (str): Path to the InfoZoom file.
            metadatafile (str): Path to the metadata output file.

        Returns:
            None

        Prints:
            str: Output messages including the execution status and version information.

        Raises:
            subprocess.CalledProcessError: If the command execution fails.
        """

        exportMetadata(
            config=self.config,
            infozoomexe=infozoomexe,
            infozoomfile=infozoomfile,
            metadatafile=metadatafile,
        )

    def LoadReport(
        self, projectname: str, report_guid: str, max_pages=None
    ) -> pd.DataFrame:
        """
        Loads a report from a specified project and returns it as a pandas DataFrame.

        Args:
            projectname (str): The name of the project from which the report is to be loaded.
            report_guid (str): The GUID (Globally Unique Identifier) of the report to be loaded.
            max_pages (int, optional): Maximum number of pages to load. Defaults to None.

        Returns:
            pandas.DataFrame: The report data as a DataFrame.

        Raises:
            Exception: If the request to load the report fails or if downloading the CSV fails.

        """
        return LoadReport(self.config, projectname, report_guid, max_pages)

    def FetchDealFromHubSpotAndUploadToNEMO(self, projectname: str) -> None:
        """
        Handles the processing and uploading of CRM deal activities to NEMO.

        This function interacts with HubSpot's API to retrieve deal information, activity history,
        and associated details, then merges and enriches the data before uploading it to the NEMO system.

        Parameters:
        -----------
        config : ConfigHandler
            An instance of ConfigHandler containing configuration settings, including API credentials
            and other necessary parameters.

        projectname : str
            The name of the project to which the deal data should be uploaded in NEMO.

        Process:
        --------
        1. Retrieves the HubSpot API token using the provided configuration.
        2. Loads deals from the CRM system.
        3. Loads and processes deal change history and activity data.
        4. Merges deal history and activity data with deal details.
        5. Resolves internal fields (e.g., company ID, user ID) to their corresponding plain text representations.
        6. Maps deal stages to their respective descriptive names.
        7. Uploads the processed deal data to the specified project in NEMO.

        Returns:
        --------
        None
            This function does not return any values. It performs operations that affect the state of
            the CRM data in the NEMO system.
        """        
        CRM_Activities_handler(config=self.config, projectname=projectname)

    #################################################################################################################################################################

    def getImportedColumns(self, projectname: str):
        project_id = None

        try:
            project_id = self.getProjectID(projectname)

            # initialize reqeust
            headers = connection_get_headers(self.config)
            response = requests.get(
                self.config.config_get_nemo_url()
                + ENDPOINT_URL_PERSISTENCE_METADATA_IMPORTED_COLUMNS.format(
                    projectId=project_id
                ),
                headers=headers,
            )
            if response.status_code != 200:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            return df

        except Exception as e:
            if project_id == None:
                raise Exception("process stopped, no project_id available")
            raise Exception("process aborted")

    #################################################################################################################################################################

    def synchronizeCsvColsAndImportedColumns(self, projectname: str, filename: str):
        importedColumns = self.getImportedColumns(projectname)
        project_id = self.getProjectID(projectname)

        # Read the first line of the CSV file to get column names
        with open(filename, "r") as file:
            first_line = file.readline().strip()

        # Split the first line into a list of column names
        csv_column_names = first_line.split(";")

        # Check if a record exists in the DataFrame for each column
        for column_name in csv_column_names:
            displayName = column_name
            column_name = self.clean_column_name(
                column_name, RESERVED_KEYWORDS
            )  # Assuming you have the clean_column_name function from the previous script

            # Check if the record with internal_name equal to the column name exists
            if not importedColumns[
                importedColumns["internalName"] == column_name
            ].empty:
                print(f"Record found for column '{column_name}' in the DataFrame.")
            else:
                print(
                    f"******************************No record found for column '{column_name}' in the DataFrame."
                )
                new_importedColumn = {
                    "id": "",
                    "internalName": column_name,
                    "displayName": displayName,
                    "importName": displayName,
                    "description": "",
                    "dataType": "string",
                    "categorialType": False,
                    "businessEvent": False,
                    "unit": "",
                    "columnType": "ExportedColumn",
                    "tenant": self.config.config_get_tenant(),
                    "projectId": project_id,
                }

                self.createImportedColumn(new_importedColumn, project_id)

    #################################################################################################################################################################

    def clean_column_name(self, column_name, reserved_keywords):
        # If csv column name is empty, return "undefined_name"
        if not column_name:
            return "undefined_name"

        # Replace all chars not matching regex [^a-zA-Z0-9_] with empty char
        cleaned_name = re.sub(r"[^a-zA-Z0-9_]", "", column_name)

        # Convert to lowercase
        cleaned_name = cleaned_name.lower()

        # If starts with a number, concatenate "numeric_" to the beginning
        if cleaned_name[0].isdigit():
            cleaned_name = "numeric_" + cleaned_name

        # Replace all double "_" chars with one "_"
        cleaned_name = re.sub(r"_{2,}", "_", cleaned_name)

        # If length of csv column name equals 1 or is a reserved keyword, concatenate "_" to the end
        if len(cleaned_name) == 1 or cleaned_name in reserved_keywords:
            cleaned_name += "_"

        return cleaned_name

    #################################################################################################################################################################

    def createImportedColumn(self, importedColumn: json, project_id: str):
        try:

            # initialize reqeust
            headers = connection_get_headers(self.config)
            response = requests.post(
                self.config.config_get_nemo_url()
                + ENDPOINT_URL_PERSISTENCE_METADATA_CREATE_IMPORTED_COLUMN,
                headers=headers,
                json=importedColumn,
            )
            if response.status_code != 201:
                raise Exception(
                    f"request failed. Status: {response.status_code}, error: {response.text}"
                )
            resultjs = json.loads(response.text)
            df = pd.json_normalize(resultjs)
            return df

        except Exception as e:
            raise Exception("process aborted")
