from typing import List

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile

from digital_folder.db.dependencies import get_db_with_user
from digital_folder.db.service import DbService
from digital_folder.supabase.client import (
    get_supabase_client,
    SupabaseStorageConfig,
    validate_bucket,
)

supabase_router = APIRouter()


@supabase_router.post(path="/upload_files/{bucket}/{folder}")
async def upload_files(
    bucket: str,
    folder: str,
    files: List[UploadFile] = File(...),
    _: DbService = Depends(get_db_with_user),
) -> dict[str, List[str]]:
    """Upload files to Supabase and return the file names"""

    config = SupabaseStorageConfig(bucket=bucket, folder=folder)
    file_names = await SupabaseDTO(config).upload_files(files)

    return {"file_names": file_names}


class SupabaseDTO:
    def __init__(self, config: SupabaseStorageConfig):
        self.supabase_client = get_supabase_client()
        self.bucket = validate_bucket(config.bucket)
        self.folder = config.folder

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
                path=f"{self.folder}/temp/{file.filename}",
                file=file_bytes,
                file_options={
                    "cache-control": "3600",
                    "upsert": "true",
                    "content-type": file.content_type,
                },
            )

            file_names.append(file.filename)

        return file_names

    def get_files_from_folder(self, subfolder: str) -> List[str]:
        """
        Get all files from a specific Supabase storage folder.

        Args:
            subfolder (str): The subfolder name.

        Returns:
            List[str]: The list of file names.
        """

        files = self.supabase_client.storage.from_(self.bucket).list(
            f"{self.folder}/{subfolder}",
            {
                "limit": 100,
                "offset": 0,
                "sortBy": {"column": "name", "order": "desc"},
            },
        )

        return [file["name"] for file in files] if files else []

    def move_files(self, files: List[str], subfolder: str) -> None:
        """
        Move files between Supabase storage folders.

        Args:
            files (List[str]): The file names to be moved.
            subfolder (str): The destination subfolder name.
        """

        for file in files:
            self.supabase_client.storage.from_(self.bucket).move(
                f"{self.folder}/temp/{file}",
                f"{self.folder}/{subfolder}/{file}",
            )

    def delete_files(self, files: List[str], subfolder: str) -> None:
        """
        Delete files from a Supabase storage folder.

        Args:
            files (List[str]): The files to be deleted.
            subfolder (str): The subfolder name.
        """

        files = [f"{self.folder}/{subfolder}/{file}" for file in files]

        self.supabase_client.storage.from_(self.bucket).remove(files)

    def delete_folder(self, subfolder: str) -> None:
        """
        Delete a Supabase storage folder.

        Args:
            subfolder (str): The subfolder name.
        """

        files = self.get_files_from_folder(subfolder)

        self.delete_files(files, subfolder)
