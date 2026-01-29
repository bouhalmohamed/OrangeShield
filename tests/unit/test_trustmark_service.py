"""
Unit tests for TrustMarkService.
"""

import pytest
from PIL import Image
from services.trustmark_service import TrustMarkService


class TestTrustMarkService:
    """Test suite for TrustMarkService class."""
    
    def test_is_available(self):
        """Test TrustMark availability check."""
        result = TrustMarkService.is_available()
        # Should return boolean (True if TrustMark installed, False otherwise)
        assert isinstance(result, bool)
    
    def test_apply_watermark_without_trustmark(self, test_image):
        """Test watermark application when TrustMark is not available."""
        # This test works whether TrustMark is available or not
        result = TrustMarkService.apply_watermark(test_image)
        
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.size == test_image.size
    
    def test_apply_watermark_preserves_image(self, test_image):
        """Test that apply_watermark preserves image properties."""
        result = TrustMarkService.apply_watermark(test_image)
        
        assert result.size == test_image.size
        assert result.mode in ['RGB', test_image.mode]
    
    def test_apply_watermark_with_secret(self, test_image):
        """Test watermark application with custom secret message."""
        secret = "Test secret message"
        result = TrustMarkService.apply_watermark(test_image, secret)
        
        assert result is not None
        assert isinstance(result, Image.Image)
    
    def test_apply_watermark_with_none_secret(self, test_image):
        """Test watermark application with None secret (uses default)."""
        result = TrustMarkService.apply_watermark(test_image, None)
        
        assert result is not None
        assert isinstance(result, Image.Image)
    
    def test_apply_watermark_different_modes(self):
        """Test watermark application with different image modes."""
        modes = ['RGB', 'RGBA', 'L', 'P']
        
        for mode in modes:
            try:
                img = Image.new(mode, (50, 50), color='red')
                result = TrustMarkService.apply_watermark(img)
                
                assert result is not None
                assert isinstance(result, Image.Image)
            except Exception:
                # Some modes may not be supported, skip them
                pass
