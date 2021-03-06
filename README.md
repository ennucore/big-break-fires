# Модель тушения пожаров с воздуха

Эта программа - модель пожара и дронов для его тушения.

## Примеры видео

"Победа": огонь сведен на нет:

![https://github.com/ennucore/big-break-fires/raw/master/win.gif](https://github.com/ennucore/big-break-fires/raw/master/win.gif)

"Проигрыш": огонь распространился:

![https://github.com/ennucore/big-break-fires/raw/master/losing.gif](https://github.com/ennucore/big-break-fires/raw/master/losing.gif)

"Ничья": установилось равновесие:

![https://github.com/ennucore/big-break-fires/raw/master/stasis.gif](https://github.com/ennucore/big-break-fires/raw/master/stasis.gif)

## Установка

Чтобы скачать репозиторий, сделайте `git clone https://github.com/ennucore/big-break-fires`
Для начала, вам нужно установить зависимости: программу ffmpeg и python-библиотеки
Установка библиотек:
`pip install python-opencv numpy`
Если у вас операционная система Linux, ffmpeg можно установить вот так:
Для Ubuntu/Debian: `sudo apt install ffmpeg`
Для Arch linux/Manjaro: `sudo pacman -S ffmpeg`
Если у вас Windows, ffmpeg вы можете скачать с оффициального сайта.

#### Запуск

Вы можете подредактировать параметры модели в файле `settings.py`

После этого запустите модель:

`python main.py`

После этого запустите визуализацию:

`python visualize.py` (Если оставлять имена файлов пустыми, то программа возьмет имена по умолчанию)

Видео будет находиться в файле `output.mp4`
