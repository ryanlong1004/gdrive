import logging
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import Resource, build
from googleapiclient.errors import HttpError
from googleapiclient.http import MediaFileUpload

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SCOPES = ["https://www.googleapis.com/auth/drive"]


class GoogleDriveService:
    """Service class for interacting with Google Drive API."""

    def __init__(self):
        """Initialize the GoogleDriveService with authenticated service."""
        self.service: Resource = self.get_service()

    def get_credentials(self) -> Credentials:
        """Get user credentials for Google Drive API.

        Returns:
            Credentials: The authenticated user credentials.
        """
        creds = None
        if os.path.exists("token.json"):
            return Credentials.from_authorized_user_file("token.json", SCOPES)
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                creds.refresh(Request())
            else:
                flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
                creds = flow.run_local_server(port=0)
            with open("token.json", "w") as token:
                token.write(creds.to_json())
        return creds

    def get_service(self) -> Resource:
        """Build and return the Google Drive service.

        Returns:
            Resource: The Google Drive service.
        """
        credentials = self.get_credentials()
        return build("drive", "v3", credentials=credentials)

    def create_folder(self, name: str) -> str:
        """Create a folder in Google Drive.

        Args:
            name (str): The name of the folder to create.

        Returns:
            str: The ID of the created folder.
        """
        try:
            file_metadata = {
                "name": name,
                "mimeType": "application/vnd.google-apps.folder",
            }
            file = self.service.files().create(body=file_metadata, fields="id").execute()
            logger.info('Folder ID: "%s".', file.get("id"))
            return file.get("id")
        except HttpError as error:
            logger.error("An error occurred: %s", error)
            return ""

    def upload_to_folder(self, folder_id: str, file_path: str) -> str:
        """Upload a file to a specified folder in Google Drive.

        Args:
            folder_id (str): The ID of the folder to upload the file to.
            file_path (str): The path of the file to upload.

        Returns:
            str: The ID of the uploaded file.
        """
        try:
            file_metadata = {
                "name": os.path.basename(file_path),
                "parents": [folder_id],
            }
            media = MediaFileUpload(file_path, resumable=True)
            file = self.service.files().create(body=file_metadata, media_body=media, fields="id").execute()
            logger.info('File ID: "%s".', file.get("id"))
            return file.get("id")
        except HttpError as error:
            logger.error("An error occurred: %s", error)
            return ""

    def list_folders(self) -> list:
        """List all folders in Google Drive.

        Returns:
            list: A list of folders.
        """
        try:
            query = "mimeType='application/vnd.google-apps.folder'"
            results = (
                self.service.files().list(q=query, spaces="drive", fields="nextPageToken, files(id, name)").execute()
            )
            items = results.get("files", [])
            if not items:
                logger.info("No folders found.")
                return []
            return items
        except HttpError as error:
            logger.error("An error occurred: %s", error)
            return []

    def list_folder_contents(self, folder_id: str) -> list:
        """List all contents of a specific folder in Google Drive.

        Args:
            folder_id (str): The ID of the folder to list contents of.

        Returns:
            list: A list of files in the folder.
        """
        try:
            query = f"'{folder_id}' in parents"
            results = (
                self.service.files().list(q=query, spaces="drive", fields="nextPageToken, files(id, name)").execute()
            )
            items = results.get("files", [])
            if not items:
                logger.info("No files found in the folder.")
                return []
            logger.info("Files in folder:")
            for item in items:
                logger.info("%s (%s)", item["name"], item["id"])
            return items
        except HttpError as error:
            logger.error("An error occurred: %s", error)
            return []

    def search_file(self, mime_type: str) -> list:
        """Search for files in Google Drive by MIME type.

        Args:
            mime_type (str): The MIME type of the files to search for.

        Returns:
            list: A list of files matching the MIME type.
        """
        try:
            files = []
            page_token = None
            while True:
                response = (
                    self.service.files()
                    .list(
                        q=f"mimeType='{mime_type}'",
                        spaces="drive",
                        fields="nextPageToken, files(id, name)",
                        pageToken=page_token,
                    )
                    .execute()
                )
                for file in response.get("files", []):
                    logger.info("Found file: %s, %s", file.get("name"), file.get("id"))
                    files.extend(response.get("files", []))
                page_token = response.get("nextPageToken", None)
                if page_token is None:
                    break
            return files
        except HttpError as error:
            logger.error("An error occurred: %s", error)
            return []

    def list_spaces(self) -> list:
        """List all spaces in Google Drive.

        Returns:
            list: A list of spaces.
        """
        try:
            results = self.service.spaces().list().execute()
            items = results.get("spaces", [])
            if not items:
                logger.info("No spaces found.")
                return []
            logger.info("Spaces:")
            for item in items:
                logger.info("%s (%s)", item["name"], item["id"])
            return items
        except HttpError as error:
            logger.error("An error occurred: %s", error)
            return []


def main():
    """Main function to demonstrate GoogleDriveService usage."""
    service = GoogleDriveService()
    folders = service.list_folders()
    for folder in folders:
        logger.info(folder)
    # Example usage of other methods
    # service.create_folder("test_folder")
    # service.upload_to_folder("folder_id", "file_path")
    # service.list_folder_contents("folder_id")
    # service.search_file("image/jpeg")
    # service.list_spaces()


if __name__ == "__main__":
    main()
