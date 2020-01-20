# imports
import os
from dotenv import load_dotenv
from os.path import join, dirname

# Get .env file
dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

install_path = os.path.abspath(dirname(__file__))

VIRK_DK_ENDPOINT = os.environ.get('VIRK_DK_ENDPOINT')
VIRK_DK_USERNAME = os.environ.get('VIRK_DK_USERNAME')
VIRK_DK_PASSWORD = os.environ.get('VIRK_DK_PASSWORD')
INPUT_FILE = os.environ.get('INPUT_FILE')