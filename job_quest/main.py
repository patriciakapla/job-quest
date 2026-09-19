from fastapi import FastAPI
from starlette.middleware.sessions import SessionMiddleware

from job_quest.core.settings import Settings
from job_quest.routers.auth import router as google_auth_router

app = FastAPI()

settings = Settings()


@app.get('/')
def main():
    print('Oh, hi! This is job-quest :)')
    return {'message': 'Oh, hi! This is job-quest :)'}


app.add_middleware(
    SessionMiddleware,
    secret_key=settings.SESSION_SECRET,
    https_only=settings.SESSION_HTTPS_ONLY,
)

app.include_router(google_auth_router)
