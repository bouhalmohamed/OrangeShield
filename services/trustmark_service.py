"""
Service TrustMark pour le watermark invisible.
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
except ImportError:
    logger.warning("TrustMark non disponible - watermark invisible désactivé")
except Exception as e:
    logger.warning(f"Erreur init TrustMark: {e}")


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
        """Applique le watermark invisible TrustMark sur l'image."""
        if not TRUSTMARK_AVAILABLE or _trustmark_instance is None:
            return image
        
        if secret_message is None:
            from utils.constants import DEFAULT_TRUSTMARK_SECRET
            secret_message = DEFAULT_TRUSTMARK_SECRET
        
        try:
            # TrustMark expects RGB PIL Image
            if image.mode != 'RGB':
                image = image.convert('RGB')
            
            # Encode secret message
            watermarked = _trustmark_instance.encode(image, secret_message)
            return watermarked
        except Exception as e:
            logger.error(f"TrustMark encoding failed: {e}")
            return image
