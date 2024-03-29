# Style Transfer Telegram Bot

Телеграм бот для переноса стиля. 

## Команды бота:
- /start: команда для начала общения с ботом, при получении которой бот отвечает 
          
          "Привет! Я, ImageBot, умею переносить стиль одной картинки на другую. 
          Для общения со мной используй данные команды: 
          /help - получить инструкции 
          /style_transfer - начать обработку изображений 
          /cancel - отменить все."

- /help: команда для вызова помощи, при получении которой бот отвечает

          "Для общения со мной используй данные команды: 
          /help - получить инструкции
          /style_transfer - начать обработку изображений
          /cancel - отменить все."
          
- /style_transfer: команда запускающая процесс по переносу стиля со сменой текущих состояний, при получении которой бот запрашивает сначала картинку style, после чего картинку content, а затем запускает процесс обработки картинок

          "Запущен перенос стиля.
          Для отмены отправь команду /cancel."
          
          "Отправь картинку стиля."
          style_img (1)
          
          "Отправь картинку для переноса стиля."
          content_img (1)
          
          "Начинаю обработку. На это потребуется некоторое время."
          ...
          "Обработка завершена."
          output_img
          
          "Для запуска переноса стиля отправь /style_transfer."
          
- /cancel: команда для выхода из процесса по переносу стиля, при получении которой бот сбрасывает текущее состояние и отвечает

          "Процесс переноса стиля отменен. 
          Для запуска отправь /style_transfer."
          
- (1) на данных этапах предусмотрена защита от дурака: если пользователь присылает не фото, состояние не меняется, а бот отвечает

          "Что-то пошло не так. Попробуй отправить картинку стиля снова или отправь для отмены /cancel."
          
- на любые другие сообщения бот отвечает

          "Я тебя не понимаю.
          Воспользуйся /help."

## Пример работы
| Style | Content | Output |
| --- | --- | --- |
| <img src="https://github.com/ArinaOwl/NST_tgbot/blob/master/images/style.jpg" width="300" /> | <img src="https://github.com/ArinaOwl/NST_tgbot/blob/master/images/content.jpg" width="300" /> | <img src="https://github.com/ArinaOwl/NST_tgbot/blob/master/images/output.jpg" width="300" /> |

## Реализация 
Для удобства использования хэндлеры разбиты по файлам, собранным в каталоге handlers. Основные хендлеры для обработки команд /start и /help реализованы в файле [general_commands.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/handlers/general_commands.py), обработка любых других сообщений реализована в файле [default_handler.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/handlers/default_handler.py).

Хэндлеры переноса стиля реализованы в файле [style_transfer_handler.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/handlers/style_transfer_handler.py). Диалог построен при помощи механизма конечных автоматов, встроенного в aiogram с поддержкой хранилища MemeoryStorage(). В нем используются два состояния:

          - waiting_for_style_img: состояние ожидания картинки style
          - waiting_for_content_img: состояние ожидания картинки content
          
Картинки сохраняются в каталоге images/.

Модель NST реализована в виде класса в файле [model.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/model.py). Вспомогательные функции для нее реализованы в файле [utils.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/utils.py).

В файле [misc.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/misc.py) объявляется бот, а файл [bot.py](https://github.com/ArinaOwl/NST_tgbot/blob/master/bot.py) служит точкой входа.
