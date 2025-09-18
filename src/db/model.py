from fastapi import UploadFile
from uuid import UUID
import os
import shutil


class UserData:
    QR_FILE = "qr.png"
    IMAGE_FILE = "image.png"
    MODEL_FILE = "model.glb"
    AUDIO_FILE = "audio.wav"
    PARAM_FILE = "params.json"

    def __init__(self, user_id: UUID, db_path: str):
        self.__db_path = db_path
        self.__uuid = user_id
        self.__qr_path = os.path.join(self.get_user_path(), UserData.QR_FILE)
        self.__image_path = os.path.join(self.get_user_path(), UserData.IMAGE_FILE)
        self.__model_path = os.path.join(self.get_user_path(), UserData.MODEL_FILE)
        self.__audio_path = os.path.join(self.get_user_path(), UserData.AUDIO_FILE)
        self.__param_path = os.path.join(self.get_user_path(), UserData.PARAM_FILE)
        self.__status = {
            UserData.QR_FILE: False,
            UserData.IMAGE_FILE: False,
            UserData.MODEL_FILE: False,
            UserData.AUDIO_FILE: False,
            UserData.PARAM_FILE: False,
        }

        os.makedirs(self.get_user_path(), exist_ok=True)

    def get_uuid(self) -> UUID:
        return self.__uuid

    def get_user_path(self) -> str:
        return os.path.join(self.__db_path, str(self.__uuid))

    def get_qr_path(self) -> str:
        return self.__qr_path if os.path.exists(self.__qr_path) else ""

    def get_image_path(self) -> str:
        return self.__image_path if os.path.exists(self.__image_path) else ""

    def get_model_path(self) -> str:
        return self.__model_path if os.path.exists(self.__model_path) else ""

    def get_audio_path(self) -> str:
        return self.__audio_path if os.path.exists(self.__audio_path) else ""

    def get_param_path(self) -> str:
        return self.__param_path if os.path.exists(self.__param_path) else ""

    def set_status(self, file_type: str, status: bool) -> None:
        if file_type in self.__status.keys():
            self.__status[file_type] = status

    def is_ready(self) -> bool:
        return all(self.__status.values())

    def load_qr(self, qr_data: UploadFile) -> None:
        self.__status[UserData.QR_FILE] = True
        if os.path.exists(self.__qr_path):
            os.remove(self.__qr_path)

        with open(self.__qr_path, "wb") as f:
            shutil.copyfileobj(qr_data.file, f)

    def load_image(self, image_data: UploadFile) -> None:
        self.__status[UserData.IMAGE_FILE] = True
        if os.path.exists(self.__image_path):
            os.remove(self.__image_path)

        with open(self.__image_path, "wb") as f:
            shutil.copyfileobj(image_data.file, f)

    def load_model(self, model_data: UploadFile) -> None:
        self.__status[UserData.MODEL_FILE] = True
        if os.path.exists(self.__model_path):
            os.remove(self.__model_path)

        with open(self.__model_path, "wb") as f:
            shutil.copyfileobj(model_data.file, f)

    def load_audio(self, audio_data: UploadFile) -> None:
        self.__status[UserData.AUDIO_FILE] = True
        if os.path.exists(self.__audio_path):
            os.remove(self.__audio_path)

        with open(self.__audio_path, "wb") as f:
            shutil.copyfileobj(audio_data.file, f)

    def load_param(self, param_data: UploadFile) -> None:
        self.__status[UserData.PARAM_FILE] = True
        if os.path.exists(self.__param_path):
            os.remove(self.__param_path)

        with open(self.__param_path, "wb") as f:
            shutil.copyfileobj(param_data.file, f)
