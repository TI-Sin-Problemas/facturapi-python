"""Tests settings"""
import os
from dotenv import load_dotenv

load_dotenv()

FACTURAPI_KEY = os.getenv("FACTURAPI_KEY")
