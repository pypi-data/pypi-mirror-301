<h1 align="center">Привет! Меня зовут</h1>


<a href="https://gitverse.ru/cumproject/wombo" target="_blank">
  <img src="https://upload.wikimedia.org/wikipedia/commons/d/d7/WomboLogo.svg"/>
</a>

### Я модуль для dream.ai компании wombo (нейронной сети для генерации изображений)

```Проект придерживается ZeroVer, поэтому может ломаться обратная совместимость, + компания wombo может изменять api по своему усмотрению, что тоже может всё сломать, используйте для ботов на свои сервера например. Но относительно всегда всё остаётся одинаковым. Так же я задолбался писать на английском, поэтому отныне, придерживаюсь везде русской документации```

<details>
   <summary style="font-size: 24px; font-weight: bold;">Сборка</summary>
    Для сборки использовался poetry, в gigaIDE cloud, со следующими коммандами:
    
    python3 -m poetry config repositories.gitverse https://gitverse.ru/api/packages/cumproject/pypi

    python3 -m poetry config pypi-token.gitverse <my-project-token>

    python3 -m poetry publish -r gitverse --build


</details>


<details>
   <summary style="font-size: 24px; font-weight: bold;">Документация</summary>
    <details>
      <summary style="font-size: 24px; font-weight: bold;">Базовое использование</summary>
      <pre>
from wombo import Dream, AsyncDream
dream = Dream()
dream.generate(text, style)
      </pre>
    </details>
    <details>
      <summary style="font-size: 24px; font-weight: bold;">Стили</summary>
     <pre>
from wombo.models import StyleModel, ArtStylesModel
dream.style._get_styles() -> StyleModel
dream.style["style.name"] -> ArtStylesModel
      </pre>
    </details>
    <details>
      <summary style="font-size: 24px; font-weight: bold;">API</summary>
      <pre>
from wombo.models import TaskModel
dream.api.create_task(text: str, style: int | ArtStylesModel) -> TaskModel
dream.api.check_task(task_id: str) -> TaskModel
      </pre>
    </details>
</details>


