from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

import app.shared.registry
from app.api.exceptions_handler import register_exception_handlers
from app.api.router import router
from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f'{settings.API_PATH}/openapi.json',
    debug=True,
    description='API that helps owners manage their estate(s)',
)

register_exception_handlers(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(router)
