import lazy_object_proxy
from supabase import AClient, create_client
from supabase.lib.client_options import ClientOptions
from supamodel.config import settings


def create_sync_client():
    return create_client(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key,
        options=ClientOptions(postgrest_client_timeout=60),
    )


def create_async_client():
    return AClient(
        supabase_url=settings.supabase_url,
        supabase_key=settings.supabase_key,
        options=ClientOptions(postgrest_client_timeout=60),
    )


client = lazy_object_proxy.Proxy(create_sync_client)
aclient = lazy_object_proxy.Proxy(create_async_client)
