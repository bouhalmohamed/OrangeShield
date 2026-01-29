"""
Unit tests for WatermarkService.
"""

import pytest
from PIL import Image
from services.watermark_service import WatermarkService
from utils.constants import (
    DEFAULT_WATERMARK_PAYLOAD,
    DEFAULT_STEERING_PROMPT,
    DEFAULT_TRUSTMARK_SECRET
)


class TestWatermarkService:
    """Test suite for WatermarkService class."""
    
    def test_initialization(self):
        """Test WatermarkService initialization."""
        service = WatermarkService()
        
        assert service.image_processor is not None
        assert service.trustmark_service is not None
    
    def test_apply_dual_watermark_defaults(self, test_image):
        """Test dual watermark application with default values."""
        service = WatermarkService()
        
        result = service.apply_dual_watermark(test_image)
        
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.mode == 'RGB'
        assert result.size == test_image.size
    
    def test_apply_dual_watermark_custom_text(self, test_image):
        """Test dual watermark with custom watermark text."""
        service = WatermarkService()
        
        custom_text = "CUSTOM WATERMARK"
        result = service.apply_dual_watermark(
            test_image,
            watermark_text=custom_text
        )
        
        assert result is not None
        assert isinstance(result, Image.Image)
    
    def test_apply_dual_watermark_custom_steering(self, test_image):
        """Test dual watermark with custom steering prompt."""
        service = WatermarkService()
        
        custom_steering = "Custom steering prompt"
        result = service.apply_dual_watermark(
            test_image,
            steering_prompt=custom_steering
        )
        
        assert result is not None
        assert isinstance(result, Image.Image)
    
    def test_apply_dual_watermark_custom_trustmark(self, test_image):
        """Test dual watermark with custom TrustMark secret."""
        service = WatermarkService()
        
        custom_secret = "Custom secret"
        result = service.apply_dual_watermark(
            test_image,
            trustmark_secret=custom_secret
        )
        
        assert result is not None
        assert isinstance(result, Image.Image)
    
    def test_apply_dual_watermark_all_custom(self, test_image):
        """Test dual watermark with all custom parameters."""
        service = WatermarkService()
        
        result = service.apply_dual_watermark(
            test_image,
            watermark_text="Custom watermark",
            steering_prompt="Custom steering",
            trustmark_secret="Custom secret"
        )
        
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.size == test_image.size
    
    def test_apply_dual_watermark_preserves_size(self, test_image):
        """Test that dual watermarking preserves image size."""
        service = WatermarkService()
        
        original_size = test_image.size
        result = service.apply_dual_watermark(test_image)
        
        assert result.size == original_size
    
    def test_is_trustmark_available(self):
        """Test TrustMark availability check."""
        service = WatermarkService()
        
        result = service.is_trustmark_available()
        assert isinstance(result, bool)
    
    def test_apply_dual_watermark_empty_text(self, test_image):
        """Test dual watermark with empty text."""
        service = WatermarkService()
        
        result = service.apply_dual_watermark(
            test_image,
            watermark_text="",
            steering_prompt=""
        )
        
        assert result is not None
        assert isinstance(result, Image.Image)
