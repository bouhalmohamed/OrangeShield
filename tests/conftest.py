"""
Pytest configuration and shared fixtures.
"""

import pytest
import os
import tempfile
import shutil
from PIL import Image
from io import BytesIO
from flask import Flask
from app import create_app
from config import Config


@pytest.fixture
def temp_dirs():
    """Create temporary directories for uploads and outputs."""
    upload_dir = tempfile.mkdtemp()
    output_dir = tempfile.mkdtemp()
    
    yield {
        'upload': upload_dir,
        'output': output_dir
    }
    
    # Cleanup
    shutil.rmtree(upload_dir, ignore_errors=True)
    shutil.rmtree(output_dir, ignore_errors=True)


@pytest.fixture
def test_image():
    """Create a test PIL Image."""
    img = Image.new('RGB', (100, 100), color='red')
    return img


@pytest.fixture
def test_image_bytes():
    """Create test image as bytes."""
    img = Image.new('RGB', (100, 100), color='blue')
    img_bytes = BytesIO()
    img.save(img_bytes, format='JPEG')
    img_bytes.seek(0)
    return img_bytes.getvalue()


@pytest.fixture
def sample_image_file(test_image_bytes):
    """Create a file-like object with image data."""
    return BytesIO(test_image_bytes)


@pytest.fixture
def app(temp_dirs):
    """Create Flask application for testing."""
    # Override config with temp directories
    class TestConfig(Config):
        UPLOAD_FOLDER = temp_dirs['upload']
        OUTPUT_FOLDER = temp_dirs['output']
    
    app = create_app(TestConfig)
    app.config['TESTING'] = True
    app.config['WTF_CSRF_ENABLED'] = False
    
    return app


@pytest.fixture
def client(app):
    """Create Flask test client."""
    return app.test_client()


@pytest.fixture
def runner(app):
    """Create Flask CLI test runner."""
    return app.test_cli_runner()
