"""
Integration tests for Flask routes.
"""

import pytest
from io import BytesIO
from PIL import Image


class TestRoutes:
    """Integration tests for Flask routes."""
    
    def test_index_route(self, client):
        """Test index page route."""
        response = client.get('/')
        
        assert response.status_code == 200
        assert b'OrangeShield' in response.data or b'watermark' in response.data.lower()
    
    def test_apply_watermark_no_file(self, client):
        """Test watermark route without file upload."""
        response = client.post('/apply-watermark')
        
        assert response.status_code == 400
        data = response.get_json()
        assert 'error' in data
        assert 'No image uploaded' in data['error']
    
    def test_apply_watermark_empty_filename(self, client):
        """Test watermark route with empty filename."""
        data = {
            'image': (BytesIO(b''), '')
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
    
    def test_apply_watermark_invalid_file_type(self, client, test_image_bytes):
        """Test watermark route with invalid file type."""
        data = {
            'image': (BytesIO(test_image_bytes), 'test.txt')
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 400
        json_data = response.get_json()
        assert 'error' in json_data
        assert 'Invalid file type' in json_data['error']
    
    def test_apply_watermark_valid_jpg(self, client, test_image_bytes):
        """Test watermark route with valid JPG file."""
        data = {
            'image': (BytesIO(test_image_bytes), 'test.jpg'),
            'document_type': 'default'
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert 'preview' in json_data
        assert 'download_url' in json_data
        assert json_data['preview'].startswith('data:image/jpeg;base64,')
        assert json_data['download_url'].startswith('/download/')
    
    def test_apply_watermark_valid_png(self, client):
        """Test watermark route with valid PNG file."""
        img = Image.new('RGB', (50, 50), color='green')
        img_bytes = BytesIO()
        img.save(img_bytes, format='PNG')
        img_bytes.seek(0)
        
        data = {
            'image': (img_bytes, 'test.png'),
            'document_type': 'default'
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
    
    def test_apply_watermark_with_preset(self, client, test_image_bytes):
        """Test watermark route with document preset."""
        data = {
            'image': (BytesIO(test_image_bytes), 'test.jpg'),
            'document_type': 'confidential'
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['watermark_type'] == 'confidential'
    
    def test_apply_watermark_with_custom(self, client, test_image_bytes):
        """Test watermark route with custom watermark."""
        data = {
            'image': (BytesIO(test_image_bytes), 'test.jpg'),
            'document_type': 'custom',
            'custom_watermark': 'My Custom Watermark',
            'custom_steering': 'My steering prompt',
            'custom_trustmark': 'My secret'
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        assert json_data['success'] is True
        assert json_data['watermark_type'] == 'custom'
    
    def test_download_file_not_found(self, client):
        """Test download route with non-existent file."""
        response = client.get('/download/nonexistent.jpg')
        
        assert response.status_code == 404
        json_data = response.get_json()
        assert 'error' in json_data
    
    def test_download_file_exists(self, client, test_image_bytes, temp_dirs):
        """Test download route with existing file."""
        import os
        from config import Config
        
        # Create a test file in output directory
        test_filename = 'test_download.jpg'
        test_path = os.path.join(temp_dirs['output'], test_filename)
        
        with open(test_path, 'wb') as f:
            f.write(test_image_bytes)
        
        # Temporarily override output folder
        original_output = Config.OUTPUT_FOLDER
        Config.OUTPUT_FOLDER = temp_dirs['output']
        
        try:
            response = client.get(f'/download/{test_filename}')
            assert response.status_code == 200
            assert response.content_type == 'image/jpeg'
        finally:
            Config.OUTPUT_FOLDER = original_output
    
    def test_apply_watermark_response_structure(self, client, test_image_bytes):
        """Test that watermark response has correct structure."""
        data = {
            'image': (BytesIO(test_image_bytes), 'test.jpg'),
            'document_type': 'default'
        }
        response = client.post('/apply-watermark', data=data, content_type='multipart/form-data')
        
        assert response.status_code == 200
        json_data = response.get_json()
        
        required_keys = ['success', 'preview', 'download_url', 'trustmark_applied', 'watermark_type']
        for key in required_keys:
            assert key in json_data, f"Missing key: {key}"
        
        assert isinstance(json_data['success'], bool)
        assert isinstance(json_data['trustmark_applied'], bool)
        assert isinstance(json_data['watermark_type'], str)
