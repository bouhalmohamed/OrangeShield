"""
Tests unitaires pour ZebraService.
"""

import pytest
from PIL import Image
from pathlib import Path
from services.zebra_service import ZebraService


class TestZebraService:
    """Tests pour la classe ZebraService."""
    
    def test_initialization_default_path(self):
        """Test initialisation avec chemin par défaut."""
        service = ZebraService()
        assert service.zebra_path is not None
    
    def test_initialization_custom_path(self, tmp_path):
        """Test initialisation avec chemin personnalisé."""
        custom_path = tmp_path / "custom_zebra.png"
        service = ZebraService(zebra_path=str(custom_path))
        assert service.zebra_path == custom_path
    
    def test_is_available_with_zebra(self, tmp_path):
        """Test disponibilité quand l'image zèbre existe."""
        zebra_path = tmp_path / "zebra.png"
        img = Image.new('RGB', (100, 100), color='white')
        img.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        assert service.is_available() is True
    
    def test_is_available_without_zebra(self, tmp_path):
        """Test disponibilité quand l'image zèbre n'existe pas."""
        service = ZebraService(zebra_path=str(tmp_path / "nonexistent.png"))
        assert service.is_available() is False
    
    def test_remove_white_background(self, tmp_path):
        """Test suppression du fond blanc."""
        zebra_path = tmp_path / "zebra.png"
        img = Image.new('RGBA', (10, 10), color=(255, 255, 255, 255))
        img.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        result = service._remove_white_background(img)
        
        assert result.mode == 'RGBA'
        # Vérifier que les pixels blancs sont transparents
        data = list(result.getdata())
        assert all(pixel[3] == 0 for pixel in data)  # Alpha = 0 pour blanc
    
    def test_get_region_color(self):
        """Test obtention de la couleur moyenne d'une région."""
        service = ZebraService()
        
        img = Image.new('RGB', (100, 100), color=(128, 64, 32))
        color = service._get_region_color(img, 0, 0, 50)
        
        assert color == (128, 64, 32)
    
    def test_get_region_color_out_of_bounds(self):
        """Test couleur de région hors limites."""
        service = ZebraService()
        
        img = Image.new('RGB', (100, 100), color='red')
        color = service._get_region_color(img, 200, 200, 50)
        
        # Doit retourner gris par défaut
        assert color == (128, 128, 128)
    
    def test_tint_image(self, tmp_path):
        """Test application de teinte."""
        zebra_path = tmp_path / "zebra.png"
        img = Image.new('RGBA', (10, 10), color=(100, 100, 100, 255))
        img.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        tinted = service._tint_image(img, (255, 0, 0), strength=0.5)
        
        assert tinted.mode == 'RGBA'
        # La couleur doit être entre l'original et le tint
        pixel = tinted.getpixel((0, 0))
        assert pixel[0] > 100  # Rouge augmenté
    
    def test_create_zebra_variant_resize(self, tmp_path):
        """Test création de variante avec redimensionnement."""
        zebra_path = tmp_path / "zebra.png"
        img = Image.new('RGBA', (200, 100), color=(0, 0, 0, 255))
        img.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        variant = service._create_zebra_variant(img, target_size=50)
        
        assert variant.width == 50
    
    def test_create_zebra_variant_flip(self, tmp_path):
        """Test création de variante avec flip."""
        zebra_path = tmp_path / "zebra.png"
        img = Image.new('RGBA', (100, 100), color=(0, 0, 0, 255))
        img.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        variant = service._create_zebra_variant(img, target_size=50, flip=True)
        
        assert variant is not None
    
    def test_create_zebra_variant_opacity(self, tmp_path):
        """Test création de variante avec opacité réduite."""
        zebra_path = tmp_path / "zebra.png"
        img = Image.new('RGBA', (10, 10), color=(0, 0, 0, 255))
        img.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        variant = service._create_zebra_variant(img, target_size=10, opacity=0.5)
        
        # Vérifier que l'alpha est réduit
        data = list(variant.getdata())
        assert all(pixel[3] < 255 for pixel in data if pixel[3] > 0)
    
    def test_blend_zebra(self, tmp_path):
        """Test fusion du zèbre dans l'image."""
        zebra_path = tmp_path / "zebra.png"
        zebra = Image.new('RGBA', (20, 20), color=(255, 0, 0, 128))
        zebra.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        
        base = Image.new('RGBA', (100, 100), color=(0, 0, 255, 255))
        result = service._blend_zebra(base, zebra, (10, 10))
        
        assert result.size == base.size
        assert result.mode == 'RGBA'
    
    def test_calculate_grid_placements(self):
        """Test calcul des placements en grille."""
        service = ZebraService()
        
        placements = service._calculate_grid_placements(
            width=200, 
            height=200, 
            grid_spacing=100,
            zebra_size=30,
            duplicates=1,
            seed=42
        )
        
        assert len(placements) > 0
        for p in placements:
            assert 'position' in p
            assert 'size' in p
            assert 'opacity' in p
    
    def test_apply_zebra_pattern(self, tmp_path, test_image):
        """Test application du motif zèbre complet."""
        zebra_path = tmp_path / "zebra.png"
        zebra = Image.new('RGBA', (50, 50), color=(0, 0, 0, 255))
        zebra.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        result = service.apply_zebra_pattern(
            test_image,
            grid_spacing=100,
            zebra_size=20,
            opacity_multiplier=0.5,
            seed=42
        )
        
        assert result is not None
        assert result.size == test_image.size
    
    def test_apply_zebra_pattern_preserves_size(self, tmp_path, test_image):
        """Test que le motif préserve la taille de l'image."""
        zebra_path = tmp_path / "zebra.png"
        zebra = Image.new('RGBA', (50, 50), color=(0, 0, 0, 255))
        zebra.save(zebra_path)
        
        service = ZebraService(zebra_path=str(zebra_path))
        original_size = test_image.size
        result = service.apply_zebra_pattern(test_image)
        
        assert result.size == original_size
