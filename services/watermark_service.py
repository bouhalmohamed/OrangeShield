"""
Service de watermarking - coordonne l'application des watermarks visible, invisible et motif zèbre.
"""

from PIL import Image
from typing import Optional
from models.image_processor import ImageProcessor
from services.trustmark_service import TrustMarkService
from services.zebra_service import ZebraService
from utils.constants import (
    DEFAULT_WATERMARK_PAYLOAD,
    DEFAULT_STEERING_PROMPT,
    DEFAULT_TRUSTMARK_SECRET,
    ZEBRA_GRID_SPACING,
    ZEBRA_SIZE,
    ZEBRA_OPACITY
)


class WatermarkService:
    """Service pour appliquer la protection triple : visible + zèbre + TrustMark."""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.trustmark_service = TrustMarkService()
        self.zebra_service = ZebraService()
    
    def apply_full_protection(
        self,
        input_image: Image.Image,
        watermark_text: Optional[str] = None,
        steering_prompt: Optional[str] = None,
        trustmark_secret: Optional[str] = None,
        enable_zebra: bool = True,
        zebra_spacing: int = ZEBRA_GRID_SPACING,
        zebra_size: int = ZEBRA_SIZE,
        zebra_opacity: float = ZEBRA_OPACITY
    ) -> Image.Image:
        """
        Applique la protection complète sur l'image :
        1. Motif de zèbres (confusion sémantique)
        2. Watermark visible avec semantic steering
        3. TrustMark invisible (encodage)
        """
        if watermark_text is None:
            watermark_text = DEFAULT_WATERMARK_PAYLOAD
        if steering_prompt is None:
            steering_prompt = DEFAULT_STEERING_PROMPT
        if trustmark_secret is None:
            trustmark_secret = DEFAULT_TRUSTMARK_SECRET
        
        result = input_image
        
        # Étape 1: Appliquer le motif de zèbres
        if enable_zebra and self.zebra_service.is_available():
            result = self.zebra_service.apply_zebra_pattern(
                result,
                grid_spacing=zebra_spacing,
                zebra_size=zebra_size,
                opacity_multiplier=zebra_opacity
            )
        
        # Étape 2: Appliquer le watermark visible avec semantic steering
        result = self.image_processor.apply_semantic_steering_watermark(
            result,
            watermark_text=watermark_text,
            steering_prompt=steering_prompt
        )
        
        # Étape 3: Appliquer TrustMark (obligatoire)
        result = self.trustmark_service.apply_watermark(
            result,
            secret_message=trustmark_secret
        )
        
        return result
    
    # Alias pour compatibilité
    def apply_dual_watermark(
        self,
        input_image: Image.Image,
        watermark_text: Optional[str] = None,
        steering_prompt: Optional[str] = None,
        trustmark_secret: Optional[str] = None
    ) -> Image.Image:
        """Alias pour apply_full_protection (compatibilité)."""
        return self.apply_full_protection(
            input_image,
            watermark_text=watermark_text,
            steering_prompt=steering_prompt,
            trustmark_secret=trustmark_secret,
            enable_zebra=True
        )
    
    def is_trustmark_available(self) -> bool:
        """Vérifie si TrustMark est disponible."""
        return self.trustmark_service.is_available()
    
    def is_zebra_available(self) -> bool:
        """Vérifie si le service zèbre est disponible."""
        return self.zebra_service.is_available()
    
    def get_protection_status(self) -> dict:
        """Retourne le statut des différentes protections."""
        return {
            'visible_watermark': True,
            'zebra_pattern': self.is_zebra_available(),
            'trustmark': self.is_trustmark_available()
        }
