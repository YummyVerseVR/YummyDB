from fastapi import FastAPI, APIRouter, Form, UploadFile, File
from fastapi.responses import FileResponse, JSONResponse
from uuid import UUID
import os
import requests

from db.controller import DataBase


class App:
    def __init__(
        self,
        db_path: str,
        controller_endpoint: str,
        debug: bool = False,
    ):
        self.__debug = debug
        self.__db = DataBase(db_path)
        self.__app = FastAPI()
        self.__router = APIRouter()

        self.__controller_endpoint = controller_endpoint
        self.__setup_routes()

    def __setup_routes(self):
        self.__router.add_api_route("/notify/{user_id}", self.notify, methods=["GET"])
        self.__router.add_api_route(
            "/{userID}/status", self.data_status, methods=["GET"]
        )
        self.__router.add_api_route("/create/user", self.create_user, methods=["POST"])
        self.__router.add_api_route("/save/qr", self.save_qr, methods=["POST"])
        self.__router.add_api_route("/save/image", self.save_image, methods=["POST"])
        self.__router.add_api_route("/save/model", self.save_model, methods=["POST"])
        self.__router.add_api_route("/save/audio", self.save_audio, methods=["POST"])
        self.__router.add_api_route("/save/param", self.save_param, methods=["POST"])
        self.__router.add_api_route("/{user_id}/qr", self.get_qr, methods=["GET"])
        self.__router.add_api_route("/{user_id}/image", self.get_image, methods=["GET"])
        self.__router.add_api_route("/{user_id}/model", self.get_model, methods=["GET"])
        self.__router.add_api_route("/{user_id}/audio", self.get_audio, methods=["GET"])
        self.__router.add_api_route("/{user_id}/param", self.get_param, methods=["GET"])
        self.__router.add_api_route("/ping", self.ping, methods=["GET"])

    def __send_notify(self, user_id: str) -> None:
        body = {"uuid": user_id, "is_ready": True}

        if self.__debug:
            print(f"Notify {self.__controller_endpoint}/set-user-status: {body}")
            return

        requests.post(f"{self.__controller_endpoint}/set-user-status", json=body)

    def get_app(self) -> FastAPI:
        self.__app.include_router(self.__router)
        return self.__app

    # /notify/{user_id}
    async def notify(self, _: str) -> JSONResponse:
        return JSONResponse({"message": "This endpoint is deprecated."})

    # /{user_id}/status
    async def data_status(self, user_id: str) -> JSONResponse:
        uuid = UUID(user_id)
        return JSONResponse({"user_id": str(uuid), "status": self.__db.is_ready(uuid)})

    # /create/user
    async def create_user(self, user_id: str = Form(...)) -> JSONResponse:
        uuid = UUID(user_id)
        self.__db.add_user(uuid)
        return JSONResponse({"message": f"User {uuid} created successfully."})

    # /save/qr
    async def save_qr(
        self,
        user_id: str = Form(...),
        file: UploadFile = File(...),
    ) -> JSONResponse:
        uuid = UUID(user_id)
        if not self.__db.is_exist(uuid):
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        self.__db.load_qr(uuid, file)

        if self.__db.is_ready(uuid):
            self.__send_notify(str(uuid))

        return JSONResponse({"message": f"QR file for user {uuid} saved successfully."})

    # /save/image
    async def save_image(
        self,
        user_id: str = Form(...),
        file: UploadFile = File(...),
    ) -> JSONResponse:
        uuid = UUID(user_id)
        if not self.__db.is_exist(uuid):
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        self.__db.load_image(uuid, file)

        if self.__db.is_ready(uuid):
            self.__send_notify(str(uuid))

        return JSONResponse(
            {"message": f"Image file for user {uuid} saved successfully."}
        )

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

    # /save/param
    async def save_param(
        self,
        user_id: str = Form(...),
        file: UploadFile = File(...),
    ) -> JSONResponse:
        uuid = UUID(user_id)
        if not self.__db.is_exist(uuid):
            return JSONResponse(
                status_code=404, content={"message": f"User {uuid} not found."}
            )

        self.__db.load_param(uuid, file)

        if self.__db.is_ready(uuid):
            self.__send_notify(str(uuid))

        return JSONResponse(
            {"message": f"Param file for user {uuid} saved successfully."}
        )

    # /{user_id}/qr
    async def get_qr(self, user_id: str) -> FileResponse:
        uuid = UUID(user_id)
        qr_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            qr_path = userdata.get_qr_path()
        else:
            return FileResponse("./dummy.png", status_code=404)

        if not qr_path or not os.path.exists(qr_path):
            return FileResponse("./dummy.png", status_code=404)

        return FileResponse(
            qr_path, media_type="image/png", filename=os.path.basename(qr_path)
        )

    # /{user_id}/image
    async def get_image(self, user_id: str) -> FileResponse:
        uuid = UUID(user_id)
        image_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            image_path = userdata.get_image_path()
        else:
            return FileResponse("./dummy.png", status_code=404)

        if not image_path or not os.path.exists(image_path):
            return FileResponse("./dummy.png", status_code=404)

        return FileResponse(
            image_path, media_type="image/png", filename=os.path.basename(image_path)
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
            return FileResponse("./dummy.wav", status_code=404)

        if not audio_path or not os.path.exists(audio_path):
            return FileResponse("./dummy.wav", status_code=404)

        return FileResponse(
            audio_path, media_type="audio/wav", filename=os.path.basename(audio_path)
        )

    # /{user_id}/param
    async def get_param(self, user_id: str) -> FileResponse:
        uuid = UUID(user_id)
        param_path = ""
        if (userdata := self.__db.get_user(uuid)) is not None:
            param_path = userdata.get_param_path()
        else:
            return FileResponse("./dummy.json", status_code=404)

        if not param_path or not os.path.exists(param_path):
            return FileResponse("./dummy.json", status_code=404)

        return FileResponse(
            param_path,
            media_type="application/json",
            filename=os.path.basename(param_path),
        )

    async def ping(self) -> JSONResponse:
        return JSONResponse({"message": "pong"})
