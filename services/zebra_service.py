"""
Service d'intégration de zèbres - ajoute des motifs de zèbres subtils dans les images
pour créer une confusion sémantique contre les modèles IA génératifs.
"""

import random
from PIL import Image, ImageFilter, ImageStat
from pathlib import Path
from typing import Tuple, List, Dict, Optional


class ZebraService:
    """Service pour intégrer des zèbres dans les images."""
    
    def __init__(self, zebra_path: Optional[str] = None):
        """Initialise le service avec le chemin vers l'image du zèbre."""
        if zebra_path is None:
            # Chemin par défaut vers zebra.png à la racine du projet
            self.zebra_path = Path(__file__).parent.parent / 'zebra.png'
        else:
            self.zebra_path = Path(zebra_path)
        
        self._zebra_clean = None
    
    def _load_zebra(self) -> Image.Image:
        """Charge et prépare l'image du zèbre."""
        if self._zebra_clean is not None:
            return self._zebra_clean
        
        if not self.zebra_path.exists():
            raise FileNotFoundError(f"Image zèbre non trouvée: {self.zebra_path}")
        
        zebra = Image.open(self.zebra_path).convert('RGBA')
        self._zebra_clean = self._remove_white_background(zebra)
        return self._zebra_clean
    
    def _remove_white_background(self, img: Image.Image) -> Image.Image:
        """Supprime le fond blanc de l'image du zèbre."""
        img = img.convert('RGBA')
        data = list(img.getdata())
        new_data = []
        
        for pixel in data:
            r, g, b, a = pixel
            brightness = (r + g + b) / 3
            
            if r > 240 and g > 240 and b > 240:
                new_data.append((r, g, b, 0))
            elif r > 220 and g > 220 and b > 220:
                alpha = int((255 - brightness) * 3)
                alpha = min(255, max(0, alpha))
                new_data.append((r, g, b, alpha))
            else:
                new_data.append(pixel)
        
        result = Image.new('RGBA', img.size)
        result.putdata(new_data)
        return result
    
    def _get_region_color(self, img: Image.Image, x: int, y: int, size: int) -> Tuple[int, int, int]:
        """Obtient la couleur moyenne d'une région de l'image."""
        left = max(0, x)
        top = max(0, y)
        right = min(img.width, x + size)
        bottom = min(img.height, y + size)
        
        if right <= left or bottom <= top:
            return (128, 128, 128)
        
        region = img.crop((left, top, right, bottom))
        stat = ImageStat.Stat(region)
        return tuple(int(c) for c in stat.mean[:3])
    
    def _tint_image(self, img: Image.Image, tint_color: Tuple[int, int, int], 
                    strength: float = 0.3) -> Image.Image:
        """Applique une teinte pour mélanger le zèbre avec le fond."""
        img = img.convert('RGBA')
        data = list(img.getdata())
        new_data = []
        
        tr, tg, tb = tint_color
        
        for pixel in data:
            r, g, b, a = pixel
            if a > 0:
                new_r = int(r * (1 - strength) + tr * strength)
                new_g = int(g * (1 - strength) + tg * strength)
                new_b = int(b * (1 - strength) + tb * strength)
                new_data.append((new_r, new_g, new_b, a))
            else:
                new_data.append(pixel)
        
        result = Image.new('RGBA', img.size)
        result.putdata(new_data)
        return result
    
    def _create_zebra_variant(self, zebra_img: Image.Image, target_size: int,
                              flip: bool = False, rotation: float = 0, 
                              opacity: float = 1.0, blur_amount: float = 0,
                              tint_color: Optional[Tuple[int, int, int]] = None,
                              tint_strength: float = 0.3) -> Image.Image:
        """Crée une variante du zèbre avec des transformations."""
        aspect = zebra_img.width / zebra_img.height
        new_width = target_size
        new_height = int(target_size / aspect)
        
        variant = zebra_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
        
        if flip:
            variant = variant.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        
        if rotation != 0:
            variant = variant.rotate(rotation, expand=True, resample=Image.Resampling.BICUBIC)
        
        if tint_color:
            variant = self._tint_image(variant, tint_color, tint_strength)
        
        if blur_amount > 0:
            r, g, b, a = variant.split()
            rgb = Image.merge('RGB', (r, g, b))
            rgb = rgb.filter(ImageFilter.GaussianBlur(blur_amount))
            r, g, b = rgb.split()
            variant = Image.merge('RGBA', (r, g, b, a))
        
        if opacity < 1.0:
            data = list(variant.getdata())
            new_data = []
            for pixel in data:
                r, g, b, a = pixel
                new_a = int(a * opacity)
                new_data.append((r, g, b, new_a))
            variant = Image.new('RGBA', variant.size)
            variant.putdata(new_data)
        
        return variant
    
    def _blend_zebra(self, base_img: Image.Image, zebra: Image.Image, 
                     position: Tuple[int, int]) -> Image.Image:
        """Mélange un zèbre dans l'image de base."""
        x, y = position
        zebra_layer = Image.new('RGBA', base_img.size, (0, 0, 0, 0))
        
        paste_x = max(0, x)
        paste_y = max(0, y)
        
        crop_left = max(0, -x)
        crop_top = max(0, -y)
        crop_right = min(zebra.width, base_img.width - x)
        crop_bottom = min(zebra.height, base_img.height - y)
        
        if crop_right > crop_left and crop_bottom > crop_top:
            cropped_zebra = zebra.crop((crop_left, crop_top, crop_right, crop_bottom))
            zebra_layer.paste(cropped_zebra, (paste_x, paste_y))
        
        return Image.alpha_composite(base_img, zebra_layer)
    
    def _calculate_grid_placements(self, width: int, height: int, 
                                   grid_spacing: int = 50,
                                   zebra_size: int = 30,
                                   duplicates: int = 1,
                                   seed: Optional[int] = None) -> List[Dict]:
        """Calcule les placements en grille des zèbres."""
        if seed is not None:
            random.seed(seed)
        
        placements = []
        
        for y in range(0, height, grid_spacing):
            for x in range(0, width, grid_spacing):
                for _ in range(duplicates):
                    offset_x = random.randint(-5, 5)
                    offset_y = random.randint(-5, 5)
                    size_var = zebra_size + random.randint(-5, 5)
                    size_var = max(10, size_var)
                    
                    placements.append({
                        'position': (x + offset_x, y + offset_y),
                        'size': size_var,
                        'flip': random.choice([True, False]),
                        'rotation': random.uniform(-25, 25),
                        'opacity': random.uniform(0.25, 0.40),
                        'blur': random.uniform(0.1, 0.4),
                        'tint_strength': random.uniform(0.25, 0.40),
                    })
        
        return placements
    
    def apply_zebra_pattern(self, image: Image.Image, 
                            grid_spacing: int = 50,
                            zebra_size: int = 30,
                            opacity_multiplier: float = 1.0,
                            seed: Optional[int] = None) -> Image.Image:
        """
        Applique le motif de zèbres sur l'image.
        
        Args:
            image: Image PIL en entrée
            grid_spacing: Espacement de la grille en pixels
            zebra_size: Taille des zèbres
            opacity_multiplier: Multiplicateur d'opacité
            seed: Seed pour reproductibilité
        
        Returns:
            Image avec motif de zèbres intégré
        """
        zebra_clean = self._load_zebra()
        
        base_img = image.convert('RGBA')
        width, height = base_img.size
        
        placements = self._calculate_grid_placements(
            width, height, grid_spacing, zebra_size, 
            duplicates=1, seed=seed
        )
        
        result = base_img.copy()
        
        for placement in placements:
            x, y = placement['position']
            
            tint_color = self._get_region_color(base_img, x, y, placement['size'])
            
            zebra_variant = self._create_zebra_variant(
                zebra_clean,
                placement['size'],
                flip=placement['flip'],
                rotation=placement['rotation'],
                opacity=placement['opacity'] * opacity_multiplier,
                blur_amount=placement['blur'],
                tint_color=tint_color,
                tint_strength=placement['tint_strength']
            )
            
            result = self._blend_zebra(result, zebra_variant, placement['position'])
        
        return result
    
    def is_available(self) -> bool:
        """Vérifie si le service est disponible (image zèbre présente)."""
        return self.zebra_path.exists()
