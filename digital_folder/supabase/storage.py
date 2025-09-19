from typing import Any, List

from fastapi import APIRouter, File, HTTPException, UploadFile

from digital_folder.supabase.client import get_supabase_client

supabase_router = APIRouter()


@supabase_router.post(path="/upload_files/{bucket}")
async def upload_files(bucket: str, files: List[UploadFile] = File(...)) -> Any:
    """Upload files to Supabase and return the file names"""

    file_names = await SupabaseDTO(bucket).upload_files(files)

    return {"file_names": file_names}


class SupabaseDTO:
    def __init__(self, bucket: str):
        self.bucket = bucket
        self.supabase_client = get_supabase_client()

    async def upload_files(self, files: List[UploadFile] = File(...)) -> List[str]:
        """
        Upload files to Supabase and return the file names.

        Args:
            files (List[UploadFile]): The list of files to be uploaded.

        Returns:
            List[str]: The list of uploaded file names.
        """

        file_names = []
        for file in files:
            file_extension = file.content_type.split("/")[-1]
            if file_extension not in ["png", "jpg", "jpeg", "gif"]:
                raise HTTPException(
                    status_code=400, detail="Upload image failed - Invalid file type"
                )

            file_bytes = await file.read()

            self.supabase_client.storage.from_(self.bucket).upload(
                path=f"temp/{file.filename}",
                file=file_bytes,
                file_options={
                    "cache-control": "3600",
                    "upsert": "true",
                    "content-type": file.content_type,
                },
            )

            file_names.append(file.filename)

        return file_names

    def list_files_from_folder(self, folder_name: str) -> List[str]:
        """
        List files from a Supabase storage folder.

        Args:
            folder_name (str): The folder name.

        Returns:
            List[str]: The list of file names.
        """

        files = self.supabase_client.storage.from_(self.bucket).list(
            folder_name,
            {
                "limit": 100,
                "offset": 0,
                "sortBy": {"column": "name", "order": "desc"},
            },
        )

        return [file["name"] for file in files] if files else []

    def move_files(self, files: List[str], folder_name: str) -> None:
        """
        Move files between Supabase storage folders.

        Args:
            files (List[str]): The file names to be moved.
            folder_name (str): The destination folder name.
        """

        for file in files:
            self.supabase_client.storage.from_(self.bucket).move(
                f"temp/{file}", f"{folder_name}/{file}"
            )

    def delete_files(self, files: List[str]) -> None:
        """
        Delete files from a Supabase storage folder.

        Args:
            files (List[str]): The files to be deleted.
        """

        self.supabase_client.storage.from_(self.bucket).remove(files)

    def delete_folder(self, folder_name: str) -> None:
        """
        Delete a Supabase storage folder.

        Args:
            folder_name (str): The folder name.
        """

        files = self.list_files_from_folder(folder_name)
        files = [f"{folder_name}/{file}" for file in files]

        self.delete_files(files)
