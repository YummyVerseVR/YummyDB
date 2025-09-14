from fastapi import FastAPI, APIRouter, Form, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from uuid import UUID
import os
import requests

from db.controller import DataBase


class App:
    def __init__(self, db_path: str, controller_endpoint: str):
        self.__db = DataBase(db_path)
        self.__app = FastAPI()
        self.__router = APIRouter()

        self.__controller_endpoint = controller_endpoint
        self.__setup_routes()

    def __setup_routes(self):
        self.__router.add_api_route("/", self.root, methods=["GET"])

        self.__router.add_api_route(
            "/{userID}/status", self.data_status, methods=["GET"]
        )
        self.__router.add_api_route("/create/user", self.create_user, methods=["POST"])
        self.__router.add_api_route("/save/model", self.save_model, methods=["POST"])
        self.__router.add_api_route("/save/audio", self.save_audio, methods=["POST"])
        self.__router.add_api_route("/{user_id}/model", self.get_model, methods=["GET"])
        self.__router.add_api_route("/{user_id}/audio", self.get_audio, methods=["GET"])

    def __send_notify(self, user_id: str) -> None:
        body = {"uuid": user_id, "is_ready": True}
        requests.post(f"{self.__controller_endpoint}/set-user-status", json=body)

    def get_app(self) -> FastAPI:
        self.__app.include_router(self.__router)
        return self.__app

    # /
    async def root(self) -> JSONResponse:
        return JSONResponse(
            {"message": "This is a database server for YummyVerse project."}
        )

    # /{user_id}/status
    async def data_status(self, user_id: str) -> JSONResponse:
        uuid = UUID(user_id)
        return JSONResponse({"user_id": str(uuid), "status": self.__db.is_ready(uuid)})

    # /create/user
    async def create_user(self, user_id: str = Form(...)) -> JSONResponse:
        uuid = UUID(user_id)
        self.__db.add_user(uuid)
        return JSONResponse({"message": f"User {uuid} created successfully."})

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

        if self.__db.is_ready(uuid):
            self.__send_notify(str(uuid))

        return JSONResponse(
            {"message": f"Model file for user {uuid} saved successfully."}
        )

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

        if self.__db.is_ready(uuid):
            self.__send_notify(str(uuid))

        return JSONResponse(
            {"message": f"Audio file for user {uuid} saved successfully."}
        )

    # /{user_id}/model
    async def get_model(self, user_id: str) -> FileResponse:
        uuid = UUID(user_id)
        model_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            model_path = userdata.get_model_path()
        else:
            return FileResponse("./dummy.glb", status_code=404)

        if not model_path or not os.path.exists(model_path):
            return FileResponse("./dummy.glb", status_code=404)

        return FileResponse(
            model_path,
            media_type="application/octet-stream",
            filename=os.path.basename(model_path),
        )

    # /{user_id}/audio
    async def get_audio(self, user_id: str) -> FileResponse:
        uuid = UUID(user_id)
        audio_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            audio_path = userdata.get_audio_path()
        else:
            return FileResponse("./dummy.glb", status_code=404)

        if not audio_path or not os.path.exists(audio_path):
            return FileResponse("./dummy.glb", status_code=404)

        return FileResponse(
            audio_path, media_type="audio/wav", filename=os.path.basename(audio_path)
        )
