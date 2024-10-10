from wombo.models import StyleModel, ArtStylesModel, TaskModel, pydantic_version

from abc import ABC, abstractmethod, abstractproperty
from typing import TypeVar, Union

from httpx._client import AsyncClient, Client

T = TypeVar("T")

class BaseDream(ABC):
    _client: Union[Client, AsyncClient]
    class Utils:
        @staticmethod
        def _get_model(model: T, data: any) -> T:
            if pydantic_version.split(".")[0] == "1":
                return model.parse_obj(data)
            if pydantic_version.split(".")[0] == "2":
                return model.model_validate(data)
            raise ValueError

        @classmethod
        def _data_gen(cls, text: str, style: int) -> dict:
            return {
                "input_spec": {
                    "aspect_ratio": "old_vertical_ratio",
                    "prompt": text,
                    "style": cls._what_style(style),
                    "display_freq": 10
                }
            }

        @staticmethod
        def _headers_gen(auth_key: str) -> dict:
            return {
                "authorization": f"bearer {auth_key}",
                "x-app-version": "WEB-2.0.0",
            }

        @staticmethod
        def _what_style(style: Union[int, ArtStylesModel]) -> dict:
            if isinstance(style, ArtStylesModel):
                return style.id
            return style

    class Style(ABC):
        def __init__(self, dream: "BaseDream") -> None:
            self.dream = dream
            self.styles = None

        def __getitem__(self, key: str) -> Union[int, ArtStylesModel]:
            if self.styles is None:
                return 115
            for style in self.styles.root:
                if key == style.name:
                    return style
            return 115

        @property
        def free(self) -> StyleModel:
            res = [style for style in self.styles.root if not style.is_premium]
            return self.dream.Utils._get_model(StyleModel, res)

        @property
        def premium(self) -> StyleModel:
            res = [style for style in self.styles.root if style.is_premium]
            return self.dream.Utils._get_model(StyleModel, res)

        def _save_styles(self, styles: StyleModel) -> None:
            self.styles = styles

        @abstractproperty
        def url(self) -> str:
            ...

        @abstractmethod
        def _get_styles(self)-> StyleModel:
            ...

    class Auth(ABC):
        urls = {
            "js_filename": "https://dream.ai/create",
            "google_key": "https://dream.ai/_next/static/chunks/pages/_app-{js_filename}.js",
            "auth_key": "https://identitytoolkit.googleapis.com/v1/accounts:signUp"
        }
        def __init__(self, dream: "BaseDream", token: str = None) -> None:
            self.dream = dream
            self.token = token

        def _save_token(self, token: str) -> None:
            self.token = token

        @abstractmethod
        def _get_js_filename(self) -> str:
            ...

        @abstractmethod
        def _get_google_key(self) -> str:
            ...

        @abstractmethod
        def _get_auth_key(self) -> str:
            ...

    class API(ABC):
        url = "https://paint.api.wombo.ai/api/v2/tasks"
        def __init__(self, dream: "BaseDream") -> None:
            self.dream = dream

        @abstractmethod
        def create_task(self, text: str, style: Union[int, ArtStylesModel] = 115)-> TaskModel:
            ...

        @abstractmethod
        def check_task(self, task_id: str) -> TaskModel:
            ...

    def __init__(self, token: str = None, debug: bool = False):
        self.style = self.Style(self)
        self.auth = self.Auth(self, token=token)
        self.api = self.API(self)
        self.debug = debug

    @abstractmethod
    def generate(self, text: str, style: Union[int, ArtStylesModel] = 115, *, timeout: int = 60, check_for: int = 3) -> TaskModel:
        ...