from http import HTTPStatus

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse

from config.settings import settings

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f'{settings.API_PATH}/openapi.json',
    debug=True,
    description='API that helps owners manage their estate(s)',
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)


@app.get('/', status_code=HTTPStatus.OK)
async def root():
    return {'message': 'AgroAPI', 'version': settings.VERSION}


@app.get('/up', status_code=HTTPStatus.OK)
async def up():
    return {'message': 'ok'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
async def html():
    return """<html>
        <head>AgroAPI</head>
        <body>🚜</body>
    </html>"""
