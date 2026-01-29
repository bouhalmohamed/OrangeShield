"""
Unit tests for file utility functions.
"""

import pytest
from utils.file_utils import is_allowed_file, secure_file_path


class TestFileUtils:
    """Test suite for file utility functions."""
    
    def test_is_allowed_file_valid_extensions(self):
        """Test allowed file extensions."""
        valid_files = [
            'test.png',
            'test.jpg',
            'test.jpeg',
            'test.gif',
            'test.webp',
            'TEST.PNG',
            'test.JPG',
            'file.name.png'
        ]
        
        for filename in valid_files:
            assert is_allowed_file(filename) is True
    
    def test_is_allowed_file_invalid_extensions(self):
        """Test invalid file extensions."""
        invalid_files = [
            'test.txt',
            'test.pdf',
            'test.doc',
            'test.exe',
            'test',
            'test.'
        ]
        
        for filename in invalid_files:
            assert is_allowed_file(filename) is False
    
    def test_is_allowed_file_edge_cases(self):
        """Test edge cases for file validation."""
        # .png alone is technically valid (extension only)
        assert is_allowed_file('.png') is True
    
    def test_is_allowed_file_empty(self):
        """Test with empty or None filename."""
        assert is_allowed_file('') is False
        assert is_allowed_file(None) is False
    
    def test_secure_file_path(self):
        """Test secure filename generation."""
        test_cases = [
            ('normal_file.jpg', 'normal_file.jpg'),
            ('file with spaces.png', 'file_with_spaces.png'),
            ('../../../etc/passwd.jpg', 'etc_passwd.jpg'),
            ('file@#$%name.jpg', 'filename.jpg'),
        ]
        
        for input_name, expected_pattern in test_cases:
            result = secure_file_path(input_name)
            # Should not contain dangerous characters
            assert '/' not in result
            assert '\\' not in result
            assert result.endswith('.jpg') or result.endswith('.png')
