import json
import os
from typing import Any, Dict, Optional

from sqlmodel import Session, SQLModel, create_engine

from ._logging import logger


class Persistence:
    _instance = None

    def __init__(self, database_url: Optional[str] = None, connect_args: Optional[Dict[str, Any]] = None, engine_args: Optional[Dict[str, Any]] = None) -> None:
        self._database_url = database_url
        self._connect_args = connect_args
        self._engine_args = engine_args

        if not database_url and 'DATABASE_URL' in os.environ:
            self._database_url = os.environ['DATABASE_URL']
        if not connect_args and 'DATABASE_CONNECT_ARGS' in os.environ:
            self._connect_args = json.loads(
                os.environ['DATABASE_CONNECT_ARGS'])
        if not engine_args and 'DATABASE_ENGINE_ARGS' in os.environ:
            self._engine_args = json.loads(
                os.environ['DATABASE_ENGINE_ARGS'])
        if not self._database_url:
            self._database_url = f"sqlite:///{os.path.join(os.getcwd(), 'myla.db')}"
            logger.warn(f"DATABASE_URL not specified, use {self._database_url}")

        if not self._connect_args:
            self._connect_args = {}

        if not self._engine_args:
            self._engine_args = {}

        self._engine = create_engine(
            self._database_url,
            connect_args=self._connect_args,
            json_serializer=lambda obj: json.dumps(obj, ensure_ascii=False),
            **self._engine_args
        )

    @property
    def engine(self):
        return self._engine

    def create_session(self) -> Session:
        return Session(self._engine)

    def initialize_database(self):
        SQLModel.metadata.create_all(self._engine)

    @staticmethod
    def default():
        if not Persistence._instance:
            Persistence._instance = Persistence()
        return Persistence._instance
