"""
Unit tests for ImageProcessor model.
"""

import pytest
from PIL import Image
from models.image_processor import ImageProcessor


class TestImageProcessor:
    """Test suite for ImageProcessor class."""
    
    def test_initialization_defaults(self):
        """Test ImageProcessor initialization with default parameters."""
        processor = ImageProcessor()
        
        assert processor.opacity == 55
        assert processor.font_size == 16
        assert processor.base_angle == 25
        assert processor.chaos_strength == 0.08
        assert processor._font is None
    
    def test_initialization_custom(self):
        """Test ImageProcessor initialization with custom parameters."""
        processor = ImageProcessor(
            opacity=100,
            font_size=20,
            base_angle=45,
            chaos_strength=0.1
        )
        
        assert processor.opacity == 100
        assert processor.font_size == 20
        assert processor.base_angle == 45
        assert processor.chaos_strength == 0.1
    
    def test_load_font(self, test_image):
        """Test font loading."""
        processor = ImageProcessor()
        font = processor._load_font()
        
        assert font is not None
    
    def test_apply_semantic_steering_watermark_basic(self, test_image):
        """Test basic watermark application."""
        processor = ImageProcessor()
        watermark_text = "TEST WATERMARK"
        steering_prompt = "Test steering"
        
        result = processor.apply_semantic_steering_watermark(
            test_image,
            watermark_text,
            steering_prompt
        )
        
        assert result is not None
        assert isinstance(result, Image.Image)
        assert result.mode == 'RGB'
        assert result.size == test_image.size
    
    def test_apply_semantic_steering_watermark_preserves_size(self, test_image):
        """Test that watermarking preserves image dimensions."""
        processor = ImageProcessor()
        
        original_size = test_image.size
        result = processor.apply_semantic_steering_watermark(
            test_image,
            "TEST",
            "PROMPT"
        )
        
        assert result.size == original_size
    
    def test_apply_semantic_steering_watermark_different_sizes(self):
        """Test watermarking with different image sizes."""
        processor = ImageProcessor()
        
        sizes = [(50, 50), (200, 200), (100, 300), (500, 100)]
        
        for width, height in sizes:
            img = Image.new('RGB', (width, height), color='green')
            result = processor.apply_semantic_steering_watermark(
                img,
                "TEST",
                "PROMPT"
            )
            
            assert result.size == (width, height)
            assert result.mode == 'RGB'
    
    def test_apply_semantic_steering_watermark_empty_text(self, test_image):
        """Test watermarking with empty text."""
        processor = ImageProcessor()
        
        result = processor.apply_semantic_steering_watermark(
            test_image,
            "",
            ""
        )
        
        assert result is not None
        assert result.mode == 'RGB'
    
    def test_apply_semantic_steering_watermark_long_text(self, test_image):
        """Test watermarking with long text."""
        processor = ImageProcessor()
        
        long_text = "A" * 100
        result = processor.apply_semantic_steering_watermark(
            test_image,
            long_text,
            "PROMPT"
        )
        
        assert result is not None
        assert result.mode == 'RGB'
