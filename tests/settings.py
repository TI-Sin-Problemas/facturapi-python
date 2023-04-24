"""Tests settings"""
import os

try:
    import dotenv

    dotenv.load_dotenv()
except ModuleNotFoundError:
    pass

API_KEY = os.getenv("FACTURAPI_API_KEY")
