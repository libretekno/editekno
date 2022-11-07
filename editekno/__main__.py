import logging
import asyncio

from aiogram import Bot, Dispatcher, executor
from aiogram.utils import exceptions

from editekno import (
  API_TOKEN, ALLOWED_TYPES, CHANNEL, CAPTION,
  PORT,  WEBHOOK_PATH, WEBHOOK_URL, HOST
)

logger = logging.getLogger(__name__)

bot = Bot(token=API_TOKEN)
dispatcher = Dispatcher(bot)


async def edit_message(message_id):
    try:
        await bot.edit_message_caption(
            chat_id=CHANNEL,
            message_id=message_id,
            caption=CAPTION
        )
    except exceptions.MessageNotModified:
        logger.error(f'Message with ID: {message_id!r} caption equals {CAPTION}.')
    except exceptions.MessageIdInvalid:
        logger.error(f'Message with ID: {message_id!r} not found.')
    except exceptions.RetryAfter as exc:
        logger.error(f'Flood limit is exceeded on ID: {message_id!r}. Sleep {exc.timeout} seconds.')
        await asyncio.sleep(exc.timeout)
        await edit_message(message_id)


async def channel_message_handler(message):
    await edit_message(message.message_id)


dispatcher.register_channel_post_handler(
  channel_message_handler,
  lambda m: hasattr(m, 'caption') and m.caption != CAPTION,
  chat_id=CHANNEL,
  is_forwarded=False,
  content_types=ALLOWED_TYPES
)

async def on_startup(dispatcher):
    await bot.set_webhook(WEBHOOK_URL)


executor.start_webhook(
  dispatcher=dispatcher,
  webhook_path=WEBHOOK_PATH,
  on_startup=on_startup,
  host=HOST,
  port=PORT,
)
