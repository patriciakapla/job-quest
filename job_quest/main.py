from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from starlette.middleware.sessions import SessionMiddleware

from job_quest.core.settings import Settings
from job_quest.exceptions import (
    ApplicationNotFoundError,
    InvalidSalaryRangeError,
    ResumeNotFoundError,
)
from job_quest.routers.applications_routers import (
    router as applications_router,
)
from job_quest.routers.auth_routers import router as google_auth_router
from job_quest.routers.resumes_routers import router as resumes_router
from job_quest.routers.users_routers import router as users_router

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
app.include_router(users_router)
app.include_router(applications_router)
app.include_router(resumes_router)


@app.exception_handler(InvalidSalaryRangeError)
async def invalid_salary_range_handler(
    request: Request,
    exc: InvalidSalaryRangeError,
) -> JSONResponse:
    return JSONResponse(
        status_code=422,
        content={'detail': str(exc)},
    )


@app.exception_handler(ApplicationNotFoundError)
async def application_not_found_handler(
    request: Request, exc: ApplicationNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={'detail': str(exc)})


@app.exception_handler(ResumeNotFoundError)
async def resume_not_found_handler(
    request: Request, exc: ResumeNotFoundError
) -> JSONResponse:
    return JSONResponse(status_code=404, content={'detail': str(exc)})
