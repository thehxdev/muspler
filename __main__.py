import os
import logging
import ffmpeg
import random as rand
import config as conf
from telegram import Update
from telegram.ext import (
    filters,
    MessageHandler,
    ApplicationBuilder,
    ContextTypes,
    CommandHandler
)


# Your telegram bot token
BOT_TOKEN = conf.BOT_TOKEN

# Where to download audio files and process them.
# It MUST be a directory
DIR_PREFIX = conf.DIR_PREFIX

SAMPLE_DURATION = 30
FINAL_AUDIO_BITRATE = 96


logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.WARN
)



async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg: str = 'This bot can make samples from your music and audio files! Just send me an audio file.'
    chat_id: int = update.effective_chat.id
    await context.bot.send_message(chat_id=chat_id, text=msg)



async def ffmpeg_make_sample(input_path: str,
                             output_path:str,
                             duration: int) -> None:
    start = (0) if duration == 0 else rand.randint(0, duration - SAMPLE_DURATION) 
    audio_input = ffmpeg.input(input_path)
    audio_cut = audio_input.audio.filter('atrim', start=start, end=start + SAMPLE_DURATION)
    audio_output = ffmpeg.output(audio_cut,
                                 output_path,
                                 **{'b:a': f'{FINAL_AUDIO_BITRATE}k'}).overwrite_output()
    ffmpeg.run(audio_output, quiet=True)


def remove_file(path: str) -> None:
    if (os.path.exists(path)):
        os.remove(path)


async def audio_sample_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    bot = context.bot
    chat_id = update.effective_chat.id
    msg = update.effective_message
    file_name = msg.effective_attachment.file_name
    input_path = f'{DIR_PREFIX}/{file_name}'
    output_path = f'{DIR_PREFIX}/new_{file_name}'

    m = await msg.reply_text(text='Downloading file on server...',
                             reply_to_message_id=msg.id)

    try:
        audio_file = await msg.audio.get_file()
        await audio_file.download_to_drive(input_path)

        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=m.id,
                                    text='Trimig audio file...')

        await ffmpeg_make_sample(input_path, output_path, msg.audio.duration)

        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=m.id,
                                    text='Sending sample audio...')

        await msg.reply_voice(voice=output_path,
                              reply_to_message_id=msg.id,
                              caption=msg.audio.title)

        await m.delete()
    except:
        await bot.edit_message_text(chat_id=chat_id,
                                    message_id=m.id,
                                    text='Creating sample failed!')
    finally:
        remove_file(input_path)
        remove_file(output_path)



if __name__ == '__main__':
    application = ApplicationBuilder().token(BOT_TOKEN).build()

    application.add_handler(CommandHandler('start', start))

    application.add_handler(MessageHandler(filters.AUDIO & (~filters.COMMAND),
                                           audio_sample_handler, block=False))

    application.run_polling()
