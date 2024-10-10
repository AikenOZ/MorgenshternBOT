import telebot
from threading import Timer
import time  # Импортируем модуль времени

bot = telebot.TeleBot("Token", parse_mode="HTML")


chat_ids = "@nmrgtest"
media_group_timers = {}  # Словарь для таймеров медиагрупп
media_group_messages = {}  # Словарь для хранения message_id всех сообщений в медиагруппе
ino = "<blockquote><i>OZ - IT Premium Quality</i></blockquote>"



def add_ino_to_last_media(group_id):
    last_media_id = media_group_messages[group_id][-1]
    bot.edit_message_caption(chat_id=chat_ids, message_id=last_media_id, caption=ino)
    del media_group_timers[group_id]
    del media_group_messages[group_id]

@bot.channel_post_handler(content_types=['audio', 'animation'])
def handle_audio_animation(message):
    if message.media_group_id:
        media_group_messages.setdefault(message.media_group_id, []).append(message.message_id)
        if message.media_group_id in media_group_timers:
            media_group_timers[message.media_group_id].cancel() 
        media_group_timers[message.media_group_id] = Timer(2.0, add_ino_to_last_media, [message.media_group_id])
        media_group_timers[message.media_group_id].start()
    else:
        new_caption = message.caption or ""  # Сохраняем оригинальную подпись
        new_caption += '\n\n' + ino  # Добавляем преписку
        bot.edit_message_caption(chat_id=chat_ids, message_id=message.message_id, caption=new_caption)


@bot.channel_post_handler(content_types=['photo', 'video'])
def handle_media(message):
    if message.forward_date:
        bot.send_message(chat_ids, ino)
    else:
        new_caption = message.caption or ""  # Берем оригинальную подпись если она есть
        if message.media_group_id:
            media_group_messages.setdefault(message.media_group_id, []).append(message.message_id)
            new_caption += '\n\n' + ino  # Добавляем преписку
            bot.edit_message_caption(chat_id=chat_ids, message_id=message.message_id, caption=new_caption)
        else:
            new_caption += '\n\n' + ino
            bot.edit_message_caption(chat_id=chat_ids, message_id=message.message_id, caption=new_caption)



@bot.channel_post_handler(content_types=['text', 'document', 'sticker', 'video_note', 'voice', 'location', 'contact',
                                         'new_chat_members', 'left_chat_member', 'new_chat_title', 'new_chat_photo',
                                         'delete_chat_photo', 'group_chat_created', 'supergroup_chat_created',
                                         'channel_chat_created', 'migrate_to_chat_id', 'migrate_from_chat_id',
                                         'pinned_message'])
@bot.channel_post_handler(content_types=['text'])
def handle_text(message):
    original_text = message.text  # Получаем оригинальный текст сообщения
    new_text = f'{original_text}\n\n{ino}'  # Добавляем преписку к оригинальному тексту
    bot.edit_message_text(chat_id=chat_ids, message_id=message.message_id, text=new_text)

if __name__ == "__main__":
    while True:
        try:
            bot.polling(none_stop=True, timeout=60)  # Увеличение таймаута и запуск бота
        except Exception as e:  # Обработка любого типа исключений
            print(f"Произошла ошибка: {e}")  # Логирование ошибки
            time.sleep(10)  # Перезапуск бота после задержки в 10 секунд
