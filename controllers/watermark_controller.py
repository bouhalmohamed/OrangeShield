"""
Contrôleur pour les requêtes de watermarking.
"""

from flask import request, jsonify
from PIL import Image
from io import BytesIO
import base64
import uuid
import os
from typing import Dict, Tuple, Optional
from services.watermark_service import WatermarkService
from utils.file_utils import is_allowed_file
from utils.constants import DOCUMENT_PRESETS, DEFAULT_WATERMARK_PAYLOAD, DEFAULT_STEERING_PROMPT, DEFAULT_TRUSTMARK_SECRET
from config import Config


class WatermarkController:
    """Gère les requêtes HTTP pour le watermarking."""
    
    def __init__(self):
        self.watermark_service = WatermarkService()
    
    def process_watermark_request(self) -> Tuple[Dict, int]:
        """Traite une requête d'application de watermark."""
        try:
            # Validate file upload
            validation_error = self._validate_upload()
            if validation_error:
                return validation_error
            
            file = request.files['image']
            
            # Get watermark settings from form data
            watermark_config = self._extract_watermark_config()
            
            # Open and process image
            input_image = Image.open(file.stream)
            
            # Apply dual watermark
            output_image = self.watermark_service.apply_dual_watermark(
                input_image,
                watermark_text=watermark_config['watermark_text'],
                steering_prompt=watermark_config['steering_prompt'],
                trustmark_secret=watermark_config['trustmark_secret']
            )
            
            # Generate response data
            response_data = self._generate_response_data(
                output_image,
                watermark_config['document_type']
            )
            
            return jsonify(response_data), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def _validate_upload(self) -> Optional[Tuple[Dict, int]]:
        """Valide le fichier uploadé."""
        if 'image' not in request.files:
            return jsonify({'error': 'No image uploaded'}), 400
        
        file = request.files['image']
        
        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400
        
        if not is_allowed_file(file.filename):
            return jsonify({
                'error': 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF, WEBP'
            }), 400
        
        return None
    
    def _extract_watermark_config(self) -> Dict[str, str]:
        """Extrait la configuration du watermark depuis les données du formulaire."""
        document_type = request.form.get('document_type', 'default')
        custom_watermark = request.form.get('custom_watermark', '').strip()
        custom_steering = request.form.get('custom_steering', '').strip()
        custom_trustmark = request.form.get('custom_trustmark', '').strip()
        
        # Determine watermark settings based on document type
        if document_type == 'custom':
            # Use custom values, fallback to defaults if empty
            watermark_text = custom_watermark if custom_watermark else DEFAULT_WATERMARK_PAYLOAD
            steering_prompt = custom_steering if custom_steering else DEFAULT_STEERING_PROMPT
            trustmark_secret = custom_trustmark if custom_trustmark else DEFAULT_TRUSTMARK_SECRET
        elif document_type in DOCUMENT_PRESETS:
            preset = DOCUMENT_PRESETS[document_type]
            watermark_text = preset['watermark']
            steering_prompt = preset['steering']
            trustmark_secret = preset['trustmark']
        else:
            # Default watermark
            watermark_text = DEFAULT_WATERMARK_PAYLOAD
            steering_prompt = DEFAULT_STEERING_PROMPT
            trustmark_secret = DEFAULT_TRUSTMARK_SECRET
        
        return {
            'document_type': document_type,
            'watermark_text': watermark_text,
            'steering_prompt': steering_prompt,
            'trustmark_secret': trustmark_secret
        }
    
    def _generate_response_data(
        self,
        output_image: Image.Image,
        document_type: str
    ) -> Dict:
        """Génère les données de réponse avec preview et lien de téléchargement."""
        # Save to bytes
        img_io = BytesIO()
        output_image.save(img_io, 'JPEG', quality=Config.JPEG_QUALITY)
        img_io.seek(0)
        
        # Convert to base64 for preview
        img_base64 = base64.b64encode(img_io.getvalue()).decode('utf-8')
        
        # Generate unique filename
        unique_id = str(uuid.uuid4())[:8]
        output_filename = f"watermarked_{unique_id}.jpg"
        output_path = os.path.join(Config.OUTPUT_FOLDER, output_filename)
        
        # Save file
        img_io.seek(0)
        with open(output_path, 'wb') as f:
            f.write(img_io.read())
        
        return {
            'success': True,
            'preview': f'data:image/jpeg;base64,{img_base64}',
            'download_url': f'/download/{output_filename}',
            'trustmark_applied': self.watermark_service.is_trustmark_available(),
            'watermark_type': document_type
        }
