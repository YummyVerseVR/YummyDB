from fastapi import FastAPI, APIRouter, Form, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from uuid import UUID
import os

from db.controller import DataBase
from db.model import UserData


class App:
    DATABASE_PATH = os.path.join(os.getcwd(), "YummyDB")

    def __init__(self):
        self.__db = DataBase(App.DATABASE_PATH)
        self.__app = FastAPI()
        self.__router = APIRouter()

        self.__setup_routes()

    def __setup_routes(self):
        self.__router.add_api_route("/", self.root, methods=["GET"])

        self.__router.add_api_route(
            "/{userID}/status", self.data_status, methods=["POST"]
        )
        self.__router.add_api_route("/create/user", self.create_user, methods=["POST"])
        self.__router.add_api_route("/save/model", self.save_model, methods=["POST"])
        self.__router.add_api_route("/save/audio", self.save_audio, methods=["POST"])
        self.__router.add_api_route("/{userID}/model", self.get_model, methods=["POST"])
        self.__router.add_api_route("/{userID}/audio", self.get_audio, methods=["POST"])

    def get_app(self) -> FastAPI:
        self.__app.include_router(self.__router)
        return self.__app

    # /
    async def root(self) -> JSONResponse:
        return {"message": "This is a database server for YummyVerse project."}

    # /{userID}/status
    async def data_status(self, user_id: str = Form(...)) -> JSONResponse:
        uuid = UUID(user_id)
        return {"user_id": str(uuid), "status": self.__db.is_ready(uuid)}

    # /create/user
    async def create_user(self, user_id: str = Form(...)) -> JSONResponse:
        uuid = UUID(user_id)
        self.__db.add_user(uuid)
        return {"message": f"User {uuid} created successfully."}

    # /save/model
    async def save_model(
        self,
        user_id: str = Form(...),
        file: UploadFile = File(...),
    ) -> JSONResponse:
        uuid = UUID(user_id)
        if not self.__db.is_exist(uuid):
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        self.__db.load_model(uuid, file)
        return {"message": f"Model file for user {uuid} saved successfully."}

    # /save/audio
    async def save_audio(
        self,
        user_id: str = Form(...),
        file: UploadFile = File(...),
    ) -> JSONResponse:
        uuid = UUID(user_id)
        if not self.__db.is_exist(uuid):
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        self.__db.load_audio(uuid, file)
        return {"message": f"Audio file for user {uuid} saved successfully."}

    # /{userID}/model
    async def get_model(self, user_id: str = Form(...)) -> FileResponse:
        uuid = UUID(user_id)
        model_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            model_path = userdata.get_model_path()
        else:
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        if not model_path or not os.path.exists(model_path):
            return JSONResponse(
                status_code=404,
                content={"message": f"Model file for user {uuid} not found."},
            )

        return FileResponse(
            model_path,
            media_type="application/octet-stream",
            filename=os.path.basename(model_path),
        )

    # /{userID}/audio
    async def get_audio(self, user_id: str = Form(...)) -> FileResponse:
        uuid = UUID(user_id)
        audio_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            audio_path = userdata.get_audio_path()
        else:
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        if not audio_path or not os.path.exists(audio_path):
            return JSONResponse(
                status_code=404,
                content={"message": f"Audio file for user {uuid} not found."},
            )

        return FileResponse(
            audio_path, media_type="audio/wav", filename=os.path.basename(audio_path)
        )
