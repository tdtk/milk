from os.path import join, dirname
from dotenv import load_dotenv
import os


def load(path='.env'):
  load_dotenv(verbose=True)
  dotenv_path = join(dirname(__file__), path)
  load_dotenv(dotenv_path)
