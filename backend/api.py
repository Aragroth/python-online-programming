"""Является точкой запуска API через uvicorn"""
from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware

from endpoints import auth, data, check, snippets
from endpoints import files
from core.config import settings
from core.security import get_user_by_token

app = FastAPI(openapi_prefix="/api")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.DEVELOPMENT_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(auth.router, tags=['Authorization'])
app.include_router(
    data.router,
    dependencies=[Depends(get_user_by_token)],
    tags=['Description data'],
)
app.include_router(
    check.router,
    prefix='/check',
    tags=['Checking code and quizzes'],
)
app.include_router(snippets.router, prefix='/snippets', tags=['Code snippets'])
app.include_router(files.router, prefix='/images', tags=['Files'])
