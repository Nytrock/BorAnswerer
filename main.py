import requests
import json
import time

with open('config.json') as file:
    config = json.load(file)

API_URL: str = 'https://api.telegram.org/bot'
BOT_TOKEN: str = config['BOT_TOKEN']
MAX_COUNTER: int = 100

offset: int = -2
counter: int = 0
chat_id: int
text: str

while counter < MAX_COUNTER:
    print('attempt =', counter)

    updates: dict = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']

            if 'sticker' in result['message']:
                stickerpack: str = result['message']['sticker']['set_name']
                height: int = result['message']['sticker']['height']
                width: int = result['message']['sticker']['width']
                emoji: str = result['message']['sticker']['emoji']
                animated: str = 'анимирован'
                if not result['message']['sticker']['is_animated']:
                    animated = 'не ' + animated
                video: str = 'видео'
                if not result['message']['sticker']['is_video']:
                    video = 'не ' + video
                text = f'Вы отправили мне стикер из стикерпака {stickerpack}. Его размеры {width}x{height}. ' \
                       f'Он обозначает смайлик {emoji}. Он {animated} и это {video}.'
            elif 'voice' in result['message']:
                seconds: int = result['message']['voice']['duration']
                hour: int = seconds // 3600
                minutes: int = seconds % 3600 // 60
                seconds %= 60
                text = 'Вы прислали мне войс длиной '
                if hour == 0:
                    text += f'{minutes:02}:{seconds:02}'
                else:
                    text += f'{hour:02}:{minutes:02}:{seconds:02}'
            else:
                text = "Вы прислали мне сообщение. Спасибо."
            requests.get(f'{API_URL}{BOT_TOKEN}/sendMessage?chat_id={chat_id}&text={text}')
    time.sleep(1)
    counter += 1
