import os

import dotenv

from modules.is_toxic import IsToxic

dotenv.load_dotenv()

TOKEN = os.getenv('TOKEN')

isToxic = IsToxic(0.5)
