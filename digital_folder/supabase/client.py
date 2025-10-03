from fastapi import HTTPException
from pydantic import BaseModel
from supabase import Client, create_client

from digital_folder.core.config import project_settings


class SupabaseStorageConfig(BaseModel):
    bucket: str
    folder: str


def get_supabase_client() -> Client:
    """
    Initialize a new Supabase client using the unique Supabase project url and the unique Supabase service role key.


    Returns:
        Client: The Supabase client.
    """
    return create_client(
        project_settings.project_url, project_settings.service_role_key
    )


def validate_folder(folder: str) -> str:
    """
    Checks if provided folder name is valid.

    Args:
        folder (str): The folder name.

    Returns:
        str: The folder name.
    """

    if not folder or folder not in ["projects", "tickets"]:
        raise HTTPException(
            status_code=404, detail="Supabase storage folder is invalid."
        )

    return folder
