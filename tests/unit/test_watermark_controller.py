"""
Unit tests for WatermarkController.
"""

import pytest
from unittest.mock import Mock, patch, MagicMock
from flask import Flask, request
from controllers.watermark_controller import WatermarkController
from utils.constants import DOCUMENT_PRESETS, DEFAULT_WATERMARK_PAYLOAD


class TestWatermarkController:
    """Test suite for WatermarkController class."""
    
    def test_initialization(self):
        """Test WatermarkController initialization."""
        controller = WatermarkController()
        
        assert controller.watermark_service is not None
    
    def test_validate_upload_no_file(self, app):
        """Test validation when no file is uploaded."""
        with app.test_request_context():
            controller = WatermarkController()
            result = controller._validate_upload()
            
            assert result is not None
            assert result[1] == 400
    
    def test_validate_upload_empty_filename(self, app):
        """Test validation when filename is empty."""
        with app.test_request_context():
            from werkzeug.datastructures import FileStorage
            empty_file = FileStorage(stream=Mock(), filename='', name='image')
            
            with patch('controllers.watermark_controller.request') as mock_request:
                mock_request.files = {'image': empty_file}
                controller = WatermarkController()
                result = controller._validate_upload()
                
                assert result is not None
                assert result[1] == 400
    
    def test_validate_upload_invalid_extension(self, app):
        """Test validation with invalid file extension."""
        with app.test_request_context():
            from werkzeug.datastructures import FileStorage
            from io import BytesIO
            invalid_file = FileStorage(
                stream=BytesIO(b'test'),
                filename='test.txt',
                name='image'
            )
            
            with patch('controllers.watermark_controller.request') as mock_request:
                mock_request.files = {'image': invalid_file}
                controller = WatermarkController()
                result = controller._validate_upload()
                
                assert result is not None
                assert result[1] == 400
    
    def test_validate_upload_valid(self, app):
        """Test validation with valid file."""
        with app.test_request_context():
            from werkzeug.datastructures import FileStorage
            from io import BytesIO
            valid_file = FileStorage(
                stream=BytesIO(b'test'),
                filename='test.jpg',
                name='image'
            )
            
            with patch('controllers.watermark_controller.request') as mock_request:
                mock_request.files = {'image': valid_file}
                controller = WatermarkController()
                result = controller._validate_upload()
                
                assert result is None
    
    def test_extract_watermark_config_default(self, app):
        """Test extracting default watermark config."""
        with app.test_request_context(data={'document_type': 'default'}):
            controller = WatermarkController()
            config = controller._extract_watermark_config()
            
            assert config['document_type'] == 'default'
            assert 'watermark_text' in config
            assert 'steering_prompt' in config
            assert 'trustmark_secret' in config
    
    def test_extract_watermark_config_preset(self, app):
        """Test extracting preset watermark config."""
        with app.test_request_context(data={'document_type': 'confidential'}):
            controller = WatermarkController()
            config = controller._extract_watermark_config()
            
            assert config['document_type'] == 'confidential'
            assert config['watermark_text'] == DOCUMENT_PRESETS['confidential']['watermark']
    
    def test_extract_watermark_config_custom(self, app):
        """Test extracting custom watermark config."""
        with app.test_request_context(data={
            'document_type': 'custom',
            'custom_watermark': 'Custom text',
            'custom_steering': 'Custom steering',
            'custom_trustmark': 'Custom secret'
        }):
            controller = WatermarkController()
            config = controller._extract_watermark_config()
            
            assert config['document_type'] == 'custom'
            assert config['watermark_text'] == 'Custom text'
            assert config['steering_prompt'] == 'Custom steering'
            assert config['trustmark_secret'] == 'Custom secret'
    
    def test_extract_watermark_config_custom_empty(self, app):
        """Test extracting custom config with empty values (uses defaults)."""
        with app.test_request_context(data={
            'document_type': 'custom',
            'custom_watermark': '',
            'custom_steering': '',
            'custom_trustmark': ''
        }):
            controller = WatermarkController()
            config = controller._extract_watermark_config()
            
            assert config['watermark_text'] == DEFAULT_WATERMARK_PAYLOAD
    
    @patch('controllers.watermark_controller.os.path.join')
    @patch('controllers.watermark_controller.open')
    @patch('controllers.watermark_controller.Config')
    def test_generate_response_data(self, mock_config, mock_open, mock_join, test_image):
        """Test response data generation."""
        mock_join.return_value = '/tmp/test.jpg'
        mock_config.OUTPUT_FOLDER = '/tmp'
        mock_config.JPEG_QUALITY = 95
        
        controller = WatermarkController()
        result = controller._generate_response_data(test_image, 'default')
        
        assert 'success' in result
        assert result['success'] is True
        assert 'preview' in result
        assert 'download_url' in result
        assert 'trustmark_applied' in result
        assert 'watermark_type' in result
        assert result['watermark_type'] == 'default'
        assert result['preview'].startswith('data:image/jpeg;base64,')
