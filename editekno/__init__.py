import os
import logging
import pathlib

logging.basicConfig(level=logging.DEBUG)

formatter = logging.Formatter(
  '%(asctime)s - [%(levelname)s] - Line №(%(lineno)d) -> %(message)s'
)

PATH = pathlib.Path(__file__).parent.parent / 'logs' / (__name__ + '.log')

fh = logging.FileHandler(PATH, 'w')
fh.setFormatter(formatter)
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setFormatter(formatter)
ch.setLevel(logging.DEBUG)

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(fh)
logger.addHandler(ch)

aiogram_logger = logging.getLogger('aiogram')
aiogram_logger.setLevel(logging.WARNING)
aiogram_logger.addHandler(ch)
aiogram_logger.addHandler(fh)


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
