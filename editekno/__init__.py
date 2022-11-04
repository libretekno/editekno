import os
import logging

logging.basicConfig(
  level=logging.DEBUG,
  format='%(asctime)s - %(levelname)s - %(filename)s:%(lineno)d -> %(message)s'
)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

logging.getLogger('aiogram').setLevel(logging.WARNING)

ALLOWED_TYPES = ['audio', 'document', 'photo']

try:
    API_TOKEN = os.environ['API_TOKEN']
    CHANNEL = os.environ['CHANNEL']
    CAPTION = os.environ['CAPTION']
    PORT = int(os.environ['PORT'])
except KeyError as exc:
    logger.error(f'{ exc } environment variables are missing!')
    raise SystemExit(1)

if 'RENDER' in os.environ:
    WEBHOOK_HOST = f'https://{os.environ["RENDER_EXTERNAL_HOSTNAME"]}'
elif 'DYNO' in os.environ:
    WEBHOOK_HOST = f'https://{os.environ["APP_NAME"]}.herokuapp.com'
else:
    logger.error('No runtime environment found!')
    raise SystemExit(1)

WEBHOOK_PATH = f'/bot/{API_TOKEN}'
WEBHOOK_URL = f'{WEBHOOK_HOST}{WEBHOOK_PATH}'
HOST = '0.0.0.0'
