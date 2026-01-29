"""
Configuration de l'application OrangeShield.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).parent


class Config:
    """Paramètres de configuration."""
    
    # File upload settings
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max
    UPLOAD_FOLDER = BASE_DIR / 'uploads'
    OUTPUT_FOLDER = BASE_DIR / 'outputs'
    
    # Allowed file extensions
    ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp'}
    
    # Image processing settings
    JPEG_QUALITY = 95
    
    # TrustMark settings
    TRUSTMARK_VERBOSE = False
    TRUSTMARK_MODEL_TYPE = 'Q'
    
    @staticmethod
    def init_app(app):
        """Initialize application with configuration."""
        # Create necessary directories
        os.makedirs(Config.UPLOAD_FOLDER, exist_ok=True)
        os.makedirs(Config.OUTPUT_FOLDER, exist_ok=True)
        
        # Set Flask config
        app.config['MAX_CONTENT_LENGTH'] = Config.MAX_CONTENT_LENGTH
        app.config['UPLOAD_FOLDER'] = str(Config.UPLOAD_FOLDER)
        app.config['OUTPUT_FOLDER'] = str(Config.OUTPUT_FOLDER)
