from django.conf import settings
from supabase import Client

def upload_to_bucket(file_path, destination_path):
    """Uploads a file to Supabase Storage"""
    with open(file_path, 'rb') as f:
        res = settings.supabase.storage.from_(settings.SUPABASE_BUCKET).upload(
            destination_path,
            f.read(),
            {"content-type": "auto"}
        )
    return f"{settings.SUPABASE_URL}/storage/v1/object/public/{settings.SUPABASE_BUCKET}/{destination_path}"

def delete_from_bucket(file_path):
    """Deletes a file from Supabase Storage"""
    settings.supabase.storage.from_(settings.SUPABASE_BUCKET).remove([file_path])