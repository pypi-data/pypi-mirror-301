import pandas as pd

from nemo_library.sub_config_handler import ConfigHandler
from nemo_library.sub_file_upload_handler import ReUploadFileIngestion
from nemo_library.sub_hubspot_handler import CRM_Activities_handler
from nemo_library.sub_project_handler import (
    getProjectID,
    getProjectList,
    getProjectProperty,
)
from nemo_library.sub_infozoom_handler import synchMetadataWithFocus, exportMetadata

from nemo_library.sub_report_handler import LoadReport
from nemo_library.sub_synch_file_columns_handler import (
    synchronizeCsvColsAndImportedColumns,
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

    def synchronizeCsvColsAndImportedColumns(
        self,
        projectname: str,
        filename: str,
    ) -> None:
        """
        Synchronizes the columns in a CSV file with the imported columns in the project.

        This function reads the column names from the first line of a specified CSV file and compares
        them with the imported columns for a given project. If a column from the CSV is not found in 
        the list of imported columns, it creates a new record for that column in the system.

        Args:
            projectname (str): The name of the project for which the columns are being synchronized.
            filename (str): The path to the CSV file whose columns need to be synchronized.

        Returns:
            None: The function performs its operation without returning a value.

        Steps:
            1. Retrieves the project ID based on the given project name.
            2. Reads the first line of the CSV file to get the column names.
            3. Cleans the column names using a `clean_column_name` function.
            4. For each CSV column, checks if an entry exists in the imported columns DataFrame.
            5. If no record is found for a column, a new record is created and added to the system.
        """

        synchronizeCsvColsAndImportedColumns(
            config=self.config,
            projectname=projectname,
            filename=filename,
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


