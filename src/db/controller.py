import os
from uuid import UUID
from typing import Any

from db.model import UserData


class DataBase:
    def __init__(self, db_path: str = "~/YummyDB/"):
        self.__db_path = os.path.expanduser(db_path)
        self.__tables: dict[UUID, UserData] = {}

        os.makedirs(self.__db_path, exist_ok=True)
        self.__load_tables()

    def __load_tables(self) -> None:
        for user_id in os.listdir(self.__db_path):
            try:
                uuid = UUID(user_id)
                self.__tables[uuid] = UserData(uuid, self.__db_path)
            except ValueError:
                continue

        for user_id, user_data in self.__tables.items():
            if os.path.exists(user_data.get_image_path()):
                user_data.set_status(UserData.IMAGE_FILE, True)
            if os.path.exists(user_data.get_model_path()):
                user_data.set_status(UserData.MODEL_FILE, True)
            if os.path.exists(user_data.get_audio_path()):
                user_data.set_status(UserData.AUDIO_FILE, True)
            if os.path.exists(user_data.get_param_path()):
                user_data.set_status(UserData.PARAM_FILE, True)

    def get_user(self, user_id: UUID) -> UserData | None:
        if user_id not in self.__tables.keys():
            return None

        return self.__tables[user_id]

    def is_exist(self, user_id: UUID) -> bool:
        return user_id in self.__tables.keys()

    def is_ready(self, user_id: UUID) -> bool:
        if user_id not in self.__tables.keys():
            return False

        return self.__tables[user_id].is_ready()

    def add_user(self, user_id: UUID):
        if user_id in self.__tables.keys():
            return self.__tables[user_id]

        user_data = UserData(user_id, self.__db_path)

        self.__tables[user_id] = user_data

    def load_image(self, user_id: UUID, image_data: Any) -> None:
        if user_id not in self.__tables.keys():
            raise ValueError(f"User {user_id} not found in database.")

        self.__tables[user_id].load_image(image_data)

    def load_model(self, user_id: UUID, model_data: Any) -> None:
        if user_id not in self.__tables.keys():
            raise ValueError(f"User {user_id} not found in database.")

        self.__tables[user_id].load_model(model_data)

    def load_audio(self, user_id: UUID, audio_data: Any) -> None:
        if user_id not in self.__tables.keys():
            raise ValueError(f"User {user_id} not found in database.")

        self.__tables[user_id].load_audio(audio_data)

    def load_param(self, user_id: UUID, param_data: Any) -> None:
        if user_id not in self.__tables.keys():
            raise ValueError(f"User {user_id} not found in database.")

        self.__tables[user_id].load_param(param_data)

    def should_notify(self, user_id: UUID) -> bool:
        if user_id not in self.__tables.keys():
            return False

        return self.__tables[user_id].is_ready()
