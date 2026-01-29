"""
Service TrustMark pour le watermark invisible.
TrustMark est une composante essentielle du système de protection.
"""

from PIL import Image
from typing import Optional
import logging

logger = logging.getLogger(__name__)

# Initialisation de TrustMark
TRUSTMARK_AVAILABLE = False
_trustmark_instance = None

try:
    from trustmark import TrustMark
    _trustmark_instance = TrustMark(verbose=False, model_type='Q')
    TRUSTMARK_AVAILABLE = True
    logger.info("TrustMark initialisé avec succès")
except ImportError:
    logger.error("ERREUR: TrustMark non installé. Installez-le avec: pip install trustmark")
except Exception as e:
    logger.error(f"Erreur initialisation TrustMark: {e}")


class TrustMarkService:
    """Service pour appliquer le watermark invisible TrustMark."""
    
    @staticmethod
    def is_available() -> bool:
        """Vérifie si TrustMark est disponible."""
        return TRUSTMARK_AVAILABLE
    
    @staticmethod
    def apply_watermark(
        image: Image.Image,
        secret_message: Optional[str] = None
    ) -> Image.Image:
        """
        Applique le watermark invisible TrustMark sur l'image.
        
        Note: TrustMark est requis pour la protection complète.
        Sans TrustMark, l'image est retournée sans encodage invisible.
        """
        if not TRUSTMARK_AVAILABLE or _trustmark_instance is None:
            logger.warning("TrustMark non disponible - protection invisible désactivée")
            return image
        
        if secret_message is None:
            from utils.constants import DEFAULT_TRUSTMARK_SECRET
            secret_message = DEFAULT_TRUSTMARK_SECRET
        
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            watermarked = _trustmark_instance.encode(image, secret_message)
            logger.info("TrustMark encodé avec succès")
            return watermarked
        except Exception as e:
            logger.error(f"Erreur encodage TrustMark: {e}")
            return image
    
    @staticmethod
    def decode_watermark(image: Image.Image) -> Optional[str]:
        """
        Décode le message TrustMark d'une image.
        
        Returns:
            Le message décodé ou None si échec
        """
        if not TRUSTMARK_AVAILABLE or _trustmark_instance is None:
            return None
        
        try:
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            decoded = _trustmark_instance.decode(image)
            return decoded
        except Exception as e:
            logger.error(f"Erreur décodage TrustMark: {e}")
            return None
