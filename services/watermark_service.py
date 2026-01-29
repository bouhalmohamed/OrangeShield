"""
Service de watermarking - coordonne l'application des watermarks visible et invisible.
"""

from PIL import Image
from typing import Optional
from models.image_processor import ImageProcessor
from services.trustmark_service import TrustMarkService
from utils.constants import (
    DEFAULT_WATERMARK_PAYLOAD,
    DEFAULT_STEERING_PROMPT,
    DEFAULT_TRUSTMARK_SECRET
)


class WatermarkService:
    """Service pour appliquer le double watermark (visible + invisible)."""
    
    def __init__(self):
        self.image_processor = ImageProcessor()
        self.trustmark_service = TrustMarkService()
    
    def apply_dual_watermark(
        self,
        input_image: Image.Image,
        watermark_text: Optional[str] = None,
        steering_prompt: Optional[str] = None,
        trustmark_secret: Optional[str] = None
    ) -> Image.Image:
        """Applique le watermark visible et invisible sur l'image."""
        # Use defaults if not provided
        if watermark_text is None:
            watermark_text = DEFAULT_WATERMARK_PAYLOAD
        if steering_prompt is None:
            steering_prompt = DEFAULT_STEERING_PROMPT
        if trustmark_secret is None:
            trustmark_secret = DEFAULT_TRUSTMARK_SECRET
        
        # Step 1: Apply visible semantic steering watermark
        visible_watermarked = self.image_processor.apply_semantic_steering_watermark(
            input_image,
            watermark_text=watermark_text,
            steering_prompt=steering_prompt
        )
        
        # Step 2: Apply invisible TrustMark watermark
        final_image = self.trustmark_service.apply_watermark(
            visible_watermarked,
            secret_message=trustmark_secret
        )
        
        return final_image
    
    def is_trustmark_available(self) -> bool:
        """Vérifie si TrustMark est disponible."""
        return self.trustmark_service.is_available()
