from wombo.base import BaseDream
from wombo.models import StyleModel, ArtStylesModel, TaskModel

from typing import Union
import asyncio
import re

from httpx import AsyncClient

class AsyncDream(BaseDream):
    class Style(BaseDream.Style):
        @property
        async def url(self) -> str:
            response = await self.dream._client.get("https://dream.ai/")
            regex = re.findall(r"/_next/static/([a-zA-Z0-9-]+)/_ssgManifest.js", response.text)
            return f"https://dream.ai/_next/data/{regex[0]}/create.json"

        async def _get_styles(self)-> StyleModel:
            response = await self.dream._client.get(await self.url)
            response = response.json().get("pageProps").get("artStyles")
            styles: StyleModel = self.dream.Utils._get_model(StyleModel, response)
            self._save_styles(styles)
            return styles

    class Auth(BaseDream.Auth):
        async def _get_js_filename(self) -> str:
            response = await self.dream._client.get(self.urls.get("js_filename"))
            js_filename = re.findall(r"_app-(\w+)", response.text)
            return js_filename[0]

        async def _get_google_key(self) -> str:
            js_filename = await self._get_js_filename()
            url = self.urls.get("google_key").format(js_filename=js_filename)
            response = await self.dream._client.get(url)
            key = re.findall(r'"(AI\w+)"', response.text)
            return key[0]

        async def _get_auth_key(self) -> str:
            if self.token is not None:
                return self.token
            response = await self.dream._client.post(
            self.urls.get("auth_key"),
                params={"key": await self._get_google_key()},
                json={"returnSecureToken": True},
                timeout=20,
            )
            result = response.json()
            _auth_token = result.get("idToken")
            self._save_token(_auth_token)
            return _auth_token

    class API(BaseDream.API):
        async def create_task(self, text: str, style: Union[int, ArtStylesModel] = 115)-> TaskModel:
            response = await self.dream._client.post(
                url=self.url,
                headers=self.dream.Utils._headers_gen(await self.dream.auth._get_auth_key()),
                json=self.dream.Utils._data_gen(text=text, style=style),
                timeout=20
            )
            response = response.json()
            model: TaskModel = self.dream.Utils._get_model(TaskModel, response)
            return model

        async def check_task(self, task_id: str) -> TaskModel:
            response = await self.dream._client.get(self.url+f"/{task_id}", timeout=10)
            response = response.json()
            model: TaskModel = self.dream.Utils._get_model(TaskModel, response)
            return model

    def __init__(self, token: str = None, *, debug: bool = False, proxy: str = None):
        super().__init__(token=token, debug=debug)
        self._client = AsyncClient(proxy=proxy) 

    async def generate(self, text: str, style: Union[int, ArtStylesModel] = 115, *, timeout: int = 60, check_for: int = 3):
        task = await self.api.create_task(text=text, style=style)
        for _ in range(timeout, 0, -check_for):
            task = await self.api.check_task(task.id)
            if task.result is not None:
                return task
            await asyncio.sleep(check_for)
        else:
            raise TimeoutError