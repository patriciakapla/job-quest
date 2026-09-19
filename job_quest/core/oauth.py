from authlib.integrations.starlette_client import OAuth

from job_quest.core.settings import Settings

settings = Settings()

oauth = OAuth()

oauth.register(
    name='google',
    server_metadata_url=(
        'https://accounts.google.com/.well-known/openid-configuration'
    ),
    client_id=settings.GOOGLE_CLIENT_ID,
    client_secret=settings.GOOGLE_CLIENT_SECRET,
    client_kwargs={'scope': 'openid email profile'},
)
