# Style Transfer Telegram Bot

Телеграм бот для переноса стиля. Основной функционал:
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
          
