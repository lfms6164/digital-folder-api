from fastapi import HTTPException
from pydantic import BaseModel
from supabase import Client, create_client

from digital_folder.core.config import project_settings


class SupabaseStorageConfig(BaseModel):
    bucket: str
    folder: str


def get_supabase_client() -> Client:
    return create_client(
        project_settings.project_url, project_settings.service_role_key
    )


def validate_bucket(bucket: str) -> str:
    if not bucket or bucket not in ["dev", "prod"]:
        raise HTTPException(
            status_code=404, detail="Supabase storage bucket is invalid."
        )

    return bucket
