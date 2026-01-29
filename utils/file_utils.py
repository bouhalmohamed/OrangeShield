"""
Utilitaires pour la gestion des fichiers.
"""

from werkzeug.utils import secure_filename
from config import Config


def is_allowed_file(filename: str) -> bool:
    """Vérifie si l'extension du fichier est autorisée."""
    if not filename or '.' not in filename:
        return False
    extension = filename.rsplit('.', 1)[1].lower()
    return extension in Config.ALLOWED_EXTENSIONS


def secure_file_path(filename: str) -> str:
    """Génère un nom de fichier sécurisé."""
    return secure_filename(filename)
