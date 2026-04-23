import pytest
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def test_config_loads():
    from config import GROQ_MODEL
    assert GROQ_MODEL == 'llama-3.3-70b-versatile'

def test_app_starts():
    from web import app
    assert app is not None
    assert app.name == 'web'