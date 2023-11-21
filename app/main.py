from fastapi import FastAPI, Request, Response, Header
from fastapi.responses import HTMLResponse
from contextlib import asynccontextmanager
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from Models import DataBase
from dotenv import load_dotenv
from pathlib import Path
import uvicorn
import aiofile
import os


def load_env() -> tuple:
    load_dotenv()
    _db_name: str | None = os.getenv("DB_NAME")
    if (_db_name is None) or (_db_name == ""):
        raise Exception("db_name is None")
    _db_user: str | None = os.getenv("DB_USER")
    if (_db_user is None) or (_db_user == ""):
        raise Exception("db_user is None")
    _db_password: str | None = os.getenv("DB_PASSWORD")
    if (_db_password is None) or (_db_password == ""):
        raise Exception("db_password is None")
    _db_url: str | None = os.getenv("DB_URL")
    if (_db_url is None) or (_db_url == ""):
        raise Exception("DBName is None")
    _secret_key: str | None = os.getenv("SECRET_KEY")
    if (_secret_key is None) or (_secret_key == ""):
        raise Exception("Secret key is None")
    return _db_name, _db_user, _db_password, _db_url, _secret_key


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db_connection.connect()
    yield
    await db_connection.close()


FastFlixHub = FastAPI(
    docs_url=None,
    redoc_url=None,
    lifespan=lifespan
)

templates = Jinja2Templates(directory="./app/templates")
FastFlixHub.mount("/static", StaticFiles(directory="./app/static"), name="static")
db_name, db_user, db_password, db_url, secret_key = load_env()
db_connection = DataBase.DataBase(db_name=db_name, db_user=db_user,
                                  db_password=db_password, db_url=db_url)
CHUNK_SIZE = 1024*1024
video_path = Path("video.mp4")


@FastFlixHub.get(path="/", response_class=HTMLResponse)
async def root(request: Request):
    row = await db_connection.search_user(_id=56462346456)
    search_user_by_id: list = []
    if row["status"] is True:
        search_user_by_id = row["message"]
    else:
        print(f"Error!\nMessage: {row}")

    return templates.TemplateResponse("index.html", {"request": request,
                                                     "user": "user 12345",
                                                     "search_user_by_id": search_user_by_id})


@FastFlixHub.get(path="/test_video", response_class=HTMLResponse)
async def test_video_page(request: Request):
    return templates.TemplateResponse("video.html", {"request": request})


@FastFlixHub.get("/video")
async def video_endpoint(request: Request, _range: str = Header(None)):
    if _range is None:
        return templates.TemplateResponse("404.html", {"request": request})
    start, end = _range.replace("bytes=", "").split("-")
    start = int(start)
    end = int(end) if end else start + CHUNK_SIZE
    async with aiofile.async_open(video_path, "rb") as video:
        video.seek(start)
        data = await video.read(end - start)
        file_size = str(video_path.stat().st_size)
        headers = {
            'Content-Range': f'bytes {str(start)}-{str(end)}/{file_size}',
            'Accept-Ranges': 'bytes'
        }
        return Response(data, status_code=206, headers=headers, media_type="video/mp4")


if __name__ == "__main__":
    uvicorn.run("main:FastFlixHub", host="0.0.0.0", port=8000)
