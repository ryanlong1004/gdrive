# Google Drive Service

This project provides a `GoogleDriveService` class for interacting with the Google Drive API. It includes methods for creating folders, uploading files, listing folders, listing folder contents, searching for files by MIME type, and listing all spaces in Google Drive.

## Setup

1. Clone the repository:

   ```sh
   git clone <repository_url>
   cd <repository_directory>
   ```

2. Create a virtual environment and activate it:

   ```sh
   python3 -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required dependencies:

   ```sh
   pip install -r requirements.txt
   ```

4. Add your `credentials.json` and `key.json` files to the project directory. These files should be added to the `.gitignore` file to avoid committing them to version control.

## Usage

### GoogleDriveService Class

The `GoogleDriveService` class provides the following methods:

- `get_credentials()`: Get user credentials for Google Drive API.
- `get_service()`: Build and return the Google Drive service.
- `create_folder(name: str) -> str`: Create a folder in Google Drive.
- `upload_to_folder(folder_id: str, file_path: str) -> str`: Upload a file to a specified folder in Google Drive.
- `list_folders() -> list`: List all folders in Google Drive.
- `list_folder_contents(folder_id: str) -> list`: List all contents of a specific folder in Google Drive.
- `search_file(mime_type: str) -> list`: Search for files in Google Drive by MIME type.
- `list_spaces() -> list`: List all spaces in Google Drive.

### Example

Here is an example of how to use the `GoogleDriveService` class:

```python
from main import GoogleDriveService

def main():
    service = GoogleDriveService()

    # List all folders
    folders = service.list_folders()
    for folder in folders:
        print(folder)

    # Create a new folder
    folder_id = service.create_folder("New Folder")
    print(f"Created folder with ID: {folder_id}")

    # Upload a file to the new folder
    file_id = service.upload_to_folder(folder_id, "path/to/your/file.txt")
    print(f"Uploaded file with ID: {file_id}")

    # List contents of the new folder
    contents = service.list_folder_contents(folder_id)
    for item in contents:
        print(item)

    # Search for JPEG files
    jpeg_files = service.search_file("image/jpeg")
    for file in jpeg_files:
        print(file)

    # List all spaces
    spaces = service.list_spaces()
    for space in spaces:
        print(space)

if __name__ == "__main__":
    main()
```

## Logging

The project uses Python's built-in `logging` module to log information, errors, and other messages. The log level is set to `INFO` by default. You can change the log level by modifying the `logging.basicConfig(level=logging.INFO)` line in `main.py`.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.
