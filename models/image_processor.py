"""
Traitement d'images pour l'application de watermarks.
"""

import random
from PIL import Image, ImageDraw, ImageFont
import numpy as np
from typing import Optional
from utils.constants import (
    FONT_PATHS,
    WATERMARK_OPACITY,
    WATERMARK_FONT_SIZE,
    WATERMARK_BASE_ANGLE,
    WATERMARK_CHAOS_STRENGTH
)


class ImageProcessor:
    """Classe pour le traitement d'images et l'application de watermarks visibles."""
    
    def __init__(
        self,
        opacity: int = WATERMARK_OPACITY,
        font_size: int = WATERMARK_FONT_SIZE,
        base_angle: int = WATERMARK_BASE_ANGLE,
        chaos_strength: float = WATERMARK_CHAOS_STRENGTH
    ):
        self.opacity = opacity
        self.font_size = font_size
        self.base_angle = base_angle
        self.chaos_strength = chaos_strength
        self._font = None
    
    def _load_font(self) -> ImageFont.FreeTypeFont:
        """Charge une police depuis le système ou utilise la police par défaut."""
        if self._font is not None:
            return self._font
        
        for font_path in FONT_PATHS:
            try:
                self._font = ImageFont.truetype(font_path, self.font_size)
                return self._font
            except (OSError, IOError):
                continue
        
        # Fallback to default font
        self._font = ImageFont.load_default()
        return self._font
    
    def apply_semantic_steering_watermark(
        self,
        input_image: Image.Image,
        watermark_text: str,
        steering_prompt: str
    ) -> Image.Image:
        """Applique le watermark visible avec semantic steering sur l'image."""
        base = input_image.convert("RGBA")
        width, height = base.size
        
        # Create watermark layer
        watermark_layer = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        draw = ImageDraw.Draw(watermark_layer)
        font = self._load_font()
        
        # Combine watermark text and steering prompt
        combined_text = f"{watermark_text}\nSTEER_PROMPT: {steering_prompt}"
        
        # Apply chaotic repeated watermark with increased spacing
        for y in range(0, height, random.randint(140, 220)):
            for x in range(0, width, random.randint(320, 480)):
                # Random offsets for chaotic placement
                dx = int(random.uniform(-8, 8))
                dy = int(random.uniform(-8, 8))
                local_opacity = int(self.opacity + random.uniform(-15, 15))
                
                draw.text(
                    (x + dx, y + dy),
                    combined_text,
                    fill=(255, 0, 0, max(30, min(180, local_opacity))),
                    font=font
                )
        
        # Multi-angle overlay
        combined = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        
        for angle in [self.base_angle, self.base_angle + 90]:
            layer = watermark_layer.rotate(angle, expand=1)
            layer = layer.crop((0, 0, width, height))
            combined = Image.alpha_composite(combined, layer)
        
        # Chaos noise mask (invisible but affects diffusion models)
        chaos = np.random.randn(height, width) * self.chaos_strength
        chaos = (chaos - chaos.min()) / (chaos.max() - chaos.min())
        chaos = (chaos * 120).astype(np.uint8)
        
        chaos_img = Image.fromarray(chaos, mode="L")
        chaos_rgba = Image.merge("RGBA", (chaos_img, chaos_img, chaos_img, chaos_img))
        
        final_layer = Image.alpha_composite(combined, chaos_rgba)
        
        # Merge into base image
        output = Image.alpha_composite(base, final_layer)
        
        return output.convert("RGB")
