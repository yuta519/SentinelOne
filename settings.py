# coding: UTF-8
import os
from os.path import join, dirname
from dotenv import load_dotenv

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

# plug environment variables
url      = os.environ.get("url")
username = os.environ.get("username")
password = os.environ.get("password")