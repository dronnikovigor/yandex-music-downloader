# yandex-music-downloader

> Внимание! В версии v3 был изменен способ авторизации и некоторые
> аргументы. Смотрите [MIGRATION.md](MIGRATION.md) для получения информации
> об изменениях

## Содержание
1. [Python API](#python-api)
   - [Установка](#установка)
   - [Быстрый старт](#быстрый-старт)
   - [Документация API](#документация-api)
2. [CLI](#cli)
   - [О программе](#о-программе)
   - [Установка](#установка-1)
   - [Получение данных для авторизации](#получение-данных-для-авторизации)
   - [Примеры использования](#примеры-использования)
   - [Использование](#использование)
   - [Уровни совместимости](#уровни-совместимости)
3. [Спасибо](#спасибо)
4. [Дисклеймер](#дисклеймер)

## Python API

### Установка

```bash
pip install -U git+https://github.com/yourusername/yandex-music-downloader.git
```

### Быстрый старт

```python
from ymd import YandexMusicDownloader, CoreTrackQuality, LyricsFormat

# Инициализация с вашим OAuth токеном
downloader = YandexMusicDownloader("ваш_oauth_токен")

# Скачать трек по ID или URL
downloader.download_track(
    track_id="12345678",  # или URL вида "https://music.yandex.ru/album/12345678/track/7654321"
    output_dir="./downloads",
    quality=CoreTrackQuality.NORMAL,
    lyrics_format=LyricsFormat.TEXT,
    embed_cover=True
)

# Скачать альбом по ID или URL
downloader.download_album(
    album_id="87654321",  # или URL
    output_dir="./downloads/albums",
    quality=CoreTrackQuality.NORMAL
)

# Скачать плейлист по ID пользователя и ID плейлиста (или URL)
downloader.download_playlist(
    user_id="username",
    playlist_id="1234",  # или URL
    output_dir="./downloads/playlists"
)
```

### Документация API

#### `YandexMusicDownloader(token, timeout=10, max_retries=3, retry_delay=5)`
Основной класс для загрузки музыки с Яндекс.Музыки.

**Параметры:**
- `token` (str): OAuth токен для доступа к API Яндекс.Музыки
- `timeout` (int, optional): Таймаут запросов в секундах. По умолчанию 10
- `max_retries` (int, optional): Максимальное количество попыток при ошибках. По умолчанию 3
- `retry_delay` (int, optional): Задержка между попытками в секундах. По умолчанию 5

#### Методы

##### `download_track(track_id, output_dir, quality=CoreTrackQuality.NORMAL, lyrics_format=LyricsFormat.NONE, embed_cover=True, cover_resolution=800, compatibility_level=1)`
Загружает один трек.

**Параметры:**
- `track_id` (str, int): ID трека или URL
- `output_dir` (str, Path): Директория для сохранения
- `quality` (CoreTrackQuality): Качество аудио (LOW, NORMAL, LOSSLESS)
- `lyrics_format` (LyricsFormat): Формат текста песни (NONE, TEXT, LRC)
- `embed_cover` (bool): Встраивать ли обложку в файл
- `cover_resolution` (int): Разрешение обложки
- `compatibility_level` (int): Уровень совместимости тегов (1-3)

**Возвращает:**
- Path: Путь к сохраненному файлу

##### `download_album(album_id, output_dir, quality=CoreTrackQuality.NORMAL, lyrics_format=LyricsFormat.NONE, embed_cover=True, cover_resolution=800, compatibility_level=1)`
Загружает все треки из альбома.

**Параметры:**
- `album_id` (str, int): ID альбома или URL
- `output_dir` (str, Path): Базовая директория для сохранения
- Остальные параметры аналогичны `download_track`

**Возвращает:**
- List[Path]: Список путей к сохраненным файлам

##### `download_playlist(user_id, playlist_id, output_dir, quality=CoreTrackQuality.NORMAL, lyrics_format=LyricsFormat.NONE, embed_cover=True, cover_resolution=800, compatibility_level=1)`
Загружает все треки из плейлиста.

**Параметры:**
- `user_id` (str): ID пользователя (если не указан в URL)
- `playlist_id` (str, int): ID плейлиста или URL
- `output_dir` (str, Path): Базовая директория для сохранения
- Остальные параметры аналогичны `download_track`

**Возвращает:**
- List[Path]: Список путей к сохраненным файлам

#### Константы

##### `CoreTrackQuality`
- `LOW`: Низкое качество (AAC 64kbps)
- `NORMAL`: Обычное качество (AAC 192kbps)
- `LOSSLESS`: Без потерь (FLAC)

##### `LyricsFormat`
- `NONE`: Не загружать текст
- `TEXT`: Обычный текст
- `LRC`: Синхронизированный текст (LRC формат)

## CLI

## О программе
Загрузчик, созданный вследствие наличия *фатального недостатка* в проекте [yandex-music-download](https://github.com/kaimi-io/yandex-music-download).

### Возможности
- Возможность загрузки:
    - Всех треков исполнителя
    - Всех треков из альбома
    - Всех треков из плейлиста
    - Отдельного трека
- Загрузка всех метаданных трека/альбома:
    - Номер трека
    - Номер диска
    - Название трека
    - Исполнитель
    - Дополнительные исполнители
    - Дата выпуска альбома
    - Обложка альбома
    - Название альбома
    - Текст песни (при использовании флага `--add-lyrics`)
- Загрузка треков в lossless качестве
- Поддержка паттерна для пути сохранения музыки

## Установка
Для запуска скрипта требуется Python 3.9+
```
pip install -U https://github.com/llistochek/yandex-music-downloader/archive/main.zip
yandex-music-downloader --help
```

## Получение данных для авторизации
https://yandex-music.readthedocs.io/en/main/token.html

## Примеры использования
Во всех примерах замените `<Токен>` на ваш токен.

### Скачать все треки [Arctic Monkeys](https://music.yandex.ru/artist/208167) в наилучшем качестве
```
yandex-music-downloader --token "<Токен>" --quality 2 --url "https://music.yandex.ru/artist/208167"
```

### Скачать альбом [Nevermind](https://music.yandex.ru/album/294912) в высоком качестве, загружая тексты песен в формате LRC (с временными метками)
```
yandex-music-downloader --token "<Токен>" --quality 1 --lyrics-format lrc --url "https://music.yandex.ru/album/294912"
```

### Скачать трек [Seven Nation Army](https://music.yandex.ru/album/11644078/track/6705392)
```
yandex-music-downloader --token "<Токен>" --url "https://music.yandex.ru/album/11644078/track/6705392"
```

## Использование
```
usage: yandex-music-downloader [-h] [--quality <Качество>] [--skip-existing]
                               [--lyrics-format {none,text,lrc}]
                               [--embed-cover]
                               [--cover-resolution <Разрешение обложки>]
                               [--delay <Задержка>] [--stick-to-artist]
                               [--only-music]
                               [--compatibility-level <Уровень совместимости>]
                               [--timeout <Время ожидания>]
                               [--tries <Количество попыток>]
                               [--retry-delay <Задержка>]
                               (--artist-id <ID исполнителя> | --album-id <ID альбома> | --track-id <ID трека> | --playlist-id <владелец плейлиста>/<тип плейлиста> | -u URL)
                               [--unsafe-path] [--dir <Папка>]
                               [--path-pattern <Паттерн>] --token <Токен>

Загрузчик музыки с сервиса Яндекс.Музыка

options:
  -h, --help            show this help message and exit

Общие параметры:
  --quality <Качество>  Качество трека:
                        0 - Низкое (AAC 64kbps)
                        1 - Оптимальное (AAC 192kbps)
                        2 - Лучшее (FLAC)
                        (по умолчанию: 0)
  --skip-existing       Пропускать уже загруженные треки
  --lyrics-format {none,text,lrc}
                        Формат текста песни (по умолчанию: none)
  --embed-cover         Встраивать обложку в аудиофайл
  --cover-resolution <Разрешение обложки>
                        Разрешение обложки (в пикселях). Передайте "original" для загрузки в оригинальном (наилучшем) разрешении (по умолчанию: 400)
  --delay <Задержка>    Задержка между запросами, в секундах (по умолчанию: 0)
  --stick-to-artist     Загружать альбомы, созданные только данным исполнителем
  --only-music          Загружать только музыкальные альбомы (пропускать подкасты и аудиокниги)
  --compatibility-level <Уровень совместимости>
                        Уровень совместимости, от 0 до 1. См. README для подробного описания (по умолчанию: 1)

Сетевые параметры:
  --timeout <Время ожидания>
                        Время ожидания ответа от сервера, в секундах. Увеличьте если возникают сетевые ошибки (по умолчанию: 20)
  --tries <Количество попыток>
                        Количество попыток при возникновении сетевых ошибок. 0 - бесконечное количество попыток (по умолчанию: 20)
  --retry-delay <Задержка>
                        Задержка между повторными запросами при сетевых ошибках (по умолчанию: 5)

ID:
  --artist-id <ID исполнителя>
  --album-id <ID альбома>
  --track-id <ID трека>
  --playlist-id <владелец плейлиста>/<тип плейлиста>
  -u URL, --url URL     URL исполнителя/альбома/трека/плейлиста

Указание пути:
  --unsafe-path         Не очищать путь от недопустимых символов
  --dir <Папка>         Папка для загрузки музыки (по умолчанию: .)
  --path-pattern <Паттерн>
                        Поддерживает следующие заполнители: #number, #track-artist, #album-artist, #title, #album, #year, #artist-id, #album-id, #track-id, #number-padded (по умолчанию: #album-artist/#album/#number - #title)

Авторизация:
  --token <Токен>       Токен для авторизации. См. README для способов получения
```

## Уровни совместимости
Уровень совместимости позволяет отойти от стандарта тегов, которого
придерживается библиотека mutagen. Сделано это для поддержки большего
количества музыкальных плееров. Ниже подробно описаны все уровни.

### 0
Стандартные теги mutagen.

### 1
Затрагиваемые форматы: `m4a`

- Теги с несколькими значениями (`\xa9ART` и `aART`) устанвливаются с
разделителем `;`. Пример: `Artist1; Artist2; Artist3`


## Спасибо
- Разработчикам проекта [yandex-music-api](https://github.com/MarshalX/yandex-music-api)
- @ArtemBay за [скрипт](https://github.com/MarshalX/yandex-music-api/issues/656#issuecomment-2306542725) получения ссылки на загрузку в lossless качестве
- @keltecc за [метод дешифрования файлов](https://github.com/llistochek/yandex-music-downloader/issues/112#issuecomment-2812535100)
- @leowerd за [корректные имена исполнителей](https://github.com/llistochek/yandex-music-downloader/issues/93#issuecomment-2960210879) при загрузке сборников


## Дисклеймер
Данный проект является независимой разработкой и никак не связан с компанией Яндекс.
