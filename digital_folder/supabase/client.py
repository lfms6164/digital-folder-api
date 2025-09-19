from supabase import Client, create_client

from digital_folder.core.config import project_settings


def get_supabase_client() -> Client:
    return create_client(
        project_settings.project_url, project_settings.service_role_key
    )
