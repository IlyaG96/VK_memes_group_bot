# VK_memes_group_bot
Скрипт для скачивания мемчиков с сайта https://xkcd.com и отправки их в группу ВК
## Установка
Вам понадобится установленный Python 3.6-3.9 и git.

Склонируйте репозиторий или скачайте архив с кодом на компьютер:
```bash
$ git clone git@github.com:IlyaG96/VK_memes_group_bot.git
```
Создайте в этой папке виртуальное окружение:
```bash
$ python3 -m venv [полный путь до папки VK_memes_group_bot без квадратных скобочек] env
```
Активируйте виртуальное окружение и установите зависимости:
```bash
$ cd VK_memes_group_bot
$ source env/bin/activate
$ pip install -r requirements.txt
```
## Использование
- Заполните прилагающийся .env.exapmle файл и переименуйте его в .env или иным образом задайте переменные среды

```bash
PHOTO_PATH="/full/path/to/photos"
VK_TOKEN="dbc6a74qwerqewr222aasdasdasd337966d234cqr44qdc3f0d2af87rq4cqr4237fdb"
APP_ID="1144560"
VK_USER_ID="your_user_id"
VK_GROUP_ID="your_group_id"
VK_API_VERSION="5.131"
```
`APP_ID` - Создайте приложение ВК [здесь](https://dev.vk.com)

- В качестве типа приложения следует указать standalone — это подходящий тип для приложений, которые просто запускаются на компьютере.

`VK_TOKEN` - получать [тут](https://dev.vk.com/api/access-token/implicit-flow-user)  
`VK_USER_ID` - ваш user_id (vk.com/user_id)  
`VK_GROUP_ID` - id группы вк (vk.com/public<group_id>) при переходе в группу  
`VK_API_VERSION` - версия API вк.

- Затем создайте группу в [ВК](https://vk.com/groups), в которой планируете размещать картинки


Простейший способ скачать случайный мемес с сайта и разместить его на стене в группе -
```bash
$ python main.py
```

