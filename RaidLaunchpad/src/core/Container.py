import os
from src.core.Tokens import Tokens

tokens = Tokens()

pc_roaming = os.getenv('APPDATA')
pc_local = os.getenv('LOCALAPPDATA')
